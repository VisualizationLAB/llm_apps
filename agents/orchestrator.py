
# agents/orchestrator.py
"""
Agent Orchestrator - Coordinates multiple agents and manages conversations
"""

from typing import Dict, Any, List, Optional
import json
from .base_agent import BaseAgent
from .network_analyzer_agent import NetworkAnalyzerAgent
from .cost_optimizer_agent import CostOptimizerAgent
from .report_generator_agent import ReportGeneratorAgent

class AgentOrchestrator:
    """Orchestrates multiple specialized agents for complex network management tasks"""
    
    def __init__(self, workspace_client):
        self.workspace_client = workspace_client
        
        # Initialize specialized agents
        self.network_analyzer = NetworkAnalyzerAgent(workspace_client)
        self.cost_optimizer = CostOptimizerAgent(workspace_client)
        self.report_generator = ReportGeneratorAgent(workspace_client)
        
        # Agent routing configuration
        self.agent_routes = {
            "network_analysis": self.network_analyzer,
            "cost_optimization": self.cost_optimizer,
            "report_generation": self.report_generator
        }
        
        self.conversation_history = []
    
    def route_request(self, user_query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Route user requests to appropriate agents"""
        
        # Determine intent and route to appropriate agent
        intent = self._classify_intent(user_query)
        
        if intent["primary_agent"] == "multi_agent":
            # Complex request requiring multiple agents
            return self._handle_multi_agent_request(user_query, context, intent)
        else:
            # Single agent request
            agent = self.agent_routes.get(intent["primary_agent"])
            if agent:
                request = self._build_agent_request(user_query, context, intent)
                return agent.process_request(request)
            else:
                return self._handle_general_query(user_query, context)
    
    def _classify_intent(self, user_query: str) -> Dict[str, Any]:
        """Classify user intent to route to appropriate agent"""
        
        query_lower = user_query.lower()
        
        # Cost-related keywords
        cost_keywords = ["cost", "save", "savings", "expensive", "budget", "reduce", "optimize", "financial"]
        
        # Analysis keywords
        analysis_keywords = ["analyze", "performance", "quality", "score", "compare", "benchmark", "trend"]
        
        # Report keywords
        report_keywords = ["report", "summary", "document", "generate", "download", "pdf", "presentation"]
        
        # Multi-agent keywords (complex requests)
        complex_keywords = ["comprehensive", "detailed", "full analysis", "complete", "everything"]
        
        intent = {
            "primary_agent": "network_analysis",  # Default
            "secondary_agents": [],
            "complexity": "simple",
            "keywords_found": []
        }
        
        # Check for complex multi-agent requests
        if any(keyword in query_lower for keyword in complex_keywords):
            intent["complexity"] = "complex"
            intent["primary_agent"] = "multi_agent"
            intent["secondary_agents"] = ["network_analysis", "cost_optimization", "report_generation"]
        
        # Check for specific agent routes
        elif any(keyword in query_lower for keyword in cost_keywords):
            intent["primary_agent"] = "cost_optimization"
            intent["keywords_found"].extend([k for k in cost_keywords if k in query_lower])
        
        elif any(keyword in query_lower for keyword in report_keywords):
            intent["primary_agent"] = "report_generation"
            intent["keywords_found"].extend([k for k in report_keywords if k in query_lower])
        
        elif any(keyword in query_lower for keyword in analysis_keywords):
            intent["primary_agent"] = "network_analysis"
            intent["keywords_found"].extend([k for k in analysis_keywords if k in query_lower])
        
        return intent
    
    def _handle_multi_agent_request(self, user_query: str, context: Dict[str, Any], 
                                  intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle complex requests requiring multiple agents"""
        
        results = {
            "success": True,
            "multi_agent_response": True,
            "user_query": user_query,
            "agent_responses": {},
            "integrated_response": "",
            "timestamp": datetime.now().isoformat()
        }
        
        # Get analysis from network analyzer
        if "network_analysis" in intent["secondary_agents"]:
            analysis_request = {
                "analysis_type": "network_summary",
                "provider_data": context
            }
            analysis_result = self.network_analyzer.process_request(analysis_request)
            results["agent_responses"]["network_analysis"] = analysis_result
        
        # Get cost optimization insights
        if "cost_optimization" in intent["secondary_agents"]:
            cost_request = {
                "optimization_type": "general",
                "provider_data": context
            }
            cost_result = self.cost_optimizer.process_request(cost_request)
            results["agent_responses"]["cost_optimization"] = cost_result
        
        # Generate integrated report
        if "report_generation" in intent["secondary_agents"]:
            report_request = {
                "report_type": "comprehensive",
                "data": context,
                "focus_areas": ["performance", "costs", "optimization"]
            }
            report_result = self.report_generator.process_request(report_request)
            results["agent_responses"]["report_generation"] = report_result
        
        # Integrate responses
        results["integrated_response"] = self._integrate_agent_responses(
            user_query, results["agent_responses"]
        )
        
        return results
    
    def _integrate_agent_responses(self, user_query: str, agent_responses: Dict) -> str:
        """Integrate responses from multiple agents into coherent answer"""
        
        integration_prompt = f"""
        User asked: "{user_query}"
        
        Agent Responses:
        
        Network Analysis:
        {agent_responses.get('network_analysis', {}).get('analysis', 'Not available')}
        
        Cost Optimization:
        {agent_responses.get('cost_optimization', {}).get('strategies', 'Not available')}
        
        Report Content:
        {agent_responses.get('report_generation', {}).get('report_content', 'Not available')}
        
        Please integrate these agent responses into a single, coherent response that:
        1. Directly answers the user's question
        2. Combines insights from all agents
        3. Provides a logical flow of information
        4. Includes specific recommendations
        5. Uses clear, professional language
        
        Format as a well-structured response with clear sections.
        """
        
        # Use the network analyzer's LLM for integration
        integrated_response = self.network_analyzer.call_llm(integration_prompt, max_tokens=1500)
        
        return integrated_response
    
    def _build_agent_request(self, user_query: str, context: Dict[str, Any], 
                           intent: Dict[str, Any]) -> Dict[str, Any]:
        """Build appropriate request object for specific agent"""
        
        base_request = {
            "user_query": user_query,
            "provider_data": context,
            "intent": intent
        }
        
        # Customize request based on agent type
        if intent["primary_agent"] == "cost_optimization":
            # Extract cost-specific parameters
            if "save" in user_query.lower() or "reduce" in user_query.lower():
                base_request["optimization_type"] = "cost_reduction"
            else:
                base_request["optimization_type"] = "general"
        
        elif intent["primary_agent"] == "network_analysis":
            # Extract analysis-specific parameters
            if any(provider_term in user_query.lower() for provider_term in ["dr.", "provider", "doctor"]):
                base_request["analysis_type"] = "provider_performance"
            else:
                base_request["analysis_type"] = "network_summary"
        
        elif intent["primary_agent"] == "report_generation":
            # Extract report-specific parameters
            if "executive" in user_query.lower() or "summary" in user_query.lower():
                base_request["report_type"] = "executive_summary"
            else:
                base_request["report_type"] = "provider_diagnostics"
        
        return base_request
    
    def _handle_general_query(self, user_query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general queries that don't fit specific agent patterns"""
        
        # Use network analyzer for general queries
        general_request = {
            "analysis_type": "general",
            "user_query": user_query,
            "provider_data": context
        }
        
        return self.network_analyzer.process_request(general_request)
    
    def get_conversation_summary(self) -> str:
        """Generate summary of conversation history"""
        
        if not self.conversation_history:
            return "No conversation history available."
        
        summary_prompt = f"""
        Conversation History:
        {json.dumps(self.conversation_history[-10:], indent=2)}
        
        Provide a brief summary of the key topics discussed and insights provided.
        Focus on actionable recommendations and important findings.
        """
        
        return self.network_analyzer.call_llm(summary_prompt)
    
    def add_to_conversation(self, user_query: str, response: Dict[str, Any]):
        """Add interaction to conversation history"""
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "response_summary": {
                "success": response.get("success", False),
                "primary_agent": response.get("primary_agent", "unknown"),
                "key_insights": response.get("key_insights", [])
            }
        })
        
        # Keep last 50 interactions
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]