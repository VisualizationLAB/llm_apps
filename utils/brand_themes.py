"""
Brand Themes Configuration for OneHome & Humana Partnership
With safe imports for missing dependencies
"""

from typing import Dict, Any
import plotly.graph_objects as go

# Safe import for reportlab (optional for PDF features)
try:
    from reportlab.lib.colors import Color
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    # Create a mock Color class for when reportlab isn't available
    class Color:
        def __init__(self, r, g, b, alpha=1.0):
            self.r = r
            self.g = g
            self.b = b
            self.alpha = alpha

class BrandThemes:
    """
    Official brand themes for OneHome & Humana partnership
    Based on the provided logo images and brand guidelines
    """
    
    def __init__(self):
        # Extract colors from the provided logos
        self.colors = self._define_brand_colors()
        self.themes = self._create_themes()
        
    def _define_brand_colors(self) -> Dict[str, Dict[str, str]]:
        """Define official brand colors based on logo analysis"""
        return {
            'onehome': {
                'primary': '#00B5D8',      # Bright cyan blue from logo
                'secondary': '#0288A3',     # Darker blue variant
                'accent': '#B8E6F0',       # Light blue accent
                'white': '#FFFFFF',        # White text from logo
                'dark': '#1A365D',         # Dark blue for text
                'light_bg': '#E6F7FF',     # Very light blue background
                'gradient_start': '#00B5D8',
                'gradient_end': '#0288A3'
            },
            'humana': {
                'primary': '#7CB518',      # Bright green from logo
                'secondary': '#5A8A12',    # Darker green variant
                'accent': '#A6D157',       # Light green accent
                'white': '#FFFFFF',        # White background
                'dark': '#2D4A0E',         # Dark green for text
                'light_bg': '#F0F8E6',     # Very light green background
                'gradient_start': '#7CB518',
                'gradient_end': '#5A8A12'
            },
            'partnership': {
                # Combined partnership colors
                'primary_blue': '#00B5D8',    # OneHome blue
                'primary_green': '#7CB518',   # Humana green
                'secondary_blue': '#0288A3',  # Darker OneHome blue
                'secondary_green': '#5A8A12', # Darker Humana green
                'neutral_gray': '#6B7280',    # Professional gray
                'light_gray': '#F3F4F6',     # Light background
                'white': '#FFFFFF',
                'dark': '#1F2937'            # Dark text
            }
        }
    
    def _create_themes(self) -> Dict[str, Dict[str, Any]]:
        """Create comprehensive themes for different applications"""
        
        themes = {
            # OneHome focused theme
            'onehome_primary': {
                'name': 'OneHome Primary',
                'description': 'OneHome-focused theme with cyan blue colors',
                'colors': {
                    'background': self.colors['onehome']['white'],
                    'surface': self.colors['onehome']['light_bg'],
                    'primary': self.colors['onehome']['primary'],
                    'secondary': self.colors['onehome']['secondary'],
                    'accent': self.colors['onehome']['accent'],
                    'text_primary': self.colors['onehome']['dark'],
                    'text_secondary': self.colors['onehome']['secondary'],
                    'text_on_primary': self.colors['onehome']['white'],
                    'border': self.colors['onehome']['accent'],
                    'success': '#10B981',
                    'warning': '#F59E0B',
                    'error': '#EF4444',
                    'info': self.colors['onehome']['primary']
                },
                'gradients': {
                    'primary': f"linear-gradient(135deg, {self.colors['onehome']['gradient_start']}, {self.colors['onehome']['gradient_end']})",
                    'surface': f"linear-gradient(180deg, {self.colors['onehome']['white']}, {self.colors['onehome']['light_bg']})"
                },
                'chart_colors': [
                    self.colors['onehome']['primary'],
                    self.colors['onehome']['secondary'],
                    self.colors['onehome']['accent'],
                    '#00D2FF',  # Lighter blue
                    '#006B7D',  # Darker blue
                    '#4DD0E7',  # Medium blue
                    '#B3E5FC',  # Very light blue
                    '#01579B'   # Navy blue
                ]
            },
            
            # Humana focused theme  
            'humana_primary': {
                'name': 'Humana Primary',
                'description': 'Humana-focused theme with vibrant green colors',
                'colors': {
                    'background': self.colors['humana']['white'],
                    'surface': self.colors['humana']['light_bg'],
                    'primary': self.colors['humana']['primary'],
                    'secondary': self.colors['humana']['secondary'],
                    'accent': self.colors['humana']['accent'],
                    'text_primary': self.colors['humana']['dark'],
                    'text_secondary': self.colors['humana']['secondary'],
                    'text_on_primary': self.colors['humana']['white'],
                    'border': self.colors['humana']['accent'],
                    'success': self.colors['humana']['primary'],
                    'warning': '#F59E0B',
                    'error': '#EF4444',
                    'info': '#06B6D4'
                },
                'gradients': {
                    'primary': f"linear-gradient(135deg, {self.colors['humana']['gradient_start']}, {self.colors['humana']['gradient_end']})",
                    'surface': f"linear-gradient(180deg, {self.colors['humana']['white']}, {self.colors['humana']['light_bg']})"
                },
                'chart_colors': [
                    self.colors['humana']['primary'],
                    self.colors['humana']['secondary'],
                    self.colors['humana']['accent'],
                    '#8BC34A',  # Light green
                    '#4CAF50',  # Medium green
                    '#2E7D32',  # Dark green
                    '#C8E6C9',  # Very light green
                    '#1B5E20'   # Very dark green
                ]
            },
            
            # Partnership balanced theme
            'partnership_balanced': {
                'name': 'Partnership Balanced',
                'description': 'Balanced theme featuring both OneHome and Humana colors',
                'colors': {
                    'background': self.colors['partnership']['white'],
                    'surface': self.colors['partnership']['light_gray'],
                    'primary': self.colors['partnership']['primary_blue'],
                    'secondary': self.colors['partnership']['primary_green'],
                    'accent': self.colors['partnership']['neutral_gray'],
                    'text_primary': self.colors['partnership']['dark'],
                    'text_secondary': self.colors['partnership']['neutral_gray'],
                    'text_on_primary': self.colors['partnership']['white'],
                    'border': '#D1D5DB',
                    'success': self.colors['partnership']['primary_green'],
                    'warning': '#F59E0B',
                    'error': '#EF4444',
                    'info': self.colors['partnership']['primary_blue']
                },
                'gradients': {
                    'primary': f"linear-gradient(135deg, {self.colors['partnership']['primary_blue']}, {self.colors['partnership']['primary_green']})",
                    'surface': f"linear-gradient(180deg, {self.colors['partnership']['white']}, {self.colors['partnership']['light_gray']})"
                },
                'chart_colors': [
                    self.colors['partnership']['primary_blue'],
                    self.colors['partnership']['primary_green'],
                    self.colors['partnership']['secondary_blue'],
                    self.colors['partnership']['secondary_green'],
                    '#60A5FA',  # Light blue
                    '#A3E635',  # Light green
                    '#1E40AF',  # Dark blue
                    '#15803D'   # Dark green
                ]
            },
            
            # Professional report theme
            'professional_report': {
                'name': 'Professional Report',
                'description': 'Clean professional theme for reports and presentations',
                'colors': {
                    'background': '#FFFFFF',
                    'surface': '#F8FAFC',
                    'primary': self.colors['partnership']['primary_blue'],
                    'secondary': self.colors['partnership']['primary_green'],
                    'accent': '#64748B',
                    'text_primary': '#1E293B',
                    'text_secondary': '#475569',
                    'text_on_primary': '#FFFFFF',
                    'border': '#E2E8F0',
                    'success': '#059669',
                    'warning': '#D97706',
                    'error': '#DC2626',
                    'info': '#0284C7'
                },
                'gradients': {
                    'primary': 'linear-gradient(135deg, #F8FAFC, #E2E8F0)',
                    'surface': 'linear-gradient(180deg, #FFFFFF, #F8FAFC)'
                },
                'chart_colors': [
                    '#00B5D8',  # OneHome blue
                    '#7CB518',  # Humana green
                    '#64748B',  # Professional gray
                    '#0284C7',  # Info blue
                    '#059669',  # Success green
                    '#D97706',  # Warning orange
                    '#DC2626',  # Error red
                    '#7C3AED'   # Purple accent
                ]
            },
            
            # Executive dashboard theme
            'executive_dashboard': {
                'name': 'Executive Dashboard',
                'description': 'High-contrast theme for executive presentations',
                'colors': {
                    'background': '#0F172A',
                    'surface': '#1E293B',
                    'primary': '#00B5D8',
                    'secondary': '#7CB518',
                    'accent': '#F59E0B',
                    'text_primary': '#F8FAFC',
                    'text_secondary': '#CBD5E1',
                    'text_on_primary': '#0F172A',
                    'border': '#334155',
                    'success': '#10B981',
                    'warning': '#F59E0B',
                    'error': '#EF4444',
                    'info': '#06B6D4'
                },
                'gradients': {
                    'primary': 'linear-gradient(135deg, #0F172A, #1E293B)',
                    'surface': 'linear-gradient(180deg, #1E293B, #334155)'
                },
                'chart_colors': [
                    '#00B5D8',  # OneHome blue
                    '#7CB518',  # Humana green
                    '#F59E0B',  # Golden yellow
                    '#10B981',  # Emerald
                    '#8B5CF6',  # Purple
                    '#F97316',  # Orange
                    '#EC4899',  # Pink
                    '#06B6D4'   # Cyan
                ]
            }
        }
        
        return themes
    
    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get a specific theme configuration"""
        return self.themes.get(theme_name, self.themes['partnership_balanced'])
    
    def get_plotly_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get Plotly-specific theme configuration"""
        theme = self.get_theme(theme_name)
        
        return {
            'layout': {
                'template': 'plotly_white',
                'colorway': theme['chart_colors'],
                'paper_bgcolor': theme['colors']['background'],
                'plot_bgcolor': theme['colors']['surface'],
                'font': {
                    'family': 'Arial, sans-serif',
                    'size': 12,
                    'color': theme['colors']['text_primary']
                },
                'title': {
                    'font': {
                        'family': 'Arial, sans-serif',
                        'size': 16,
                        'color': theme['colors']['text_primary']
                    }
                },
                'xaxis': {
                    'gridcolor': theme['colors']['border'],
                    'linecolor': theme['colors']['border'],
                    'tickcolor': theme['colors']['text_secondary']
                },
                'yaxis': {
                    'gridcolor': theme['colors']['border'],
                    'linecolor': theme['colors']['border'],
                    'tickcolor': theme['colors']['text_secondary']
                }
            }
        }
    
    def get_streamlit_theme(self, theme_name: str) -> str:
        """Get Streamlit CSS for theme application"""
        theme = self.get_theme(theme_name)
        
        css = f"""
        <style>
        /* Main app styling */
        .stApp {{
            background: {theme['colors']['background']};
            color: {theme['colors']['text_primary']};
        }}
        
        /* Header styling */
        .stApp > header {{
            background: {theme['gradients']['primary']};
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background: {theme['colors']['surface']};
        }}
        
        /* Metrics styling */
        .metric-container {{
            background: {theme['colors']['surface']};
            border: 1px solid {theme['colors']['border']};
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: {theme['colors']['primary']};
            color: {theme['colors']['text_on_primary']};
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }}
        
        .stButton > button:hover {{
            background: {theme['colors']['secondary']};
        }}
        
        /* Success/Info boxes */
        .stSuccess {{
            background: {theme['colors']['success']}20;
            border-left: 4px solid {theme['colors']['success']};
        }}
        
        .stInfo {{
            background: {theme['colors']['info']}20;
            border-left: 4px solid {theme['colors']['info']};
        }}
        
        /* Chart containers */
        .stPlotlyChart {{
            background: {theme['colors']['surface']};
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        /* Partnership header */
        .partnership-header {{
            background: {theme['gradients']['primary']};
            color: {theme['colors']['text_on_primary']};
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        /* Logo containers */
        .logo-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: {theme['colors']['surface']};
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        </style>
        """
        
        return css
    
    def get_pdf_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get PDF/ReportLab theme configuration (only if reportlab available)"""
        if not REPORTLAB_AVAILABLE:
            print("⚠️ ReportLab not available. PDF features will be limited.")
            return {}
            
        theme = self.get_theme(theme_name)
        
        # Convert hex colors to ReportLab Color objects
        def hex_to_color(hex_color: str) -> Color:
            hex_color = hex_color.lstrip('#')
            return Color(
                int(hex_color[0:2], 16) / 255.0,
                int(hex_color[2:4], 16) / 255.0,
                int(hex_color[4:6], 16) / 255.0
            )
        
        return {
            'background_color': hex_to_color(theme['colors']['background']),
            'surface_color': hex_to_color(theme['colors']['surface']),
            'primary_color': hex_to_color(theme['colors']['primary']),
            'secondary_color': hex_to_color(theme['colors']['secondary']),
            'accent_color': hex_to_color(theme['colors']['accent']),
            'text_color': hex_to_color(theme['colors']['text_primary']),
            'text_secondary_color': hex_to_color(theme['colors']['text_secondary']),
            'border_color': hex_to_color(theme['colors']['border']),
            'chart_colors': [hex_to_color(color) for color in theme['chart_colors']],
            'fonts': {
                'title': 'Helvetica-Bold',
                'heading': 'Helvetica-Bold',
                'body': 'Helvetica',
                'caption': 'Helvetica-Oblique'
            }
        }
    
    def apply_theme_to_chart(self, fig: go.Figure, theme_name: str) -> go.Figure:
        """Apply theme to a Plotly figure"""
        theme_config = self.get_plotly_theme(theme_name)
        theme = self.get_theme(theme_name)
        
        fig.update_layout(
            template='plotly_white',
            colorway=theme['chart_colors'],
            paper_bgcolor=theme['colors']['background'],
            plot_bgcolor=theme['colors']['surface'],
            font=theme_config['layout']['font'],
            title_font=theme_config['layout']['title']['font'],
            xaxis=theme_config['layout']['xaxis'],
            yaxis=theme_config['layout']['yaxis']
        )
        
        return fig

# Check availability function
def check_dependencies():
    """Check which dependencies are available"""
    dependencies = {
        'reportlab': REPORTLAB_AVAILABLE,
        'plotly': True,  # Already imported successfully
    }
    
    try:
        from PIL import Image
        dependencies['pillow'] = True
    except ImportError:
        dependencies['pillow'] = False
    
    try:
        import yaml
        dependencies['pyyaml'] = True
    except ImportError:
        dependencies['pyyaml'] = False
    
    return dependencies

# Usage examples and theme testing
def demo_theme_usage():
    """Demonstrate how to use the brand themes"""
    
    # Check dependencies first
    deps = check_dependencies()
    print("Dependency Status:")
    for dep, available in deps.items():
        status = "✅" if available else "❌"
        print(f"  {status} {dep}")
    
    if not deps['reportlab']:
        print("\n⚠️ ReportLab not available. Install with: pip install reportlab")
    
    # Initialize themes
    brand_themes = BrandThemes()
    
    # Get OneHome theme
    onehome_theme = brand_themes.get_theme('onehome_primary')
    print("\nOneHome Primary Colors:")
    for key, value in onehome_theme['colors'].items():
        print(f"  {key}: {value}")
    
    return brand_themes

# Export for easy import
__all__ = ['BrandThemes', 'demo_theme_usage', 'check_dependencies', 'REPORTLAB_AVAILABLE']