

# agents/network_analyzer_agent.py
"""
Network Analysis Agent - Handles network performance analysis
"""

from typing import Dict, Any, List
import pandas as pd
from .base_agent import BaseAgent

class NetworkAnalyzerAgent(BaseAgent):
    """Agent specialized in network performance analysis"""
    
    def get_system_prompt(self) -> str:
        return """
        You are a Network Analysis Expert specializing in healthcare provider networks.
        Your role is to analyze provider performance, identify trends, and provide insights.
        
        Key responsibilities:
        - Analyze provider quality scores and efficiency metrics
        - Identify top and bottom performers
        - Calculate network averages and benchmarks
        - Provide specific, data-driven insights
        
        Always provide:
        1. Clear performance summaries
        2. Specific metrics and comparisons
        3. Actionable insights
        4. Risk assessments where applicable
        
        Keep responses concise, data-focused, and professional.
        """
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process network analysis requests"""
        
        analysis_type = request.get("analysis_type", "general")
        provider_data = request.get("provider_data", {})
        specific_provider = request.get("provider_id")
        
        try:
            if analysis_type == "provider_performance":
                return self._analyze_provider_performance(provider_data, specific_provider)
            elif analysis_type == "network_summary":
                return self._analyze_network_summary(provider_data)
            elif analysis_type == "quality_trends":
                return self._analyze_quality_trends(provider_data)
            elif analysis_type == "cost_analysis":
                return self._analyze_cost_performance(provider_data)
            else:
                return self._general_network_analysis(provider_data)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to complete network analysis"
            }
    
    def _analyze_provider_performance(self, data: Dict, provider_id: str = None) -> Dict[str, Any]:
        """Analyze individual provider performance"""
        
        context = self._format_provider_context(data, provider_id)
        
        prompt = f"""
        {self.get_system_prompt()}
        
        Provider Performance Analysis Request:
        {context}
        
        Please provide a comprehensive performance analysis including:
        1. Performance summary (scores, efficiency, quality)
        2. Comparison to network averages
        3. Strengths and areas for improvement
        4. Specific recommendations
        5. Risk assessment
        
        Format as a structured analysis with clear sections.
        """
        
        analysis = self.call_llm(prompt)
        
        return {
            "success": True,
            "analysis_type": "provider_performance",
            "provider_id": provider_id,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_network_summary(self, data: Dict) -> Dict[str, Any]:
        """Analyze overall network performance"""
        
        context = self._format_network_context(data)
        
        prompt = f"""
        {self.get_system_prompt()}
        
        Network Summary Analysis:
        {context}
        
        Provide a comprehensive network performance summary:
        1. Overall network health assessment
        2. Key performance indicators
        3. Top performers and concerning providers
        4. Geographic coverage analysis
        5. Priority improvement areas
        
        Focus on actionable insights for network management.
        """
        
        analysis = self.call_llm(prompt)
        
        return {
            "success": True,
            "analysis_type": "network_summary", 
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_provider_context(self, data: Dict, provider_id: str = None) -> str:
        """Format provider-specific context for LLM"""
        
        if provider_id and "providers" in data:
            # Find specific provider
            provider = next((p for p in data["providers"] if str(p.get("id")) == str(provider_id)), None)
            if provider:
                return f"""
                Provider Details:
                - Name: {provider.get('name')}
                - Organization: {provider.get('organization')}
                - Score: {provider.get('score')}/100
                - Efficiency Gain: {provider.get('efficiency_gain')}%
                - Quality Rating: {provider.get('quality_rating')}/5
                - Average Cost: ${provider.get('avg_cost')}
                - Patient Volume: {provider.get('patient_volume')}
                - Clinical Groups: {provider.get('clinical_groups')}
                - Network Status: {'In Network' if provider.get('in_network') else 'Out of Network'}
                
                Network Averages:
                - Average Score: {data.get('network_averages', {}).get('avg_score', 'N/A')}
                - Average Cost: ${data.get('network_averages', {}).get('avg_cost', 'N/A')}
                - Average Quality: {data.get('network_averages', {}).get('avg_quality', 'N/A')}
                """
        
        return "Provider data not available for analysis."
    
    def _format_network_context(self, data: Dict) -> str:
        """Format network-wide context for LLM"""
        
        return f"""
        Network Overview:
        - Total Providers: {data.get('total_providers', 0)}
        - In-Network Providers: {data.get('in_network_count', 0)}
        - Average Network Score: {data.get('avg_score', 0):.1f}
        - Average Cost: ${data.get('avg_cost', 0):,.0f}
        - Average Quality Rating: {data.get('avg_quality', 0):.1f}
        
        Performance Distribution:
        - Top Performers (Score >90): {data.get('top_performers_count', 0)}
        - Low Performers (Score <80): {data.get('low_performers_count', 0)}
        
        Geographic Coverage:
        - States Covered: {', '.join(data.get('states_covered', []))}
        - Total CBSAs: {data.get('total_cbsas', 0)}
        
        Clinical Specialties:
        - Primary Specialties: {', '.join(data.get('top_specialties', [])[:5])}
        """