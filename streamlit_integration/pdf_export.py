"""
PDF Export Module for Streamlit Integration

This module provides PDF export functionality specifically designed for Streamlit apps,
handling chart exports, data tables, and complete report generation with professional
formatting and interactive download capabilities.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any, Union
import io
import base64
from datetime import datetime
import tempfile
import os
from pathlib import Path

# Import the main PDF generator
import sys
sys.path.append('..')
from utils.pdf_generator import PDFReportGenerator

class StreamlitPDFExporter:
    """
    Streamlit-specific PDF export functionality with enhanced UI integration
    """
    
    def __init__(self):
        """Initialize the Streamlit PDF exporter"""
        self.pdf_generator = PDFReportGenerator()
        self.temp_files = []  # Track temporary files for cleanup
    
    def create_download_section(self, 
                              charts: Dict[str, go.Figure], 
                              data: pd.DataFrame,
                              analysis_results: Dict[str, Any],
                              report_title: str = "Provider Network Analysis Report") -> None:
        """
        Create a Streamlit section for PDF download with options
        
        Args:
            charts: Dictionary of chart objects
            data: Source data DataFrame
            analysis_results: Analysis results from agents
            report_title: Title for the report
        """
        st.subheader("📄 Export Report")
        
        # Report configuration options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_executive_summary = st.checkbox("Executive Summary", value=True)
            include_charts = st.checkbox("Include Charts", value=True)
            include_data_tables = st.checkbox("Data Tables", value=True)
        
        with col2:
            include_recommendations = st.checkbox("Recommendations", value=True)
            include_appendix = st.checkbox("Technical Appendix", value=False)
            chart_quality = st.selectbox("Chart Quality", ["High", "Medium", "Standard"], index=0)
        
        with col3:
            report_format = st.selectbox("Report Format", ["Professional", "Executive", "Technical"])
            page_orientation = st.selectbox("Page Orientation", ["Portrait", "Landscape"])
            include_branding = st.checkbox("Include Company Branding", value=True)
        
        # Advanced options in expandable section
        with st.expander("Advanced Export Options"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                custom_title = st.text_input("Custom Report Title", value=report_title)
                author_name = st.text_input("Author Name", value="Network Analysis Team")
                department = st.text_input("Department", value="IT Operations")
            
            with col_adv2:
                include_timestamp = st.checkbox("Include Timestamp", value=True)
                include_data_source = st.checkbox("Include Data Sources", value=True)
                password_protect = st.checkbox("Password Protection", value=False)
                
                if password_protect:
                    pdf_password = st.text_input("PDF Password", type="password")
                else:
                    pdf_password = None
        
        # Generate and download buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔍 Preview Report", type="secondary", use_container_width=True):
                self._show_report_preview(charts, data, analysis_results, custom_title)
        
        with col_btn2:
            if st.button("📊 Quick Export", type="primary", use_container_width=True):
                self._quick_export(charts, data, analysis_results, custom_title)
        
        with col_btn3:
            if st.button("⚙️ Custom Export", type="secondary", use_container_width=True):
                self._custom_export(
                    charts=charts,
                    data=data,
                    analysis_results=analysis_results,
                    report_config={
                        'title': custom_title,
                        'author': author_name,
                        'department': department,
                        'format': report_format,
                        'orientation': page_orientation,
                        'include_executive_summary': include_executive_summary,
                        'include_charts': include_charts,
                        'include_data_tables': include_data_tables,
                        'include_recommendations': include_recommendations,
                        'include_appendix': include_appendix,
                        'chart_quality': chart_quality,
                        'include_branding': include_branding,
                        'include_timestamp': include_timestamp,
                        'include_data_source': include_data_source,
                        'password': pdf_password
                    }
                )
    
    def _show_report_preview(self, 
                           charts: Dict[str, go.Figure], 
                           data: pd.DataFrame,
                           analysis_results: Dict[str, Any],
                           title: str) -> None:
        """Show a preview of the report structure"""
        with st.expander("📋 Report Preview", expanded=True):
            st.markdown("### Report Structure")
            
            preview_structure = [
                "📊 Executive Summary",
                "📈 Performance Analysis",
                "💰 Cost Optimization Results", 
                "🔍 Provider Comparison",
                "📉 Trend Analysis",
                "🎯 Recommendations",
                "📋 Data Tables",
                "🔧 Technical Appendix"
            ]
            
            for item in preview_structure:
                st.markdown(f"- {item}")
            
            # Show sample charts preview
            st.markdown("### Sample Chart Preview")
            if charts:
                sample_chart_key = list(charts.keys())[0]
                st.plotly_chart(charts[sample_chart_key], use_container_width=True)
            
            # Show data preview
            st.markdown("### Data Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(data))
            with col2:
                st.metric("Providers", data['provider_name'].nunique() if 'provider_name' in data.columns else 'N/A')
            with col3:
                st.metric("Metrics Analyzed", len(analysis_results))
            with col4:
                st.metric("Charts Generated", len(charts))
    
    def _quick_export(self, 
                     charts: Dict[str, go.Figure], 
                     data: pd.DataFrame,
                     analysis_results: Dict[str, Any],
                     title: str) -> None:
        """Generate and download a quick standard report"""
        try:
            with st.spinner("Generating PDF report..."):
                # Generate PDF with standard settings
                pdf_buffer = self.pdf_generator.generate_complete_report(
                    charts=charts,
                    data=data,
                    analysis_results=analysis_results,
                    report_title=title,
                    include_executive_summary=True,
                    include_recommendations=True
                )
                
                # Create download
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"provider_network_report_{timestamp}.pdf"
                
                st.download_button(
                    label="⬇️ Download Report",
                    data=pdf_buffer.getvalue(),
                    file_name=filename,
                    mime="application/pdf",
                    key=f"download_{timestamp}",
                    use_container_width=True
                )
                
                st.success("✅ Report generated successfully!")
                
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            st.exception(e)
    
    def _custom_export(self, 
                      charts: Dict[str, go.Figure], 
                      data: pd.DataFrame,
                      analysis_results: Dict[str, Any],
                      report_config: Dict[str, Any]) -> None:
        """Generate and download a custom configured report"""
        try:
            with st.spinner("Generating custom PDF report..."):
                # Generate PDF with custom settings
                pdf_buffer = self.pdf_generator.generate_complete_report(
                    charts=charts,
                    data=data,
                    analysis_results=analysis_results,
                    report_title=report_config['title'],
                    author=report_config.get('author'),
                    department=report_config.get('department'),
                    include_executive_summary=report_config['include_executive_summary'],
                    include_charts=report_config['include_charts'],
                    include_data_tables=report_config['include_data_tables'],
                    include_recommendations=report_config['include_recommendations'],
                    include_appendix=report_config['include_appendix'],
                    chart_quality=report_config['chart_quality'].lower(),
                    orientation=report_config['orientation'].lower(),
                    password=report_config.get('password')
                )
                
                # Create download
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{report_config['title'].lower().replace(' ', '_')}_{timestamp}.pdf"
                
                st.download_button(
                    label="⬇️ Download Custom Report",
                    data=pdf_buffer.getvalue(),
                    file_name=filename,
                    mime="application/pdf",
                    key=f"custom_download_{timestamp}",
                    use_container_width=True
                )
                
                st.success("✅ Custom report generated successfully!")
                
                # Show generation details
                with st.expander("📋 Report Details"):
                    st.json({
                        "Title": report_config['title'],
                        "Author": report_config.get('author', 'N/A'),
                        "Format": report_config['format'],
                        "Charts Included": len(charts),
                        "Data Records": len(data),
                        "Timestamp": datetime.now().isoformat()
                    })
                
        except Exception as e:
            st.error(f"❌ Error generating custom report: {str(e)}")
            st.exception(e)
    
    def export_individual_chart(self, chart: go.Figure, chart_name: str) -> None:
        """Export individual chart as PDF"""
        st.subheader(f"Export: {chart_name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            format_option = st.selectbox(
                "Export Format", 
                ["PDF", "PNG", "JPEG", "SVG"],
                key=f"format_{chart_name}"
            )
            
        with col2:
            quality = st.selectbox(
                "Quality", 
                ["High", "Medium", "Standard"],
                key=f"quality_{chart_name}"
            )
        
        if st.button(f"Export {chart_name}", key=f"export_{chart_name}"):
            try:
                if format_option == "PDF":
                    # Export as PDF
                    pdf_buffer = self.pdf_generator.create_chart_pdf(chart, chart_name)
                    
                    st.download_button(
                        label=f"⬇️ Download {chart_name}.pdf",
                        data=pdf_buffer.getvalue(),
                        file_name=f"{chart_name.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    # Export as image
                    img_buffer = self._export_chart_as_image(chart, format_option.lower(), quality)
                    
                    st.download_button(
                        label=f"⬇️ Download {chart_name}.{format_option.lower()}",
                        data=img_buffer,
                        file_name=f"{chart_name.lower().replace(' ', '_')}.{format_option.lower()}",
                        mime=f"image/{format_option.lower()}"
                    )
                
                st.success(f"✅ {chart_name} exported successfully!")
                
            except Exception as e:
                st.error(f"❌ Error exporting {chart_name}: {str(e)}")
    
    def _export_chart_as_image(self, chart: go.Figure, format: str, quality: str) -> bytes:
        """Export chart as image format"""
        # Set dimensions based on quality
        dimensions = {
            "high": (1920, 1080),
            "medium": (1280, 720),
            "standard": (800, 600)
        }
        
        width, height = dimensions[quality.lower()]
        
        # Export chart
        img_bytes = chart.to_image(
            format=format,
            width=width,
            height=height,
            scale=2 if quality.lower() == "high" else 1
        )
        
        return img_bytes
    
    def create_batch_export_section(self, charts: Dict[str, go.Figure]) -> None:
        """Create section for batch exporting multiple charts"""
        st.subheader("📊 Batch Chart Export")
        
        # Chart selection
        selected_charts = st.multiselect(
            "Select charts to export:",
            options=list(charts.keys()),
            default=list(charts.keys())
        )
        
        if selected_charts:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                batch_format = st.selectbox("Export Format", ["PDF", "PNG", "JPEG"])
            
            with col2:
                batch_quality = st.selectbox("Quality", ["High", "Medium", "Standard"])
            
            with col3:
                combine_pdf = st.checkbox("Combine into single PDF", value=True)
            
            if st.button("📦 Export Selected Charts"):
                try:
                    if batch_format == "PDF" and combine_pdf:
                        # Create combined PDF
                        selected_chart_objects = {name: charts[name] for name in selected_charts}
                        pdf_buffer = self.pdf_generator.create_charts_pdf(selected_chart_objects)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        st.download_button(
                            label="⬇️ Download Combined Charts PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"charts_export_{timestamp}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        # Create individual exports
                        self._create_individual_exports(selected_charts, charts, batch_format, batch_quality)
                    
                    st.success(f"✅ Successfully exported {len(selected_charts)} charts!")
                    
                except Exception as e:
                    st.error(f"❌ Error in batch export: {str(e)}")
    
    def _create_individual_exports(self, 
                                  selected_charts: List[str], 
                                  charts: Dict[str, go.Figure],
                                  format: str, 
                                  quality: str) -> None:
        """Create individual file exports for selected charts"""
        for chart_name in selected_charts:
            try:
                if format == "PDF":
                    pdf_buffer = self.pdf_generator.create_chart_pdf(charts[chart_name], chart_name)
                    
                    st.download_button(
                        label=f"⬇️ {chart_name}.pdf",
                        data=pdf_buffer.getvalue(),
                        file_name=f"{chart_name.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"individual_pdf_{chart_name}"
                    )
                else:
                    img_buffer = self._export_chart_as_image(charts[chart_name], format.lower(), quality)
                    
                    st.download_button(
                        label=f"⬇️ {chart_name}.{format.lower()}",
                        data=img_buffer,
                        file_name=f"{chart_name.lower().replace(' ', '_')}.{format.lower()}",
                        mime=f"image/{format.lower()}",
                        key=f"individual_img_{chart_name}"
                    )
            except Exception as e:
                st.warning(f"⚠️ Could not export {chart_name}: {str(e)}")
    
    def create_data_export_section(self, data: pd.DataFrame, analysis_results: Dict[str, Any]) -> None:
        """Create section for exporting data and analysis results"""
        st.subheader("📈 Data Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Raw Data Export**")
            
            data_format = st.selectbox("Data Format", ["CSV", "Excel", "JSON"])
            include_index = st.checkbox("Include Index", value=False)
            
            if st.button("Export Data"):
                try:
                    if data_format == "CSV":
                        csv_buffer = io.StringIO()
                        data.to_csv(csv_buffer, index=include_index)
                        
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv_buffer.getvalue(),
                            file_name=f"provider_data_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    
                    elif data_format == "Excel":
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                            data.to_excel(writer, sheet_name='Provider Data', index=include_index)
                        
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_buffer.getvalue(),
                            file_name=f"provider_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    elif data_format == "JSON":
                        json_str = data.to_json(orient='records', indent=2)
                        
                        st.download_button(
                            label="⬇️ Download JSON",
                            data=json_str,
                            file_name=f"provider_data_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )
                    
                    st.success("✅ Data exported successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error exporting data: {str(e)}")
        
        with col2:
            st.markdown("**🔍 Analysis Results Export**")
            
            include_raw_results = st.checkbox("Include Raw Results", value=True)
            include_summary = st.checkbox("Include Summary", value=True)
            
            if st.button("Export Analysis"):
                try:
                    # Prepare analysis export
                    export_data = {}
                    
                    if include_summary:
                        export_data['summary'] = {
                            'timestamp': datetime.now().isoformat(),
                            'total_providers': data['provider_name'].nunique() if 'provider_name' in data.columns else 0,
                            'total_records': len(data),
                            'analysis_modules': list(analysis_results.keys())
                        }
                    
                    if include_raw_results:
                        export_data['results'] = analysis_results
                    
                    # Export as JSON
                    import json
                    json_str = json.dumps(export_data, indent=2, default=str)
                    
                    st.download_button(
                        label="⬇️ Download Analysis Results",
                        data=json_str,
                        file_name=f"analysis_results_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                    
                    st.success("✅ Analysis results exported successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error exporting analysis: {str(e)}")
    
    def create_scheduled_export_section(self) -> None:
        """Create section for scheduling regular exports"""
        st.subheader("⏰ Scheduled Exports")
        st.info("🚧 Scheduled export functionality coming soon!")
        
        # Future implementation placeholder
        with st.expander("Configure Scheduled Exports"):
            col1, col2 = st.columns(2)
            
            with col1:
                schedule_frequency = st.selectbox(
                    "Export Frequency", 
                    ["Daily", "Weekly", "Monthly", "Quarterly"]
                )
                
                export_time = st.time_input("Export Time")
                
            with col2:
                email_recipients = st.text_area(
                    "Email Recipients (one per line)",
                    placeholder="user1@company.com\nuser2@company.com"
                )
                
                include_charts = st.checkbox("Include Charts in Scheduled Export", value=True)
            
            if st.button("Save Schedule Configuration", disabled=True):
                st.info("This feature will be available in a future update.")
    
    def cleanup_temp_files(self) -> None:
        """Clean up any temporary files created during export"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass  # Ignore cleanup errors
        
        self.temp_files.clear()

