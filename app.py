"""
Main Streamlit Application with Logo Integration
Updated to use LogoManager and BrandThemes
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import your modules
from utils.logo_manager import LogoManager
from utils.brand_themes import BrandThemes
from utils.chart_generator import ChartGenerator
from agents.orchestrator import MultiAgentOrchestrator
from streamlit_integration.pdf_export import StreamlitPDFExporter

# Page configuration
st.set_page_config(
    page_title="Provider Network Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
@st.cache_resource
def initialize_managers():
    """Initialize logo manager and brand themes"""
    logo_manager = LogoManager()
    brand_themes = BrandThemes()
    
    # Validate logos and setup placeholders if needed
    validation = logo_manager.validate_logos()
    if validation['status'] != 'complete':
        st.warning("⚠️ Some logos are missing. Setting up placeholders...")
        logo_manager.setup_missing_logos()
    
    return logo_manager, brand_themes

# Initialize
logo_manager, brand_themes = initialize_managers()

# Sidebar theme selection
with st.sidebar:
    st.header("🎨 Appearance")
    
    # Theme selection
    available_themes = list(brand_themes.themes.keys())
    theme_names = [brand_themes.themes[t]['name'] for t in available_themes]
    
    selected_theme_name = st.selectbox(
        "Select Theme",
        theme_names,
        index=2,  # Default to partnership_balanced
        help="Choose the visual theme for the application"
    )
    
    # Get selected theme key
    selected_theme = available_themes[theme_names.index(selected_theme_name)]
    
    # Logo validation status
    validation = logo_manager.validate_logos()
    if validation['status'] == 'complete':
        st.success("✅ All logos loaded")
    elif validation['status'] == 'partial':
        st.warning("⚠️ Some logos missing")
    else:
        st.error("❌ Logos not found")
    
    # Show available logos
    with st.expander("Logo Status"):
        for company, info in validation.items():
            if company != 'status':
                if info['available']:
                    st.write(f"✅ {company.title()}: {', '.join(info['formats'])}")
                else:
                    st.write(f"❌ {company.title()}: Missing")

# Apply selected theme
theme_css = brand_themes.get_streamlit_theme(selected_theme)
st.markdown(theme_css, unsafe_allow_html=True)

# Main header with logos
logo_manager.create_streamlit_logo_header(selected_theme)

# Add a separator
st.markdown("---")

# Main application content
def main():
    """Main application logic"""
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard", 
        "📈 Analysis", 
        "💰 Cost Optimization", 
        "📄 Reports"
    ])
    
    with tab1:
        dashboard_page()
    
    with tab2:
        analysis_page()
    
    with tab3:
        cost_optimization_page()
    
    with tab4:
        reports_page()

def dashboard_page():
    """Dashboard page with themed components"""
    st.header("📊 Provider Network Dashboard")
    
    # Load sample data
    @st.cache_data
    def load_data():
        try:
            return pd.read_csv("data/providers.csv")
        except FileNotFoundError:
            # Create sample data if not found
            st.warning("Sample data not found. Creating mock data...")
            return create_sample_data()
    
    def create_sample_data():
        """Create sample data for demo"""
        import numpy as np
        from datetime import datetime, timedelta
        
        providers = ["AT&T Business", "Verizon Enterprise", "Comcast Business", "CenturyLink"]
        data = []
        
        for i in range(100):
            data.append({
                'provider_name': np.random.choice(providers),
                'latency_ms': np.random.normal(25, 5),
                'uptime_percentage': np.random.uniform(95, 99.9),
                'cost_per_gb': np.random.uniform(0.05, 0.25),
                'performance_score': np.random.uniform(70, 95)
            })
        
        return pd.DataFrame(data)
    
    data = load_data()
    
    # Key metrics with themed styling
    theme = brand_themes.get_theme(selected_theme)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Providers", 
            data['provider_name'].nunique() if 'provider_name' in data.columns else 0,
            delta="2 new this month"
        )
    
    with col2:
        avg_latency = data['latency_ms'].mean() if 'latency_ms' in data.columns else 0
        st.metric(
            "Avg Latency", 
            f"{avg_latency:.1f}ms",
            delta="-2.1ms"
        )
    
    with col3:
        avg_uptime = data['uptime_percentage'].mean() if 'uptime_percentage' in data.columns else 0
        st.metric(
            "Avg Uptime", 
            f"{avg_uptime:.1f}%",
            delta="0.3%"
        )
    
    with col4:
        avg_cost = data['cost_per_gb'].mean() if 'cost_per_gb' in data.columns else 0
        st.metric(
            "Avg Cost/GB", 
            f"${avg_cost:.3f}",
            delta="-$0.012"
        )
    
    # Charts with theme applied
    if len(data) > 0:
        st.subheader("📈 Performance Overview")
        
        try:
            chart_generator = ChartGenerator(theme=selected_theme)
            charts = chart_generator.create_performance_dashboard(data)
            
            if charts:
                for chart_name, chart in charts.items():
                    # Apply theme to chart
                    themed_chart = brand_themes.apply_theme_to_chart(chart, selected_theme)
                    st.plotly_chart(themed_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating charts: {e}")

def analysis_page():
    """Analysis page"""
    st.header("📈 Network Analysis")
    st.info("Advanced network analysis features coming soon...")

def cost_optimization_page():
    """Cost optimization page"""
    st.header("💰 Cost Optimization")
    st.info("Cost optimization analysis features coming soon...")

def reports_page():
    """Reports page with PDF export"""
    st.header("📄 Reports & Export")
    
    # Load data for reports
    try:
        data = pd.read_csv("data/providers.csv")
        
        # Mock analysis results
        analysis_results = {
            'summary': {
                'total_providers': data['provider_name'].nunique(),
                'avg_performance': data['performance_score'].mean() if 'performance_score' in data.columns else 85,
                'cost_savings_potential': 150000
            }
        }
        
        # Create charts for export
        chart_generator = ChartGenerator(theme=selected_theme)
        charts = chart_generator.create_performance_dashboard(data)
        
        # Apply theme to charts
        themed_charts = {}
        for name, chart in charts.items():
            themed_charts[name] = brand_themes.apply_theme_to_chart(chart, selected_theme)
        
        # PDF Export section
        exporter = StreamlitPDFExporter()
        exporter.create_download_section(
            charts=themed_charts,
            data=data,
            analysis_results=analysis_results,
            report_title=f"Provider Network Analysis - {selected_theme_name} Theme"
        )
        
    except Exception as e:
        st.error(f"Error loading data for reports: {e}")
        st.info("Please ensure sample data is available or run the setup process.")

# Sidebar additional features
with st.sidebar:
    st.markdown("---")
    st.header("🔧 Tools")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.experimental_rerun()
    
    if st.button("🧪 Test Logos"):
        validation = logo_manager.validate_logos()
        st.json(validation)
    
    if st.button("🎨 Test Themes"):
        st.write("Available themes:")
        for theme_key, theme_info in brand_themes.themes.items():
            st.write(f"- **{theme_info['name']}**: {theme_info['description']}")

# Run the main application
if __name__ == "__main__":
    main()