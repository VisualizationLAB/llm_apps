# agents/base_agent.py
"""
Base Agent class for the provider network management system
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from databricks.sdk import WorkspaceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all network management agents"""
    
    def __init__(self, workspace_client: WorkspaceClient, model_endpoint: str = None):
        self.workspace_client = workspace_client
        self.model_endpoint = model_endpoint or self._find_best_model_endpoint()
        self.workspace_url = self._get_workspace_url()
        self.token = self._get_databricks_token()
        
    def _find_best_model_endpoint(self) -> str:
        """Find the best available Databricks LLM endpoint"""
        try:
            endpoints = self.workspace_client.serving_endpoints.list()
            
            # Preferred model order
            preferred_models = [
                "databricks-llama-2-70b-chat",
                "databricks-mpt-30b-instruct", 
                "databricks-dolly-v2-12b"
            ]
            
            for model in preferred_models:
                for endpoint in endpoints:
                    if model in endpoint.name.lower():
                        logger.info(f"Using model endpoint: {endpoint.name}")
                        return endpoint.name
            
            # Fallback to first available endpoint
            if endpoints:
                fallback = endpoints[0].name
                logger.warning(f"Using fallback endpoint: {fallback}")
                return fallback
                
        except Exception as e:
            logger.error(f"Error finding model endpoint: {e}")
            
        return "databricks-llama-2-7b-chat"  # Default fallback
    
    def _get_workspace_url(self) -> str:
        """Get Databricks workspace URL"""
        try:
            return dbutils.secrets.get(scope="network-app", key="workspace-url")
        except:
            return "https://your-workspace.databricks.com"
    
    def _get_databricks_token(self) -> str:
        """Get Databricks access token"""
        try:
            return dbutils.secrets.get(scope="network-app", key="databricks-token")
        except:
            return dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
    
    def call_llm(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.3) -> str:
        """Call Databricks LLM with error handling and retries"""
        
        url = f"{self.workspace_url}/serving-endpoints/{self.model_endpoint}/invocations"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "inputs": {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("predictions", [{}])[0].get("generated_text", "")
            
            # Clean up the response
            return self._clean_llm_response(generated_text)
            
        except requests.exceptions.Timeout:
            logger.error("LLM request timed out")
            return "Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            logger.error(f"LLM request failed: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in LLM call: {e}")
            return "An unexpected error occurred. Please try again."
    
    def _clean_llm_response(self, response: str) -> str:
        """Clean and format LLM response"""
        # Remove any prompt repetition
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that look like prompt repetition
            if not any(skip_phrase in line.lower() for skip_phrase in [
                "human:", "assistant:", "user:", "system:", "response:"
            ]):
                cleaned_lines.append(line)
        
        cleaned_response = '\n'.join(cleaned_lines).strip()
        
        # Ensure response isn't too long
        if len(cleaned_response) > 2000:
            cleaned_response = cleaned_response[:2000] + "..."
        
        return cleaned_response
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request and return response"""
        pass
    
    def log_interaction(self, request: Dict[str, Any], response: Dict[str, Any]):
        """Log agent interactions for monitoring"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": self.__class__.__name__,
            "request": request,
            "response_summary": {
                "success": response.get("success", False),
                "response_length": len(str(response))
            },
            "model_endpoint": self.model_endpoint
        }
        
        logger.info(f"Agent interaction: {json.dumps(log_entry, indent=2)}")