# Utility functions for Streamlit PDF export
def create_export_sidebar(charts: Dict[str, go.Figure], 
                         data: pd.DataFrame, 
                         analysis_results: Dict[str, Any]) -> None:
    """Create export options in Streamlit sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.subheader("📄 Quick Export")
        
        exporter = StreamlitPDFExporter()
        
        if st.button("🚀 Quick PDF Export", use_container_width=True):
            exporter._quick_export(
                charts=charts,
                data=data,
                analysis_results=analysis_results,
                title="Provider Network Analysis Report"
            )
        
        st.markdown("---")
        
        # Quick chart export
        if charts:
            st.subheader("📊 Quick Chart Export")
            selected_chart = st.selectbox("Select Chart", list(charts.keys()))
            
            if st.button("Export Chart as PDF", use_container_width=True):
                exporter.export_individual_chart(charts[selected_chart], selected_chart)

def display_export_metrics(data: pd.DataFrame, charts: Dict[str, go.Figure]) -> None:
    """Display export-related metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Data Records", len(data))
    
    with col2:
        st.metric("Charts Available", len(charts))
    
    with col3:
        providers_count = data['provider_name'].nunique() if 'provider_name' in data.columns else 0
        st.metric("Providers", providers_count)
    
    with col4:
        est_size = len(data) * len(charts) * 0.1  # Rough estimate in MB
        st.metric("Est. PDF Size", f"{est_size:.1f} MB")