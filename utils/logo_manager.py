"""
Logo Manager for Provider Network Management System
Integrates with brand themes to handle logo assets
"""

import os
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import streamlit as st
from PIL import Image
import base64

class LogoManager:
    """
    Manages logo assets and integrates them with brand themes
    """
    
    def __init__(self, logo_directory: str = "static/images/logos"):
        self.logo_dir = Path(logo_directory)
        self.logo_paths = self._discover_logos()
        
    def _discover_logos(self) -> Dict[str, Dict[str, Optional[str]]]:
        """Discover available logo files"""
        logos = {
            'humana': {
                'svg': None,
                'png': None,
                'white': None,
                'small': None
            },
            'onehome': {
                'svg': None,
                'png': None,
                'white': None,
                'small': None
            },
            'combined': {
                'png': None,
                'svg': None
            }
        }
        
        if not self.logo_dir.exists():
            print(f"⚠️ Logo directory not found: {self.logo_dir}")
            return logos
            
        # Search for logo files
        for file_path in self.logo_dir.glob("*"):
            filename = file_path.name.lower()
            
            # Humana logos
            if 'humana' in filename:
                if filename.endswith('.svg'):
                    logos['humana']['svg'] = str(file_path)
                elif filename.endswith('.png'):
                    if 'white' in filename:
                        logos['humana']['white'] = str(file_path)
                    elif 'small' in filename:
                        logos['humana']['small'] = str(file_path)
                    else:
                        logos['humana']['png'] = str(file_path)
            
            # OneHome logos
            elif 'onehome' in filename:
                if filename.endswith('.svg'):
                    logos['onehome']['svg'] = str(file_path)
                elif filename.endswith('.png'):
                    if 'white' in filename:
                        logos['onehome']['white'] = str(file_path)
                    elif 'small' in filename:
                        logos['onehome']['small'] = str(file_path)
                    else:
                        logos['onehome']['png'] = str(file_path)
            
            # Combined logos
            elif 'combined' in filename:
                if filename.endswith('.svg'):
                    logos['combined']['svg'] = str(file_path)
                elif filename.endswith('.png'):
                    logos['combined']['png'] = str(file_path)
        
        return logos
    
    def get_logo_path(self, 
                     company: str, 
                     format_type: str = 'png', 
                     theme_name: str = None) -> Optional[str]:
        """
        Get appropriate logo path based on company, format, and theme
        
        Args:
            company: 'humana', 'onehome', or 'combined'
            format_type: 'png', 'svg', 'white', 'small'
            theme_name: Theme name to determine if white logo needed
        """
        if company not in self.logo_paths:
            return None
            
        # Auto-select white logos for dark themes
        if theme_name and 'executive' in theme_name.lower():
            format_type = 'white'
        
        return self.logo_paths[company].get(format_type)
    
    def create_streamlit_logo_header(self, theme_name: str = 'partnership_balanced') -> None:
        """Create Streamlit header with both logos"""
        
        # Get logo paths
        humana_logo = self.get_logo_path('humana', 'png', theme_name)
        onehome_logo = self.get_logo_path('onehome', 'png', theme_name)
        
        # Create header layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if humana_logo and os.path.exists(humana_logo):
                st.image(humana_logo, width=150)
            else:
                st.markdown("**HUMANA**", help="Logo file not found")
        
        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='margin: 0; color: #00B5D8;'>Provider Network</h1>
                <h2 style='margin: 0; color: #7CB518;'>Management System</h2>
                <p style='margin: 5px 0; color: #6B7280;'>Humana & OneHome Partnership</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if onehome_logo and os.path.exists(onehome_logo):
                st.image(onehome_logo, width=150)
            else:
                st.markdown("**ONEHOME**", help="Logo file not found")
    
    def get_logo_for_pdf(self, company: str, theme_name: str = None) -> Optional[str]:
        """Get logo path suitable for PDF generation"""
        # Prefer PNG for PDF compatibility
        logo_path = self.get_logo_path(company, 'png', theme_name)
        
        if logo_path and os.path.exists(logo_path):
            return logo_path
        
        # Fallback to SVG if PNG not available
        svg_path = self.get_logo_path(company, 'svg', theme_name)
        if svg_path and os.path.exists(svg_path):
            return svg_path
            
        return None
    
    def validate_logos(self) -> Dict[str, Any]:
        """Validate that required logos are available"""
        validation = {
            'humana': {
                'available': False,
                'formats': [],
                'missing': []
            },
            'onehome': {
                'available': False,
                'formats': [],
                'missing': []
            },
            'status': 'incomplete'
        }
        
        required_formats = ['png', 'svg']
        
        for company in ['humana', 'onehome']:
            available_formats = []
            missing_formats = []
            
            for fmt in required_formats:
                logo_path = self.get_logo_path(company, fmt)
                if logo_path and os.path.exists(logo_path):
                    available_formats.append(fmt)
                else:
                    missing_formats.append(fmt)
            
            validation[company]['available'] = len(available_formats) > 0
            validation[company]['formats'] = available_formats
            validation[company]['missing'] = missing_formats
        
        # Overall status
        if validation['humana']['available'] and validation['onehome']['available']:
            validation['status'] = 'complete'
        elif validation['humana']['available'] or validation['onehome']['available']:
            validation['status'] = 'partial'
        else:
            validation['status'] = 'missing'
            
        return validation
    
    def setup_missing_logos(self) -> None:
        """Create placeholder logos for missing files"""
        # Ensure logo directory exists
        self.logo_dir.mkdir(parents=True, exist_ok=True)
        
        # Create placeholders for missing logos
        validation = self.validate_logos()
        
        for company in ['humana', 'onehome']:
            if not validation[company]['available']:
                self._create_placeholder_logo(company)
    
    def _create_placeholder_logo(self, company: str) -> None:
        """Create a placeholder logo"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Company-specific colors and text
            if company == 'humana':
                bg_color = '#7CB518'  # Humana green
                text = 'HUMANA'
            else:  # onehome
                bg_color = '#00B5D8'  # OneHome blue
                text = 'ONEHOME'
            
            # Create image
            img = Image.new('RGB', (300, 100), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (300 - text_width) // 2
            y = (100 - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, fill='white', font=font)
            
            # Save placeholder
            placeholder_path = self.logo_dir / f"{company}_logo.png"
            img.save(placeholder_path)
            
            print(f"✅ Created placeholder logo: {placeholder_path}")
            
        except Exception as e:
            print(f"❌ Could not create placeholder for {company}: {e}")
            # Create text file as last resort
            placeholder_path = self.logo_dir / f"{company}_logo.txt"
            with open(placeholder_path, 'w') as f:
                f.write(f"{text} LOGO PLACEHOLDER")