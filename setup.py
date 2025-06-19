"""
Setup configuration for Provider Network Management System

This setup file configures the package for installation, including dependencies,
entry points, and metadata for the provider network management application.
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Read version from __init__.py
def get_version():
    """Extract version from package __init__.py"""
    version_file = Path(__file__).parent / "provider_network_mgmt" / "__init__.py"
    if version_file.exists():
        with open(version_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    return "0.1.0"

# Read long description from README
def get_long_description():
    """Read long description from README file"""
    readme_file = Path(__file__).parent / "README.md"
    if readme_file.exists():
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "Provider Network Management System for analyzing and optimizing network provider performance and costs."

# Read requirements from requirements.txt
def get_requirements():
    """Parse requirements from requirements.txt"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    requirements = []
    
    if requirements_file.exists():
        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    # Handle git+https and other complex requirements
                    if 'git+' in line or line.startswith('-e'):
                        continue  # Skip git dependencies for now
                    requirements.append(line)
    
    return requirements

# Core dependencies (minimal for basic functionality)
CORE_REQUIREMENTS = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "plotly>=5.15.0",
    "streamlit>=1.28.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "scikit-learn>=1.3.0",
    "requests>=2.28.0",
    "reportlab>=4.0.0",
    "openpyxl>=3.1.0",
    "xlsxwriter>=3.1.0",
]

# Optional dependencies for enhanced functionality
OPTIONAL_REQUIREMENTS = {
    'databricks': [
        'databricks-cli>=0.18.0',
        'databricks-connect>=13.0.0',
        'pyspark>=3.4.0',
        'delta-spark>=2.4.0',
    ],
    'ml': [
        'scikit-learn>=1.3.0',
        'xgboost>=1.7.0',
        'lightgbm>=4.0.0',
        'networkx>=3.0',
        'scipy>=1.10.0',
    ],
    'advanced_viz': [
        'bokeh>=3.2.0',
        'altair>=5.0.0',
        'dash>=2.14.0',
        'folium>=0.14.0',
    ],
    'cloud': [
        'boto3>=1.28.0',
        'azure-storage-blob>=12.17.0',
        'google-cloud-storage>=2.10.0',
    ],
    'dev': [
        'pytest>=7.4.0',
        'pytest-cov>=4.1.0',
        'black>=23.7.0',
        'flake8>=6.0.0',
        'mypy>=1.5.0',
        'pre-commit>=3.4.0',
        'jupyter>=1.0.0',
        'ipykernel>=6.25.0',
    ],
    'docs': [
        'sphinx>=7.1.0',
        'sphinx-rtd-theme>=1.3.0',
        'myst-parser>=2.0.0',
        'sphinx-autodoc-typehints>=1.24.0',
    ]
}

# Combine all optional requirements for 'all' extra
ALL_OPTIONAL = []
for deps in OPTIONAL_REQUIREMENTS.values():
    ALL_OPTIONAL.extend(deps)

# Add 'all' option to install everything
OPTIONAL_REQUIREMENTS['all'] = ALL_OPTIONAL

# Python version requirement
PYTHON_REQUIRES = ">=3.8"

# Package metadata
PACKAGE_NAME = "provider-network-management"
AUTHOR = "Network Operations Team"
AUTHOR_EMAIL = "netops@company.com"
DESCRIPTION = "AI-powered provider network management and optimization system"
URL = "https://github.com/your-org/provider-network-management"
LICENSE = "MIT"

# Classifiers for PyPI
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Telecommunications Industry",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: System :: Networking",
    "Topic :: System :: Systems Administration",
    "Topic :: Office/Business :: Financial :: Investment",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Visualization",
]

# Entry points for command-line tools
ENTRY_POINTS = {
    'console_scripts': [
        # Main application entry points
        'provider-network-app=provider_network_mgmt.app:main',
        'provider-network-analyze=provider_network_mgmt.cli.analyze:main',
        'provider-network-optimize=provider_network_mgmt.cli.optimize:main',
        'provider-network-report=provider_network_mgmt.cli.report:main',
        
        # Data management tools
        'provider-data-ingest=provider_network_mgmt.cli.data_ops:ingest_data',
        'provider-data-validate=provider_network_mgmt.cli.data_ops:validate_data',
        'provider-data-export=provider_network_mgmt.cli.data_ops:export_data',
        
        # Databricks integration
        'provider-deploy-databricks=provider_network_mgmt.cli.databricks_ops:deploy',
        'provider-run-job=provider_network_mgmt.cli.databricks_ops:run_job',
        
        # Utilities
        'provider-config=provider_network_mgmt.cli.config:configure',
        'provider-health-check=provider_network_mgmt.cli.health:check_system',
    ],
    
    # Plugin entry points for extensibility
    'provider_network_mgmt.agents': [
        'network_analyzer=provider_network_mgmt.agents.network_analyzer_agent:NetworkAnalyzerAgent',
        'cost_optimizer=provider_network_mgmt.agents.cost_optimizer_agent:CostOptimizerAgent',
        'report_generator=provider_network_mgmt.agents.report_generator_agent:ReportGeneratorAgent',
    ],
    
    'provider_network_mgmt.exporters': [
        'pdf=provider_network_mgmt.utils.pdf_generator:PDFReportGenerator',
        'excel=provider_network_mgmt.utils.excel_exporter:ExcelExporter',
        'json=provider_network_mgmt.utils.json_exporter:JSONExporter',
    ],
    
    'provider_network_mgmt.visualizations': [
        'charts=provider_network_mgmt.utils.chart_generator:ChartGenerator',
        'dashboards=provider_network_mgmt.streamlit_integration.dashboard:DashboardGenerator',
    ]
}

