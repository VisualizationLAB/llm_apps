
# agents/report_generator_agent.py
"""
Report Generation Agent - Creates comprehensive reports and documents
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent

class ReportGeneratorAgent(BaseAgent):
    """Agent specialized in generating comprehensive network reports"""
    
    def get_system_prompt(self) -> str:
        return """
        You are a Healthcare Network Reporting Specialist with expertise in creating:
        - Executive summaries and board presentations
        - Detailed provider performance reports
        - Regulatory compliance documentation
        - Strategic analysis reports
        - Network optimization recommendations
        
        Your reports should be:
        1. Clear and accessible to non-technical audiences
        2. Well-structured with logical flow
        3. Data-driven with specific metrics
        4. Action-oriented with clear recommendations
        5. Professional and suitable for executive review
        
        Use simple language while maintaining professional tone.
        Include executive summaries, key findings, and actionable recommendations.
        """
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process report generation requests"""
        
        report_type = request.get("report_type", "network_summary")
        audience = request.get("audience", "network_manager")
        data = request.get("data", {})
        focus_areas = request.get("focus_areas", [])
        
        try:
            if report_type == "executive_summary":
                return self._generate_executive_summary(data, audience)
            elif report_type == "provider_diagnostics":
                return self._generate_provider_diagnostics_report(data)
            elif report_type == "cost_optimization":
                return self._generate_cost_optimization_report(data)
            elif report_type == "quality_analysis":
                return self._generate_quality_analysis_report(data)
            elif report_type == "network_adequacy":
                return self._generate_network_adequacy_report(data)
            else:
                return self._generate_comprehensive_report(data, focus_areas)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate report"
            }
    
    def _generate_executive_summary(self, data: Dict, audience: str) -> Dict[str, Any]:
        """Generate executive summary report"""
        
        context = self._format_executive_context(data)
        
        prompt = f"""
        {self.get_system_prompt()}
        
        Generate an Executive Summary for {audience} with the following network data:
        {context}
        
        Structure the report as follows:
        
        # EXECUTIVE SUMMARY - Provider Network Performance
        
        ## Key Highlights
        - [3-4 most important findings]
        
        ## Network Performance Overview
        - [Overall health assessment]
        - [Key metrics summary]
        
        ## Strategic Priorities
        - [Top 3 priority actions]
        
        ## Financial Impact
        - [Cost savings opportunities]
        - [ROI projections]
        
        ## Risk Assessment
        - [Key risks and mitigation strategies]
        
        ## Recommendations
        - [Specific, actionable next steps]
        
        Keep each section concise (2-3 sentences) and focus on business impact.
        Use clear, non-technical language suitable for executives.
        """
        
        report = self.call_llm(prompt, max_tokens=1200)
        
        return {
            "success": True,
            "report_type": "executive_summary",
            "audience": audience,
            "report_content": report,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_provider_diagnostics_report(self, data: Dict) -> Dict[str, Any]:
        """Generate detailed provider diagnostics report"""
        
        context = self._format_provider_diagnostics_context(data)
        
        prompt = f"""
        {self.get_system_prompt()}
        
        Generate a comprehensive Provider Diagnostics Report:
        {context}
        
        Create a detailed report with these sections:
        
        # PROVIDER NETWORK DIAGNOSTICS REPORT
        
        ## Executive Summary
        - [Brief overview of network health]
        
        ## Network Performance Analysis
        - [Overall performance metrics and trends]
        
        ## Provider Performance Breakdown
        - [Top performers analysis]
        - [Underperforming providers analysis]
        - [Performance distribution insights]
        
        ## Quality vs Cost Analysis
        - [Quality-cost positioning analysis]
        - [Value-based performance insights]
        
        ## Geographic Coverage Assessment
        - [Coverage strengths and gaps]
        - [Market opportunity analysis]
        
        ## Clinical Specialty Analysis
        - [Specialty-specific performance]
        - [Capacity and utilization insights]
        
        ## Risk Assessment
        - [Provider-specific risks]
        - [Network stability concerns]
        
        ## Strategic Recommendations
        - [Specific improvement actions]
        - [Provider management strategies]
        - [Network optimization opportunities]
        
        Use data-driven insights and provide specific, actionable recommendations.
        Include relevant metrics and comparisons throughout.
        """
        
        report = self.call_llm(prompt, max_tokens=1800)
        
        return {
            "success": True,
            "report_type": "provider_diagnostics",
            "report_content": report,
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_executive_context(self, data: Dict) -> str:
        """Format context for executive summary"""
        
        return f"""
        Network Overview:
        - Total Providers: {data.get('total_providers', 0)}
        - In-Network: {data.get('in_network_count', 0)} ({data.get('network_percentage', 0):.1f}%)
        - Average Quality Score: {data.get('avg_score', 0):.1f}/100
        - Average Cost: ${data.get('avg_cost', 0):,.0f}
        
        Performance Highlights:
        - Top Performers: {data.get('top_performers_count', 0)} providers scoring >90
        - Improvement Needed: {data.get('low_performers_count', 0)} providers scoring <80
        - Cost Savings Opportunities: {data.get('cost_savings_potential', 'TBD')}
        
        Geographic Coverage:
        - States: {len(data.get('states_covered', []))}
        - Markets (CBSAs): {data.get('total_cbsas', 0)}
        - Coverage Gaps: {data.get('coverage_gaps_count', 0)}
        """
    
    def _format_provider_diagnostics_context(self, data: Dict) -> str:
        """Format context for provider diagnostics report"""
        
        top_performers = data.get('top_performers', [])[:3]
        bottom_performers = data.get('bottom_performers', [])[:3]
        high_cost = data.get('high_cost_providers', [])[:3]
        
        context = f"""
        Comprehensive Network Data:
        
        Network Statistics:
        - Total Providers: {data.get('total_providers', 0)}
        - Average Score: {data.get('avg_score', 0):.1f}/100
        - Average Cost: ${data.get('avg_cost', 0):,.0f}
        - Average Quality: {data.get('avg_quality', 0):.1f}/5
        
        Top Performers:
        """
        
        for provider in top_performers:
            context += f"- {provider.get('name')}: Score {provider.get('score')}, Cost ${provider.get('avg_cost')}\n"
        
        context += "\nUnderperforming Providers:\n"
        for provider in bottom_performers:
            context += f"- {provider.get('name')}: Score {provider.get('score')}, Quality {provider.get('quality_rating')}\n"
        
        context += "\nHigh-Cost Providers:\n"
        for provider in high_cost:
            context += f"- {provider.get('name')}: Cost ${provider.get('avg_cost')}, Score {provider.get('score')}\n"
        
        context += f"""
        
        Geographic Distribution:
        - States: {', '.join(data.get('states_covered', []))}
        - Coverage Gaps: {data.get('coverage_gaps_count', 0)} areas
        
        Clinical Specialties:
        - Primary Specialties: {', '.join(data.get('top_specialties', [])[:5])}
        """
        
        return context
