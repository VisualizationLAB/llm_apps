# utils/pdf_generator.py
"""
PDF Report Generator for Provider Network Management
Creates professional PDF reports with charts and analysis
"""
# Add these imports at the top
from .logo_manager import LogoManager
from .brand_themes import BrandThemes

class PDFReportGenerator:
    def __init__(self, theme_name='professional_report'):
        self.theme_name = theme_name
        self.logo_manager = LogoManager()
        self.brand_themes = BrandThemes()
        # ... rest of your existing init code
    
    def _add_logo_header(self):
        """Updated method to use LogoManager"""
        elements = []
        
        # Get logo paths using LogoManager
        humana_logo = self.logo_manager.get_logo_for_pdf('humana', self.theme_name)
        onehome_logo = self.logo_manager.get_logo_for_pdf('onehome', self.theme_name)
        
        # Create logo table (rest of your existing code)
        # But now use the paths from LogoManager
        # ... existing implementation
        
        return elements
        
import io
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

# PDF generation libraries
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.linecharts import HorizontalLineChart
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.warning("PDF generation requires: pip install reportlab")

class NetworkPDFGenerator:
    """Generate comprehensive PDF reports for network management"""
    
    def __init__(self):
        if not PDF_AVAILABLE:
            raise ImportError("PDF generation requires reportlab. Install with: pip install reportlab")
        
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for PDF formatting"""
        
        # Custom title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f77b4'),
            alignment=1  # Center alignment
        ))
        
        # Custom heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50'),
            borderWidth=0,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=5
        ))
        
        # Custom subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#34495e')
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=20,
            rightIndent=20,
            backColor=colors.HexColor('#f8f9fa'),
            borderWidth=1,
            borderColor=colors.HexColor('#dee2e6'),
            borderPadding=10
        ))
        
        # Recommendation style
        self.styles.add(ParagraphStyle(
            name='Recommendation',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=15,
            bulletIndent=10,
            bulletFontName='Symbol'
        ))
    
    def generate_comprehensive_report(self, data: Dict[str, Any], 
                                    report_content: str,
                                    charts_data: Dict[str, Any] = None) -> bytes:
        """Generate comprehensive network management PDF report"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build report content
        story = []
        
        # Title page
        story.extend(self._create_title_page(data))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(data, report_content))
        story.append(PageBreak())
        
        # Network overview
        story.extend(self._create_network_overview(data))
        
        # Provider performance analysis
        story.extend(self._create_provider_analysis(data))
        story.append(PageBreak())
        
        # Cost analysis
        story.extend(self._create_cost_analysis(data))
        
        # Quality analysis
        story.extend(self._create_quality_analysis(data))
        story.append(PageBreak())
        
        # Recommendations
        story.extend(self._create_recommendations_section(report_content))
        
        # Charts and visualizations
        if charts_data:
            story.append(PageBreak())
            story.extend(self._create_charts_section(charts_data))
        
        # Appendices
        story.append(PageBreak())
        story.extend(self._create_appendices(data))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_title_page(self, data: Dict[str, Any]) -> List:
        """Create PDF title page"""
        
        story = []
        
        # Main title
        title = Paragraph("Provider Network Management Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 30))
        
        # Subtitle with date
        subtitle = Paragraph(
            f"Network Performance Analysis<br/>Generated on {datetime.now().strftime('%B %d, %Y')}",
            self.styles['Heading2']
        )
        story.append(subtitle)
        story.append(Spacer(1, 50))
        
        # Key metrics summary table
        metrics_data = [
            ['Metric', 'Value', 'Status'],
            ['Total Providers', f"{data.get('total_providers', 0):,}", '✓'],
            ['In-Network Providers', f"{data.get('in_network_count', 0):,}", '✓'],
            ['Network Coverage', f"{data.get('network_percentage', 0):.1f}%", 
             '✓' if data.get('network_percentage', 0) > 80 else '⚠'],
            ['Average Quality Score', f"{data.get('avg_score', 0):.1f}/100", 
             '✓' if data.get('avg_score', 0) > 85 else '⚠'],
            ['Average Cost', f"${data.get('avg_cost', 0):,.0f}", '✓']
        ]
        
        table = Table(metrics_data, colWidths=[2*inch, 1.5*inch, 0.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Report scope
        scope_text = f"""
        <b>Report Scope:</b><br/>
        This comprehensive report analyzes the performance of {data.get('total_providers', 0)} 
        healthcare providers across {len(data.get('states_covered', []))} states, 
        covering {len(data.get('clinical_specialties', []))} clinical specialties.
        The analysis includes quality metrics, cost efficiency, geographic coverage, 
        and strategic recommendations for network optimization.
        """
        
        scope = Paragraph(scope_text, self.styles['Normal'])
        story.append(scope)
        
        return story
    
    def _create_executive_summary(self, data: Dict[str, Any], report_content: str) -> List:
        """Create executive summary section"""
        
        story = []
        
        # Section title
        title = Paragraph("Executive Summary", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Extract executive summary from report content
        exec_summary = self._extract_section_from_report(report_content, "executive summary", "key highlights")
        
        if exec_summary:
            summary_para = Paragraph(exec_summary, self.styles['ExecutiveSummary'])
            story.append(summary_para)
        else:
            # Generate default executive summary
            default_summary = f"""
            <b>Network Performance Overview:</b><br/>
            Our provider network consists of {data.get('total_providers', 0)} providers with 
            {data.get('in_network_count', 0)} currently in-network ({data.get('network_percentage', 0):.1f}% coverage).
            The network maintains an average quality score of {data.get('avg_score', 0):.1f}/100 
            with an average cost of ${data.get('avg_cost', 0):,.0f} per episode.
            <br/><br/>
            <b>Key Findings:</b><br/>
            • {data.get('top_performers_count', 0)} providers demonstrate exceptional performance (>90 score)<br/>
            • {data.get('low_performers_count', 0)} providers require performance improvement (<80 score)<br/>
            • Geographic coverage spans {len(data.get('states_covered', []))} states with 
            {data.get('coverage_gaps_count', 0)} identified coverage gaps<br/>
            • Estimated cost optimization potential of 15-20% through strategic network changes
            """
            
            summary_para = Paragraph(default_summary, self.styles['ExecutiveSummary'])
            story.append(summary_para)
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_network_overview(self, data: Dict[str, Any]) -> List:
        """Create network overview section"""
        
        story = []
        
        # Section title
        title = Paragraph("Network Overview", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Provider distribution table
        overview_data = [
            ['Category', 'Count', 'Percentage'],
            ['Total Providers', f"{data.get('total_providers', 0):,}", '100%'],
            ['In-Network', f"{data.get('in_network_count', 0):,}", 
             f"{data.get('network_percentage', 0):.1f}%"],
            ['Out-of-Network', f"{data.get('out_of_network_count', 0):,}", 
             f"{100 - data.get('network_percentage', 0):.1f}%"],
            ['High Performers (Score >90)', f"{data.get('top_performers_count', 0):,}", 
             f"{(data.get('top_performers_count', 0) / max(data.get('total_providers', 1), 1)) * 100:.1f}%"],
            ['Low Performers (Score <80)', f"{data.get('low_performers_count', 0):,}", 
             f"{(data.get('low_performers_count', 0) / max(data.get('total_providers', 1), 1)) * 100:.1f}%"]
        ]
        
        table = Table(overview_data, colWidths=[2.5*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Geographic coverage
        geo_title = Paragraph("Geographic Coverage", self.styles['CustomSubHeading'])
        story.append(geo_title)
        
        geo_text = f"""
        The network spans <b>{len(data.get('states_covered', []))}</b> states: 
        {', '.join(data.get('states_covered', [])[:10])}
        {'...' if len(data.get('states_covered', [])) > 10 else ''}
        <br/><br/>
        Coverage includes <b>{data.get('total_cbsas', 0)}</b> Core Based Statistical Areas (CBSAs) 
        with {data.get('coverage_gaps_count', 0)} identified coverage gaps requiring attention.
        """
        
        geo_para = Paragraph(geo_text, self.styles['Normal'])
        story.append(geo_para)
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_provider_analysis(self, data: Dict[str, Any]) -> List:
        """Create provider performance analysis section"""
        
        story = []
        
        # Section title
        title = Paragraph("Provider Performance Analysis", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Top performers
        top_title = Paragraph("Top Performing Providers", self.styles['CustomSubHeading'])
        story.append(top_title)
        
        top_performers = data.get('top_performers', [])[:5]
        if top_performers:
            top_data = [['Provider', 'Organization', 'Score', 'Quality', 'Cost']]
            for provider in top_performers:
                top_data.append([
                    provider.get('name', 'N/A'),
                    provider.get('organization', 'N/A')[:25] + ('...' if len(provider.get('organization', '')) > 25 else ''),
                    f"{provider.get('score', 0)}",
                    f"{provider.get('quality_rating', 0):.1f}/5",
                    f"${provider.get('avg_cost', 0):,.0f}"
                ])
            
            top_table = Table(top_data, colWidths=[1.8*inch, 1.8*inch, 0.8*inch, 0.8*inch, 1*inch])
            top_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(top_table)
        
        story.append(Spacer(1, 15))
        
        # Underperforming providers
        bottom_title = Paragraph("Providers Requiring Attention", self.styles['CustomSubHeading'])
        story.append(bottom_title)
        
        bottom_performers = data.get('bottom_performers', [])[:5]
        if bottom_performers:
            bottom_data = [['Provider', 'Organization', 'Score', 'Quality', 'Issues']]
            for provider in bottom_performers:
                issues = []
                if provider.get('score', 0) < 80:
                    issues.append('Low Score')
                if provider.get('quality_rating', 0) < 4.0:
                    issues.append('Quality')
                if provider.get('avg_cost', 0) > data.get('avg_cost', 0) * 1.2:
                    issues.append('High Cost')
                
                bottom_data.append([
                    provider.get('name', 'N/A'),
                    provider.get('organization', 'N/A')[:25] + ('...' if len(provider.get('organization', '')) > 25 else ''),
                    f"{provider.get('score', 0)}",
                    f"{provider.get('quality_rating', 0):.1f}/5",
                    ', '.join(issues) if issues else 'Review Needed'
                ])
            
            bottom_table = Table(bottom_data, colWidths=[1.8*inch, 1.8*inch, 0.8*inch, 0.8*inch, 1*inch])
            bottom_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(bottom_table)
        
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_cost_analysis(self, data: Dict[str, Any]) -> List:
        """Create cost analysis section"""
        
        story = []
        
        # Section title
        title = Paragraph("Cost Analysis", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Cost summary
        cost_summary = f"""
        <b>Network Cost Profile:</b><br/>
        • Average Cost per Episode: <b>${data.get('avg_cost', 0):,.0f}</b><br/>
        • Cost Range: ${data.get('min_cost', 0):,.0f} - ${data.get('max_cost', 0):,.0f}<br/>
        • High-Cost Providers (>120% of average): <b>{data.get('high_cost_count', 0)}</b><br/>
        • Cost-Efficient Providers (<80% of average): <b>{data.get('low_cost_count', 0)}</b>
        """
        
        cost_para = Paragraph(cost_summary, self.styles['Normal'])
        story.append(cost_para)
        story.append(Spacer(1, 15))
        
        # Cost optimization opportunities
        optimization_title = Paragraph("Cost Optimization Opportunities", self.styles['CustomSubHeading'])
        story.append(optimization_title)
        
        high_cost_providers = data.get('high_cost_providers', [])[:3]
        if high_cost_providers:
            opt_text = "<b>High-Cost Provider Analysis:</b><br/>"
            for i, provider in enumerate(high_cost_providers, 1):
                potential_savings = (provider.get('avg_cost', 0) - data.get('avg_cost', 0)) * provider.get('patient_volume', 0)
                opt_text += f"{i}. <b>{provider.get('name')}</b> - Cost: ${provider.get('avg_cost', 0):,.0f} "
                opt_text += f"(Potential Savings: ${potential_savings:,.0f})<br/>"
            
            opt_para = Paragraph(opt_text, self.styles['Normal'])
            story.append(opt_para)
        
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_quality_analysis(self, data: Dict[str, Any]) -> List:
        """Create quality analysis section"""
        
        story = []
        
        # Section title
        title = Paragraph("Quality Analysis", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Quality metrics summary
        quality_summary = f"""
        <b>Network Quality Profile:</b><br/>
        • Average Quality Score: <b>{data.get('avg_score', 0):.1f}/100</b><br/>
        • Average Quality Rating: <b>{data.get('avg_quality', 0):.1f}/5</b><br/>
        • Providers Exceeding 90 Score: <b>{data.get('top_performers_count', 0)}</b><br/>
        • Providers Below 80 Score: <b>{data.get('low_performers_count', 0)}</b><br/>
        • Quality Improvement Target: <b>Achieve 87+ average network score</b>
        """
        
        quality_para = Paragraph(quality_summary, self.styles['Normal'])
        story.append(quality_para)
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_recommendations_section(self, report_content: str) -> List:
        """Create recommendations section"""
        
        story = []
        
        # Section title
        title = Paragraph("Strategic Recommendations", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Extract recommendations from report content
        recommendations = self._extract_section_from_report(report_content, "recommendations", "conclusion")
        
        if recommendations:
            rec_para = Paragraph(recommendations, self.styles['Normal'])
            story.append(rec_para)
        else:
            # Default recommendations
            default_recs = """
            <b>Priority Actions:</b><br/>
            1. <b>Performance Improvement:</b> Implement quality improvement programs for providers scoring below 80<br/>
            2. <b>Cost Optimization:</b> Renegotiate contracts with high-cost, low-performing providers<br/>
            3. <b>Network Expansion:</b> Recruit high-quality providers in coverage gap areas<br/>
            4. <b>Contract Management:</b> Establish performance-based incentives for top performers<br/>
            5. <b>Monitoring:</b> Implement quarterly performance reviews and benchmarking
            """
            
            rec_para = Paragraph(default_recs, self.styles['Normal'])
            story.append(rec_para)
        
        return story
    
    def _create_charts_section(self, charts_data: Dict[str, Any]) -> List:
        """Create charts and visualizations section"""
        
        story = []
        
        # Section title
        title = Paragraph("Data Visualizations", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Note about charts
        chart_note = Paragraph(
            "The following section contains key data visualizations and charts "
            "supporting the analysis presented in this report.",
            self.styles['Normal']
        )
        story.append(chart_note)
        story.append(Spacer(1, 20))
        
        # Placeholder for chart images (would be generated from plotly figures)
        chart_placeholder = Paragraph(
            "<b>Chart Placeholder:</b> Network Performance Dashboard<br/>"
            "• Provider Score Distribution<br/>"
            "• Quality vs Cost Analysis<br/>"
            "• Geographic Coverage Map<br/>"
            "• Performance Trends",
            self.styles['Normal']
        )
        story.append(chart_placeholder)
        
        return story
    
    def _create_appendices(self, data: Dict[str, Any]) -> List:
        """Create appendices section"""
        
        story = []
        
        # Section title
        title = Paragraph("Appendices", self.styles['CustomHeading'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Methodology
        methodology_title = Paragraph("A. Methodology", self.styles['CustomSubHeading'])
        story.append(methodology_title)
        
        methodology_text = """
        This analysis is based on comprehensive provider performance data including:
        • Quality scores derived from patient outcomes and satisfaction metrics
        • Cost efficiency calculations based on episode-level cost data
        • Geographic coverage analysis using CBSA-level mapping
        • Performance benchmarking against industry standards
        """
        
        methodology_para = Paragraph(methodology_text, self.styles['Normal'])
        story.append(methodology_para)
        story.append(Spacer(1, 15))
        
        # Data sources
        sources_title = Paragraph("B. Data Sources", self.styles['CustomSubHeading'])
        story.append(sources_title)
        
        sources_text = """
        • Provider credentialing and demographic data
        • Claims and utilization data
        • Quality metrics and patient satisfaction scores
        • Contract terms and payment data
        • Geographic and market intelligence data
        """
        
        sources_para = Paragraph(sources_text, self.styles['Normal'])
        story.append(sources_para)
        
        return story
    
    def _extract_section_from_report(self, report_content: str, 
                                   start_marker: str, end_marker: str) -> str:
        """Extract specific section from report content"""
        
        if not report_content:
            return ""
        
        lines = report_content.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            line_lower = line.lower()
            
            if start_marker.lower() in line_lower:
                in_section = True
                continue
            
            if end_marker.lower() in line_lower and in_section:
                break
            
            if in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines).strip()
    
    def create_chart_image(self, fig, width: int = 600, height: int = 400) -> Image:
        """Convert Plotly figure to ReportLab Image"""
        
        # Convert plotly figure to image bytes
        img_bytes = fig.to_image(format="png", width=width, height=height)
        
        # Create ReportLab Image
        img_buffer = io.BytesIO(img_bytes)
        img = Image(img_buffer, width=width*0.75, height=height*0.75)  # Scale for PDF
        
        return img

# utils/chart_generator.py
"""
Chart Generator for PDF Reports
Creates professional charts for network analysis
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List

class NetworkChartGenerator:
    """Generate charts for network analysis reports"""
    
    def __init__(self):
        # Define consistent color schemes
        self.color_scheme = {
            'primary': '#3498db',
            'secondary': '#2ecc71', 
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#9b59b6',
            'dark': '#2c3e50'
        }
    
    def create_provider_score_distribution(self, providers_df: pd.DataFrame) -> go.Figure:
        """Create provider score distribution chart"""
        
        fig = go.Figure()
        
        # Add histogram
        fig.add_trace(go.Histogram(
            x=providers_df['score'],
            nbinsx=20,
            name='Provider Distribution',
            marker_color=self.color_scheme['primary'],
            opacity=0.7
        ))
        
        # Add mean line
        mean_score = providers_df['score'].mean()
        fig.add_vline(
            x=mean_score,
            line_dash="dash",
            line_color=self.color_scheme['danger'],
            annotation_text=f"Network Average: {mean_score:.1f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            title="Provider Score Distribution",
            xaxis_title="Quality Score",
            yaxis_title="Number of Providers",
            showlegend=False,
            template="plotly_white"
        )
        
        return fig
    
    def create_quality_cost_quadrant(self, providers_df: pd.DataFrame) -> go.Figure:
        """Create quality vs cost quadrant analysis"""
        
        avg_cost = providers_df['avg_cost'].mean()
        avg_quality = providers_df['quality_rating'].mean()
        
        # Determine quadrants
        def get_quadrant_color(row):
            if row['quality_rating'] >= avg_quality and row['avg_cost'] <= avg_cost:
                return 'Star Performers'  # High quality, low cost
            elif row['quality_rating'] >= avg_quality and row['avg_cost'] > avg_cost:
                return 'Premium Providers'  # High quality, high cost
            elif row['quality_rating'] < avg_quality and row['avg_cost'] <= avg_cost:
                return 'Budget Options'  # Low quality, low cost
            else:
                return 'Question Marks'  # Low quality, high cost
        
        providers_df['quadrant'] = providers_df.apply(get_quadrant_color, axis=1)
        
        fig = px.scatter(
            providers_df,
            x='avg_cost',
            y='quality_rating',
            color='quadrant',
            size='patient_volume',
            hover_data=['name', 'organization', 'score'],
            color_discrete_map={
                'Star Performers': self.color_scheme['secondary'],
                'Premium Providers': self.color_scheme['primary'],
                'Budget Options': self.color_scheme['warning'],
                'Question Marks': self.color_scheme['danger']
            },
            title="Quality vs Cost Analysis"
        )
        
        # Add quadrant lines
        fig.add_hline(y=avg_quality, line_dash="dash", line_color="gray")
        fig.add_vline(x=avg_cost, line_dash="dash", line_color="gray")
        
        # Add quadrant labels
        fig.add_annotation(x=avg_cost*0.7, y=avg_quality*1.1, text="STAR<br>PERFORMERS", 
                          showarrow=False, font=dict(color="green", size=12))
        fig.add_annotation(x=avg_cost*1.3, y=avg_quality*1.1, text="PREMIUM<br>PROVIDERS", 
                          showarrow=False, font=dict(color="blue", size=12))
        fig.add_annotation(x=avg_cost*0.7, y=avg_quality*0.9, text="BUDGET<br>OPTIONS", 
                          showarrow=False, font=dict(color="orange", size=12))
        fig.add_annotation(x=avg_cost*1.3, y=avg_quality*0.9, text="QUESTION<br>MARKS", 
                          showarrow=False, font=dict(color="red", size=12))
        
        fig.update_layout(
            xaxis_title="Average Cost ($)",
            yaxis_title="Quality Rating",
            template="plotly_white"
        )
        
        return fig
    
    def create_geographic_coverage_chart(self, providers_df: pd.DataFrame) -> go.Figure:
        """Create geographic coverage analysis chart"""
        
        # State-level analysis
        state_summary = providers_df.groupby('state').agg({
            'score': 'mean',
            'avg_cost': 'mean',
            'patient_volume': 'sum',
            'in_network': 'sum'
        }).reset_index()
        
        state_summary['total_providers'] = providers_df.groupby('state').size().values
        state_summary['network_percentage'] = (state_summary['in_network'] / state_summary['total_providers']) * 100
        
        fig = px.bar(
            state_summary,
            x='state',
            y='network_percentage',
            color='score',
            title="Network Coverage by State",
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            xaxis_title="State",
            yaxis_title="Network Coverage (%)",
            template="plotly_white"
        )
        
        return fig
    
    def create_performance_trends_chart(self, providers_df: pd.DataFrame) -> go.Figure:
        """Create performance trends analysis"""
        
        # Create efficiency vs score scatter
        fig = px.scatter(
            providers_df,
            x='efficiency_gain',
            y='score',
            size='patient_volume',
            color='in_network',
            hover_data=['name', 'organization'],
            title="Provider Performance: Efficiency vs Quality Score",
            color_discrete_map={True: self.color_scheme['secondary'], False: self.color_scheme['warning']}
        )
        
        fig.update_layout(
            xaxis_title="Efficiency Gain (%)",
            yaxis_title="Quality Score",
            template="plotly_white"
        )
        
        return fig
    
    def create_cost_analysis_chart(self, providers_df: pd.DataFrame) -> go.Figure:
        """Create cost analysis breakdown chart"""
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Cost Distribution', 'Cost by Specialty', 
                          'Volume vs Cost', 'Network Status Comparison'),
            specs=[[{"type": "histogram"}, {"type": "box"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Cost distribution
        fig.add_trace(
            go.Histogram(x=providers_df['avg_cost'], name='Cost Distribution', 
                        marker_color=self.color_scheme['primary']),
            row=1, col=1
        )
        
        # Cost by clinical groups (simplified)
        clinical_groups = []
        costs_by_group = []
        for _, row in providers_df.iterrows():
            if isinstance(row['clinical_groups_list'], list):
                for group in row['clinical_groups_list']:
                    clinical_groups.append(group)
                    costs_by_group.append(row['avg_cost'])
        
        if clinical_groups:
            fig.add_trace(
                go.Box(y=costs_by_group, name='Cost by Specialty',
                      marker_color=self.color_scheme['secondary']),
                row=1, col=2
            )
        
        # Volume vs Cost
        fig.add_trace(
            go.Scatter(x=providers_df['patient_volume'], y=providers_df['avg_cost'],
                      mode='markers', name='Volume vs Cost',
                      marker=dict(color=self.color_scheme['info'])),
            row=2, col=1
        )
        
        # Network status comparison
        network_comparison = providers_df.groupby('in_network')['avg_cost'].mean()
        fig.add_trace(
            go.Bar(x=['Out of Network', 'In Network'], y=network_comparison.values,
                  name='Network Comparison', marker_color=[self.color_scheme['warning'], self.color_scheme['secondary']]),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Comprehensive Cost Analysis",
            template="plotly_white"
        )
        
        return fig

# streamlit_integration/pdf_export.py
"""
Streamlit integration for PDF export functionality
"""

import streamlit as st
import base64
from datetime import datetime
from typing import Dict, Any
from ..utils.pdf_generator import NetworkPDFGenerator, PDF_AVAILABLE
from ..utils.chart_generator import NetworkChartGenerator

def add_pdf_export_functionality():
    """Add PDF export functionality to Streamlit app"""
    
    if not PDF_AVAILABLE:
        st.error("PDF generation not available. Install with: pip install reportlab")
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📄 Generate Reports")
    
    # Report type selection
    report_type = st.sidebar.selectbox(
        "Report Type",
        ["Executive Summary", "Comprehensive Analysis", "Provider Diagnostics", "Cost Optimization"]
    )
    
    # Report customization
    with st.sidebar.expander("📋 Report Options"):
        include_charts = st.checkbox("Include Visualizations", value=True)
        include_recommendations = st.checkbox("Include AI Recommendations", value=True)
        audience = st.selectbox("Target Audience", ["Network Manager", "Executive Leadership", "Board of Directors"])
    
    # Generate report button
    if st.sidebar.button("📥 Generate PDF Report", type="primary"):
        
        # Load current data
        df = load_data()
        
        with st.spinner("🤖 Generating comprehensive report..."):
            
            # Get AI analysis if requested
            report_content = ""
            if include_recommendations:
                report_content = generate_ai_report_content(df, report_type, audience)
            
            # Prepare data for PDF
            pdf_data = prepare_pdf_data(df)
            
            # Generate charts if requested
            charts_data = None
            if include_charts:
                charts_data = generate_pdf_charts(df)
            
            # Generate PDF
            pdf_generator = NetworkPDFGenerator()
            pdf_bytes = pdf_generator.generate_comprehensive_report(
                pdf_data, report_content, charts_data
            )
            
            # Create download link
            create_pdf_download_link(pdf_bytes, report_type)
        
        st.sidebar.success("✅ Report generated successfully!")

def generate_ai_report_content(df: pd.DataFrame, report_type: str, audience: str) -> str:
    """Generate AI-powered report content using agents"""
    
    try:
        # Initialize orchestrator if available
        if 'orchestrator' in st.session_state:
            orchestrator = st.session_state.orchestrator
        else:
            from ..agents.orchestrator import AgentOrchestrator
            from databricks.sdk import WorkspaceClient
            
            workspace_client = WorkspaceClient()
            orchestrator = AgentOrchestrator(workspace_client)
            st.session_state.orchestrator = orchestrator
        
        # Prepare context
        context = prepare_network_context(df)
        
        # Generate report based on type
        if report_type == "Executive Summary":
            query = f"Generate an executive summary report for {audience} covering our network performance, key insights, and strategic recommendations."
        elif report_type == "Comprehensive Analysis":
            query = f"Create a comprehensive network analysis report for {audience} including performance metrics, cost analysis, quality assessment, and detailed recommendations."
        elif report_type == "Provider Diagnostics":
            query = f"Generate a detailed provider diagnostics report for {audience} analyzing individual provider performance, identifying top performers and improvement opportunities."
        elif report_type == "Cost Optimization":
            query = f"Create a cost optimization analysis report for {audience} identifying cost savings opportunities, efficiency improvements, and financial recommendations."
        else:
            query = f"Generate a comprehensive network management report for {audience}."
        
        # Get AI response
        response = orchestrator.route_request(query, context)
        
        if response.get("success"):
            if response.get("multi_agent_response"):
                return response.get("integrated_response", "")
            else:
                return response.get("analysis", "") or response.get("strategies", "") or response.get("report_content", "")
        else:
            return "AI analysis temporarily unavailable. Report generated with standard analysis."
    
    except Exception as e:
        st.error(f"Error generating AI content: {e}")
        return "AI analysis unavailable. Report generated with standard metrics."

def prepare_pdf_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data structure for PDF generation"""
    
    # Basic network metrics
    total_providers = len(df)
    in_network_count = len(df[df['in_network'] == True])
    network_percentage = (in_network_count / total_providers) * 100 if total_providers > 0 else 0
    
    # Performance metrics
    avg_score = df['score'].mean()
    avg_cost = df['avg_cost'].mean()
    avg_quality = df['quality_rating'].mean()
    avg_efficiency = df['efficiency_gain'].mean()
    
    # Top and bottom performers
    top_performers = df.nlargest(5, 'score').to_dict('records')
    bottom_performers = df.nsmallest(5, 'score').to_dict('records')
    high_cost_providers = df.nlargest(5, 'avg_cost').to_dict('records')
    
    # Geographic analysis
    states_covered = df['state'].unique().tolist()
    cbsas = df['cbsa'].nunique()
    
    # Clinical specialties
    all_specialties = []
    for specialties in df['clinical_groups_list'].dropna():
        if isinstance(specialties, list):
            all_specialties.extend(specialties)
    
    specialty_counts = pd.Series(all_specialties).value_counts()
    top_specialties = specialty_counts.head(10).index.tolist()
    
    # Performance categories
    top_performers_count = len(df[df['score'] > 90])
    low_performers_count = len(df[df['score'] < 80])
    high_cost_count = len(df[df['avg_cost'] > avg_cost * 1.2])
    low_cost_count = len(df[df['avg_cost'] < avg_cost * 0.8])
    
    return {
        'total_providers': total_providers,
        'in_network_count': in_network_count,
        'out_of_network_count': total_providers - in_network_count,
        'network_percentage': network_percentage,
        'avg_score': avg_score,
        'avg_cost': avg_cost,
        'avg_quality': avg_quality,
        'avg_efficiency': avg_efficiency,
        'min_cost': df['avg_cost'].min(),
        'max_cost': df['avg_cost'].max(),
        'top_performers': top_performers,
        'bottom_performers': bottom_performers,
        'high_cost_providers': high_cost_providers,
        'top_performers_count': top_performers_count,
        'low_performers_count': low_performers_count,
        'high_cost_count': high_cost_count,
        'low_cost_count': low_cost_count,
        'states_covered': states_covered,
        'total_cbsas': cbsas,
        'coverage_gaps_count': 0,  # Would be calculated based on requirements
        'clinical_specialties': specialty_counts.to_dict(),
        'top_specialties': top_specialties
    }

def generate_pdf_charts(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate charts for PDF inclusion"""
    
    chart_generator = NetworkChartGenerator()
    
    charts = {
        'score_distribution': chart_generator.create_provider_score_distribution(df),
        'quality_cost_quadrant': chart_generator.create_quality_cost_quadrant(df),
        'geographic_coverage': chart_generator.create_geographic_coverage_chart(df),
        'performance_trends': chart_generator.create_performance_trends_chart(df),
        'cost_analysis': chart_generator.create_cost_analysis_chart(df)
    }
    
    return charts

def prepare_network_context(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare network context for AI agents"""
    
    # Convert DataFrame to agent-friendly format
    providers_list = []
    for _, row in df.iterrows():
        provider = {
            'id': row['id'],
            'name': row['name'],
            'organization': row['organization'],
            'score': row['score'],
            'efficiency_gain': row['efficiency_gain'],
            'avg_cost': row['avg_cost'],
            'quality_rating': row['quality_rating'],
            'patient_volume': row['patient_volume'],
            'in_network': row['in_network'],
            'state': row['state'],
            'cbsa': row['cbsa'],
            'clinical_groups': row.get('clinical_groups', ''),
            'clinical_groups_list': row.get('clinical_groups_list', [])
        }
        providers_list.append(provider)
    
    # Calculate network statistics
    in_network_providers = [p for p in providers_list if p['in_network']]
    out_network_providers = [p for p in providers_list if not p['in_network']]
    
    network_stats = {
        'avg_score': df['score'].mean(),
        'avg_cost': df['avg_cost'].mean(),
        'avg_quality': df['quality_rating'].mean(),
        'total_volume': df['patient_volume'].sum()
    }
    
    # Top and bottom performers
    top_performers = sorted(providers_list, key=lambda x: x['score'], reverse=True)[:5]
    bottom_performers = sorted(providers_list, key=lambda x: x['score'])[:5]
    high_cost_providers = sorted(providers_list, key=lambda x: x['avg_cost'], reverse=True)[:5]
    low_performers = [p for p in providers_list if p['score'] < 80]
    
    return {
        'providers': providers_list,
        'network_stats': network_stats,
        'total_providers': len(providers_list),
        'in_network_count': len(in_network_providers),
        'out_of_network_count': len(out_network_providers),
        'network_percentage': (len(in_network_providers) / len(providers_list)) * 100,
        'avg_score': network_stats['avg_score'],
        'avg_cost': network_stats['avg_cost'],
        'avg_quality': network_stats['avg_quality'],
        'top_performers': top_performers,
        'bottom_performers': bottom_performers,
        'high_cost_providers': high_cost_providers,
        'low_performers': low_performers,
        'top_performers_count': len([p for p in providers_list if p['score'] > 90]),
        'low_performers_count': len(low_performers),
        'states_covered': list(set(p['state'] for p in providers_list)),
        'total_cbsas': len(set(p['cbsa'] for p in providers_list)),
        'coverage_gaps_count': 0  # Would be calculated based on requirements
    }

def create_pdf_download_link(pdf_bytes: bytes, report_type: str):
    """Create download link for PDF report"""
    
    # Encode PDF for download
    b64_pdf = base64.b64encode(pdf_bytes).decode()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"network_report_{report_type.lower().replace(' ', '_')}_{timestamp}.pdf"
    
    # Create download link
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}">📥 Download {report_type} Report</a>'
    
    st.sidebar.markdown(href, unsafe_allow_html=True)
    
    # Also show in main area
    st.success("✅ Report generated successfully!")
    st.markdown(f"### 📄 {report_type} Report Ready")
    st.markdown(href, unsafe_allow_html=True)
    
    # Report summary
    st.info(f"""
    **Report Details:**
    - Type: {report_type}
    - Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
    - Format: PDF
    - Size: {len(pdf_bytes) / 1024:.1f} KB
    """)

# Add to requirements.txt:
"""
# PDF Generation Requirements
reportlab>=4.0.0
Pillow>=9.0.0
"""