# Package data to include
PACKAGE_DATA = {
    'provider_network_mgmt': [
        'data/*.csv',
        'data/*.json',
        'templates/*.html',
        'templates/*.jinja2',
        'static/css/*.css',
        'static/js/*.js',
        'static/images/*',
        'config/*.yaml',
        'config/*.yml',
        'config/*.json',
    ]
}

# Data files to install
DATA_FILES = [
    ('share/provider_network_mgmt/examples', [
        'data/providers.csv',
        'examples/sample_analysis.py',
        'examples/sample_config.yaml',
    ]),
    ('share/provider_network_mgmt/docs', [
        'README.md',
        'CHANGELOG.md',
        'LICENSE',
    ]),
]

def check_dependencies():
    """Check for system dependencies and provide helpful error messages"""
    missing_deps = []
    
    # Check for required system packages
    try:
        import sqlite3
    except ImportError:
        missing_deps.append("sqlite3 (usually included with Python)")
    
    if missing_deps:
        print("Warning: Missing system dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("Please install these dependencies before continuing.")

def create_package_structure():
    """Create necessary package structure if it doesn't exist"""
    package_dir = Path(__file__).parent / "provider_network_mgmt"
    
    # Create main package directory
    package_dir.mkdir(exist_ok=True)
    
    # Create __init__.py if it doesn't exist
    init_file = package_dir / "__init__.py"
    if not init_file.exists():
        with open(init_file, 'w') as f:
            f.write(f'''"""
Provider Network Management System

A comprehensive AI-powered system for analyzing and optimizing network provider
performance, costs, and service level agreements.
"""

__version__ = "{get_version()}"
__author__ = "{AUTHOR}"
__email__ = "{AUTHOR_EMAIL}"

# Main package imports
from .agents.orchestrator import MultiAgentOrchestrator
from .utils.chart_generator import ChartGenerator
from .utils.pdf_generator import PDFReportGenerator

__all__ = [
    "MultiAgentOrchestrator",
    "ChartGenerator", 
    "PDFReportGenerator",
]
''')
    
    # Create CLI package
    cli_dir = package_dir / "cli"
    cli_dir.mkdir(exist_ok=True)
    (cli_dir / "__init__.py").touch()

def pre_install_checks():
    """Perform pre-installation checks and setup"""
    print("Setting up Provider Network Management System...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    # Create package structure
    create_package_structure()
    
    print("Pre-installation checks completed.")

# Custom setup command
class CustomInstallCommand:
    """Custom installation with post-install setup"""
    
    def __init__(self):
        self.setup_config_dir()
        self.setup_data_dir()
    
    def setup_config_dir(self):
        """Setup configuration directory"""
        config_dir = Path.home() / ".provider_network_mgmt"
        config_dir.mkdir(exist_ok=True)
        
        # Create default config file
        config_file = config_dir / "config.yaml"
        if not config_file.exists():
            default_config = """
# Provider Network Management Configuration
app:
  name: "Provider Network Management"
  version: "1.0.0"
  debug: false

database:
  type: "sqlite"
  path: "~/.provider_network_mgmt/data.db"

logging:
  level: "INFO"
  file: "~/.provider_network_mgmt/app.log"

export:
  default_format: "pdf"
  output_dir: "~/Downloads/provider_reports"

alerts:
  email_enabled: false
  smtp_server: ""
  smtp_port: 587
"""
            with open(config_file, 'w') as f:
                f.write(default_config)
    
    def setup_data_dir(self):
        """Setup data directory"""
        data_dir = Path.home() / ".provider_network_mgmt" / "data"
        data_dir.mkdir(exist_ok=True)

if __name__ == "__main__":
    # Run pre-installation checks
    pre_install_checks()
    
    # Setup package
    setup(
        name=PACKAGE_NAME,
        version=get_version(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url=URL,
        license=LICENSE,
        
        # Package discovery
        packages=find_packages(),
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        include_package_data=True,
        
        # Dependencies
        python_requires=PYTHON_REQUIRES,
        install_requires=get_requirements() or CORE_REQUIREMENTS,
        extras_require=OPTIONAL_REQUIREMENTS,
        
        # Entry points
        entry_points=ENTRY_POINTS,
        
        # Metadata
        classifiers=CLASSIFIERS,
        keywords="network management, provider analysis, cost optimization, AI, automation",
        project_urls={
            "Bug Reports": f"{URL}/issues",
            "Source": URL,
            "Documentation": f"{URL}/docs",
            "Changelog": f"{URL}/blob/main/CHANGELOG.md",
        },
        
        # Additional metadata
        zip_safe=False,  # Needed for package data access
        platforms=["any"],
        
        # Custom commands would go here if needed
        # cmdclass={
        #     'install': CustomInstallCommand,
        # },
    )
    
    # Post-installation setup
    try:
        custom_install = CustomInstallCommand()
        print("\n✅ Provider Network Management System installed successfully!")
        print("\nNext steps:")
        print("1. Run 'provider-network-app' to start the Streamlit application")
        print("2. Run 'provider-config' to configure your settings")
        print("3. Check 'provider-health-check' to verify installation")
        print(f"4. Configuration stored in: {Path.home() / '.provider_network_mgmt'}")
        
    except Exception as e:
        print(f"\n⚠️  Installation completed with warnings: {e}")
        print("You may need to run the configuration manually.")