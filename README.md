# provider-network-app

# requirements.txt
# Core Streamlit and Data Processing
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
scipy>=1.10.0

# Databricks Integration
databricks-sdk>=0.12.0
databricks-connect>=13.0.0

# PDF Generation
reportlab>=4.0.0
Pillow>=9.0.0

# Additional Dependencies
requests>=2.28.0
python-dateutil>=2.8.0

# ============================================
# databricks.yml - Databricks Bundle Configuration
# ============================================

# Bundle configuration for Databricks deployment
bundle:
  name: provider-network-management
  
resources:
  apps:
    network-management-app:
      name: "Provider Network Management - AI Powered"
      description: "Intelligent provider network optimization with AI agents and PDF reporting"
      
      source_code_path: ./src
      
      config:
        command: ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501"]
        
        env:
          - name: PYTHONPATH
            value: /app/src
          - name: STREAMLIT_SERVER_HEADLESS
            value: true
          - name: STREAMLIT_SERVER_PORT
            value: 8501
            
      compute:
        cluster_id: "${var.cluster_id}"
        
      permissions:
        - level: CAN_RUN
          group_name: "network-managers"
        - level: CAN_MANAGE
          group_name: "network-admins"

variables:
  cluster_id:
    description: "Databricks cluster ID for the app"
    default: "your-cluster-id"

# ============================================
# setup.py - Python Package Setup
# ============================================

from setuptools import setup, find_packages

setup(
    name="provider-network-management",
    version="1.0.0",
    description="AI-Powered Provider Network Management System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Network Management Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "scipy>=1.10.0",
        "databricks-sdk>=0.12.0",
        "reportlab>=4.0.0",
        "Pillow>=9.0.0",
        "requests>=2.28.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "databricks": [
            "databricks-connect>=13.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

# ============================================
# README.md - Project Documentation
# ============================================

# 🏥 AI-Powered Provider Network Management

An intelligent provider network optimization system built with Databricks AI agents, Streamlit, and comprehensive PDF reporting capabilities.

## 🌟 Features

### 🤖 AI-Powered Analysis
- **Modular Agent Architecture**: Specialized agents for network analysis, cost optimization, and report generation
- **Databricks LLM Integration**: Uses Databricks Foundation Models for intelligent insights
- **Natural Language Queries**: Ask questions in plain English about your network
- **Multi-Agent Orchestration**: Complex queries handled by multiple specialized agents

### 📊 Comprehensive Analytics
- **Provider Performance Analysis**: Quality scores, efficiency metrics, and benchmarking
- **Cost Optimization**: Identify savings opportunities and contract negotiation strategies
- **Geographic Coverage**: CBSA-level analysis and gap identification
- **Quality vs Cost Quadrants**: Strategic positioning analysis

### 📋 Professional Reporting
- **AI-Generated Reports**: Executive summaries and detailed analysis
- **PDF Export**: Professional reports with charts and recommendations
- **Multiple Audiences**: Tailored content for executives, managers, and boards
- **Interactive Visualizations**: Plotly charts and dashboards

### 🔧 Technical Architecture
- **Modular Design**: Separate agents for different functions
- **Databricks Integration**: Native LLM support and data lake connectivity
- **Streamlit Frontend**: Interactive web interface
- **PDF Generation**: Professional document creation

## 🚀 Quick Start

### Prerequisites
- Databricks workspace with Apps enabled
- Python 3.8+
- Access to Databricks Foundation Models

### Installation

1. **Clone and Setup**
```bash
git clone <repository-url>
cd provider-network-management
pip install -r requirements.txt
```

2. **Configure Databricks Secrets**
```bash
# Using Databricks CLI
databricks secrets create-scope network-app
databricks secrets put --scope network-app --key workspace-url
databricks secrets put --scope network-app --key databricks-token
```

3. **Prepare Data**
```bash
# Create data directory and add your CSV
mkdir data
# Copy your providers.csv to data/ folder
```

4. **Deploy to Databricks**
```bash
# Deploy using Databricks bundle
databricks bundle deploy --target dev
databricks bundle run network-management-app
```

### Local Development
```bash
# Run locally for development
streamlit run app.py
```

## 📁 Project Structure

```
provider-network-management/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── databricks.yml                  # Databricks bundle configuration
├── setup.py                       # Package setup
├── README.md                      # This file
├── agents/                        # AI Agent modules
│   ├── __init__.py
│   ├── base_agent.py              # Base agent class
│   ├── network_analyzer_agent.py   # Network analysis specialist
│   ├── cost_optimizer_agent.py     # Cost optimization specialist
│   ├── report_generator_agent.py   # Report generation specialist
│   └── orchestrator.py            # Multi-agent orchestrator
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── pdf_generator.py           # PDF report generation
│   └── chart_generator.py         # Chart creation utilities
├── streamlit_integration/         # Streamlit-specific components
│   ├── __init__.py
│   └── pdf_export.py             # PDF export functionality
└── data/                          # Data directory
    └── providers.csv              # Provider data (user-supplied)
```

## 📊 Data Format

Your `data/providers.csv` should include these columns:

```csv
id,name,organization,score,efficiency_gain,state,cbsa,clinical_groups,in_network,patient_volume,avg_cost,quality_rating
1,Dr. Sarah Johnson,Metro Medical Group,92,15.3,CA,Los Angeles-Long Beach-Anaheim,Cardiology;Internal Medicine,True,1250,285,4.8
```

**Required Columns:**
- `id`: Unique provider identifier
- `name`: Provider name
- `organization`: Healthcare organization
- `score`: Provider quality score (0-100)
- `efficiency_gain`: Efficiency percentage
- `state`: Two-letter state code
- `cbsa`: Core Based Statistical Area name
- `clinical_groups`: Semicolon-separated specialties
- `in_network`: Boolean (True/False)
- `patient_volume`: Number of patients
- `avg_cost`: Average cost per episode
- `quality_rating`: Quality rating (1-5 scale)

## 🤖 AI Agent Architecture

### Base Agent (`base_agent.py`)
- Common LLM interaction methods
- Error handling and response cleaning
- Logging and monitoring

### Network Analyzer Agent (`network_analyzer_agent.py`)
- Provider performance analysis
- Network summary generation
- Quality trend analysis
- Competitive benchmarking

### Cost Optimizer Agent (`cost_optimizer_agent.py`)
- Cost reduction strategies
- Contract analysis
- Provider replacement options
- ROI calculations

### Report Generator Agent (`report_generator_agent.py`)
- Executive summaries
- Detailed diagnostics reports
- Regulatory compliance docs
- Custom report formats

### Orchestrator (`orchestrator.py`)
- Intent classification
- Agent routing
- Multi-agent coordination
- Response integration

## 📋 Usage Examples

### Network Analysis Queries
```
"Analyze the performance of our cardiology network"
"Which providers are underperforming and need attention?"
"Show me quality trends over the past year"
```

### Cost Optimization Queries
```
"How can I reduce network costs by 15%?"
"Which high-cost providers should I consider replacing?"
"Generate contract negotiation strategies for top performers"
```

### Reporting Queries
```
"Generate an executive summary for the board"
"Create a comprehensive provider diagnostics report"
"Prepare a cost optimization analysis for Q4 planning"
```

## 🔐 Security & Compliance

### Data Protection
- Provider data remains in Databricks environment
- No external data transmission for LLM processing
- Role-based access controls
- Audit logging for all interactions

### HIPAA Compliance
- De-identified data processing
- Secure data handling practices
- Access controls and monitoring
- Audit trail maintenance

## 🛠️ Configuration

### Databricks Secrets
```bash
# Required secrets
workspace-url          # Your Databricks workspace URL
databricks-token      # Access token for API calls

# Optional secrets (for external LLMs)
openai-api-key        # OpenAI API key
anthropic-api-key     # Anthropic API key
```

### Environment Variables
```bash
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
PYTHONPATH=/app/src
```

## 📈 Performance Optimization

### Caching Strategies
- Data loading cached for 5 minutes
- LLM responses cached based on query hash
- Chart generation optimized with plotly caching

### Resource Management
- Automatic cluster scaling
- Memory-efficient data processing
- Optimized LLM token usage

## 🔧 Development

### Local Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black .

# Type checking
mypy .
```

### Adding New Agents
1. Inherit from `BaseAgent`
2. Implement `get_system_prompt()` and `process_request()`
3. Add to orchestrator routing
4. Update documentation

### Extending PDF Reports
1. Modify `NetworkPDFGenerator` class
2. Add new chart types in `NetworkChartGenerator`
3. Update report templates
4. Test with sample data

## 🐛 Troubleshooting

### Common Issues

**"Databricks SDK not available"**
- Install: `pip install databricks-sdk`
- Configure workspace connection

**"PDF generation not available"**
- Install: `pip install reportlab Pillow`
- Check system dependencies

**"LLM endpoint not found"**
- Verify Databricks Foundation Models are enabled
- Check workspace permissions
- Validate model endpoint names

**"Data folder not found"**
- Create `data/` directory
- Add `providers.csv` with required columns
- Check file permissions

### Debug Mode
```python
# Enable debug logging in app
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

### Documentation
- [Databricks Apps Documentation](https://docs.databricks.com/en/dev-tools/databricks-apps/index.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ReportLab PDF Generation](https://www.reportlab.com/documentation/)

### Getting Help
1. Check troubleshooting section
2. Review Databricks workspace logs
3. Validate data format and permissions
4. Test with sample data

## 🔄 Updates & Maintenance

### Regular Updates
- Monitor Databricks SDK updates
- Update LLM model endpoints as needed
- Refresh sample data and documentation
- Performance optimization reviews

### Version Management
- Semantic versioning (MAJOR.MINOR.PATCH)
- Databricks bundle versioning
- Backward compatibility considerations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

---

**Ready to optimize your provider network with AI? 🚀**

For deployment assistance or questions, refer to the troubleshooting section or check the Databricks documentation.

# ============================================
# .gitignore - Git Ignore File
# ============================================

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/

# Streamlit
.streamlit/

# Data files (add your specific data files here)
data/*.csv
data/*.xlsx
data/*.json
!data/sample_providers.csv

# Generated reports
reports/
outputs/
*.pdf

# Databricks
.databricks/
databricks.yml.bak

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# ============================================
# Dockerfile - Optional Docker Support
# ============================================

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# ============================================
# docker-compose.yml - Docker Compose Configuration
# ============================================

version: '3.8'

services:
  provider-network-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
    volumes:
      - ./data:/app/data:ro
      - ./reports:/app/reports
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

# ============================================
# deploy.sh - Deployment Script
# ============================================

#!/bin/bash

# Provider Network Management Deployment Script
set -e

echo "🏥 Deploying Provider Network Management App to Databricks"

# Check if Databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "❌ Databricks CLI not found. Please install it first:"
    echo "pip install databricks-cli"
    exit 1
fi

# Check if bundle configuration exists
if [ ! -f "databricks.yml" ]; then
    echo "❌ databricks.yml not found. Please ensure you're in the project root."
    exit 1
fi

# Validate bundle configuration
echo "📋 Validating bundle configuration..."
databricks bundle validate

# Deploy to Databricks
echo "🚀 Deploying to Databricks..."
databricks bundle deploy --target ${TARGET:-dev}

# Optional: Run the app after deployment
if [ "$1" = "--run" ]; then
    echo "▶️  Starting the application..."
    databricks bundle run network-management-app --target ${TARGET:-dev}
fi

echo "✅ Deployment completed successfully!"
echo "🌐 Access your app in the Databricks workspace under Apps section"

# ============================================
# tests/test_agents.py - Unit Tests
# ============================================

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from agents.network_analyzer_agent import NetworkAnalyzerAgent
from agents.cost_optimizer_agent import CostOptimizerAgent
from agents.orchestrator import AgentOrchestrator

class TestNetworkAnalyzerAgent:
    """Test cases for Network Analyzer Agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.mock_workspace_client = Mock()
        self.agent = NetworkAnalyzerAgent(self.mock_workspace_client)
    
    def test_system_prompt(self):
        """Test system prompt generation"""
        prompt = self.agent.get_system_prompt()
        assert "Network Analysis Expert" in prompt
        assert "provider performance" in prompt.lower()
    
    def test_provider_performance_analysis(self):
        """Test provider performance analysis"""
        test_data = {
            "providers": [
                {"id": 1, "name": "Dr. Test", "score": 90, "avg_cost": 300}
            ]
        }
        
        request = {
            "analysis_type": "provider_performance",
            "provider_data": test_data,
            "provider_id": "1"
        }
        
        with patch.object(self.agent, 'call_llm', return_value="Test analysis"):
            response = self.agent.process_request(request)
            
        assert response["success"] is True
        assert response["analysis_type"] == "provider_performance"
        assert "analysis" in response

class TestCostOptimizerAgent:
    """Test cases for Cost Optimizer Agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.mock_workspace_client = Mock()
        self.agent = CostOptimizerAgent(self.mock_workspace_client)
    
    def test_cost_reduction_strategies(self):
        """Test cost reduction strategy generation"""
        test_data = {
            "high_cost_providers": [
                {"name": "Dr. Expensive", "avg_cost": 500, "score": 80}
            ],
            "network_stats": {"avg_cost": 300, "total_volume": 1000}
        }
        
        request = {
            "optimization_type": "cost_reduction",
            "target_savings": 15.0,
            "savings_type": "percentage",
            "provider_data": test_data
        }
        
        with patch.object(self.agent, 'call_llm', return_value="Cost strategies"):
            response = self.agent.process_request(request)
            
        assert response["success"] is True
        assert response["optimization_type"] == "cost_reduction"

class TestAgentOrchestrator:
    """Test cases for Agent Orchestrator"""
    
    def setup_method(self):
        """Setup test environment"""
        self.mock_workspace_client = Mock()
        self.orchestrator = AgentOrchestrator(self.mock_workspace_client)
    
    def test_intent_classification(self):
        """Test query intent classification"""
        cost_query = "How can I reduce costs by 20%?"
        intent = self.orchestrator._classify_intent(cost_query)
        
        assert intent["primary_agent"] == "cost_optimization"
        assert "cost" in intent["keywords_found"]
    
    def test_network_analysis_routing(self):
        """Test routing to network analysis agent"""
        query = "Analyze provider performance"
        context = {"providers": []}
        
        with patch.object(self.orchestrator.network_analyzer, 'process_request') as mock_process:
            mock_process.return_value = {"success": True, "analysis": "Test"}
            response = self.orchestrator.route_request(query, context)
            
        mock_process.assert_called_once()
        assert response["success"] is True

if __name__ == "__main__":
    pytest.main([__file__])

# ============================================
# DEPLOYMENT_GUIDE.md - Detailed Deployment Instructions
# ============================================

# 🚀 Deployment Guide - Provider Network Management

## Prerequisites Checklist

- [ ] Databricks workspace with Apps enabled
- [ ] Python 3.8+ environment
- [ ] Databricks CLI installed and configured
- [ ] Access to Foundation Models in your workspace
- [ ] Provider data in CSV format

## Step-by-Step Deployment

### 1. Environment Setup

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure Databricks CLI
databricks configure --token
# Enter your workspace URL and access token
```

### 2. Clone and Prepare

```bash
# Clone the repository
git clone <your-repo-url>
cd provider-network-management

# Install dependencies
pip install -r requirements.txt

# Verify structure
ls -la
# Should see: app.py, agents/, utils/, data/, etc.
```

### 3. Data Preparation

```bash
# Create data directory if it doesn't exist
mkdir -p data

# Copy your provider data
cp /path/to/your/providers.csv data/

# Verify data format
head -5 data/providers.csv
```

### 4. Configure Secrets

```bash
# Create secret scope
databricks secrets create-scope network-app

# Add workspace URL
databricks secrets put --scope network-app --key workspace-url
# Enter your workspace URL (e.g., https://your-workspace.cloud.databricks.com)

# Add authentication token
databricks secrets put --scope network-app --key databricks-token
# Enter your access token
```

### 5. Deploy Application

```bash
# Validate configuration
databricks bundle validate

# Deploy to development
databricks bundle deploy --target dev

# Deploy to production (optional)
databricks bundle deploy --target prod
```

### 6. Verify Deployment

```bash
# Check app status
databricks apps list

# Get app details
databricks apps get network-management-app
```

### 7. Access Your Application

1. Open your Databricks workspace
2. Navigate to "Apps" in the sidebar
3. Find "Provider Network Management - AI Powered"
4. Click to launch the application

## Configuration Options

### Custom Model Endpoints

If you have custom LLM endpoints:

```bash
# Add custom endpoint
databricks secrets put --scope network-app --key custom-model-endpoint
```

### External LLM APIs (Optional)

```bash
# For OpenAI integration
databricks secrets put --scope network-app --key openai-api-key

# For Anthropic integration
databricks secrets put --scope network-app --key anthropic-api-key
```

### Performance Tuning

Edit `databricks.yml` for resource allocation:

```yaml
compute:
  cluster_id: "${var.cluster_id}"
  min_workers: 1
  max_workers: 4
  node_type_id: "i3.xlarge"
  driver_node_type_id: "i3.xlarge"
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check application logs
databricks apps logs network-management-app

# Monitor resource usage
databricks clusters get --cluster-id <your-cluster-id>
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Redeploy
databricks bundle deploy --target dev
```

### Troubleshooting

**Common Issues:**

1. **Model endpoint not found**
   - Verify Foundation Models are enabled
   - Check endpoint names in workspace

2. **Data loading errors**
   - Verify CSV format matches requirements
   - Check file permissions

3. **Memory issues**
   - Increase cluster resources
   - Optimize data processing

**Debug Mode:**

```python
# Add to top of app.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Best Practices

### Access Control

```bash
# Set workspace permissions
databricks permissions update workspace-object <object-id> \
  --json '{"access_control_list": [{"user_name": "user@company.com", "permission_level": "CAN_RUN"}]}'
```

### Data Protection

- Use Databricks Unity Catalog for data governance
- Implement row-level security if needed
- Regular access reviews and audits

### Compliance

- Enable audit logging
- Implement data retention policies
- Document data lineage

## Scaling Considerations

### High-Volume Deployments

- Use auto-scaling clusters
- Implement data partitioning
- Consider Delta Lake for large datasets

### Multi-Environment Setup

```yaml
# databricks.yml
targets:
  dev:
    variables:
      cluster_id: "dev-cluster-id"
  
  staging:
    variables:
      cluster_id: "staging-cluster-id"
  
  prod:
    variables:
      cluster_id: "prod-cluster-id"
```

## Support and Resources

- [Databricks Apps Documentation](https://docs.databricks.com/apps/)
- [Foundation Models Guide](https://docs.databricks.com/machine-learning/foundation-models/)
- [Unity Catalog Setup](https://docs.databricks.com/data-governance/unity-catalog/)

---

**Deployment complete! Your AI-powered provider network management system is ready to use! 🎉**

provider-network-management/
├── app.py                          # Main Streamlit app
├── agents/                         # Modular AI agents
│   ├── base_agent.py              # Common functionality
│   ├── network_analyzer_agent.py   # Performance analysis
│   ├── cost_optimizer_agent.py     # Cost optimization
│   ├── report_generator_agent.py   # Report creation
│   └── orchestrator.py            # Multi-agent coordination
├── utils/                          # Utilities
│   ├── pdf_generator.py           # Professional PDF creation
│   └── chart_generator.py         # Visualization generation
├── streamlit_integration/          # UI components
│   └── pdf_export.py              # Export functionality
├── data/                          # Data directory
│   └── providers.csv              # Your provider data
├── requirements.txt               # Dependencies
├── databricks.yml               # Databricks deployment config
├── setup.py                     # Package configuration
└── README.md                    # Comprehensive documentation