"""
Chart Generator Module for Provider Network Management System

This module provides comprehensive visualization capabilities for network performance,
cost analysis, and provider metrics. Creates professional charts suitable for
reports and dashboard integration.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import io
import base64
from datetime import datetime, timedelta
import warnings
from .brand_themes import BrandThemes

warnings.filterwarnings('ignore')

# Set professional styling
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ChartGenerator:
    """
    Professional chart generation for provider network analysis
    """
    
    def __init__(self, theme: str = 'plotly_white'):
        """
        Initialize chart generator with styling preferences
        
        Args:
            theme: Plotly theme ('plotly_white', 'plotly_dark', 'simple_white')
        """

        self.theme_name = theme
        self.brand_themes = BrandThemes()
        # Apply theme colors automatically
        theme_config = self.brand_themes.get_theme(theme)
        self.color_palette = theme_config['chart_colors']

        # self.theme = theme
        # self.color_palette = [
        #     '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        #     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        # ]
        
    def create_performance_dashboard(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Create comprehensive performance dashboard with multiple visualizations
        
        Args:
            data: DataFrame with provider performance metrics
            
        Returns:
            Dictionary containing multiple chart objects
        """
        charts = {}
        
        # 1. Network Performance Overview
        charts['performance_overview'] = self._create_performance_overview(data)
        
        # 2. Cost Analysis
        charts['cost_analysis'] = self._create_cost_analysis(data)
        
        # 3. Provider Comparison
        charts['provider_comparison'] = self._create_provider_comparison(data)
        
        # 4. Trend Analysis
        charts['trend_analysis'] = self._create_trend_analysis(data)
        
        # 5. Geographic Distribution
        if 'latitude' in data.columns and 'longitude' in data.columns:
            charts['geographic_map'] = self._create_geographic_map(data)
            
        return charts
    
    def _create_performance_overview(self, data: pd.DataFrame) -> go.Figure:
        """Create performance overview dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Latency Distribution', 'Bandwidth Utilization', 
                          'Uptime by Provider', 'Performance Score'],
            specs=[[{"type": "histogram"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Latency distribution
        if 'latency_ms' in data.columns:
            fig.add_trace(
                go.Histogram(x=data['latency_ms'], name='Latency', 
                           marker_color=self.color_palette[0]),
                row=1, col=1
            )
        
        # Bandwidth utilization
        if 'bandwidth_utilization' in data.columns:
            bandwidth_avg = data.groupby('provider_name')['bandwidth_utilization'].mean().reset_index()
            fig.add_trace(
                go.Bar(x=bandwidth_avg['provider_name'], 
                      y=bandwidth_avg['bandwidth_utilization'],
                      name='Bandwidth %', marker_color=self.color_palette[1]),
                row=1, col=2
            )
        
        # Uptime by provider
        if 'uptime_percentage' in data.columns:
            uptime_avg = data.groupby('provider_name')['uptime_percentage'].mean().reset_index()
            fig.add_trace(
                go.Bar(x=uptime_avg['provider_name'], 
                      y=uptime_avg['uptime_percentage'],
                      name='Uptime %', marker_color=self.color_palette[2]),
                row=2, col=1
            )
        
        # Performance score scatter
        if 'cost_per_gb' in data.columns and 'performance_score' in data.columns:
            fig.add_trace(
                go.Scatter(x=data['cost_per_gb'], y=data['performance_score'],
                          mode='markers', name='Cost vs Performance',
                          marker=dict(size=10, color=self.color_palette[3])),
                row=2, col=2
            )
        
        fig.update_layout(
            title_text="Network Performance Overview Dashboard",
            showlegend=False,
            template=self.theme,
            height=600
        )
        
        return fig
    
    def _create_cost_analysis(self, data: pd.DataFrame) -> go.Figure:
        """Create comprehensive cost analysis visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Cost per GB by Provider', 'Monthly Cost Trend', 
                          'Cost vs Quality Score', 'Cost Distribution'],
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "box"}]]
        )
        
        # Cost per GB by provider
        if 'cost_per_gb' in data.columns:
            cost_avg = data.groupby('provider_name')['cost_per_gb'].mean().reset_index()
            fig.add_trace(
                go.Bar(x=cost_avg['provider_name'], y=cost_avg['cost_per_gb'],
                      name='Cost/GB', marker_color=self.color_palette[0]),
                row=1, col=1
            )
        
        # Monthly cost trend (simulated if date column exists)
        if 'monthly_cost' in data.columns:
            monthly_data = data.groupby(['provider_name', 'month'])['monthly_cost'].sum().reset_index()
            for provider in monthly_data['provider_name'].unique():
                provider_data = monthly_data[monthly_data['provider_name'] == provider]
                fig.add_trace(
                    go.Scatter(x=provider_data['month'], y=provider_data['monthly_cost'],
                              mode='lines+markers', name=provider),
                    row=1, col=2
                )
        
        # Cost vs Quality
        if 'cost_per_gb' in data.columns and 'quality_score' in data.columns:
            fig.add_trace(
                go.Scatter(x=data['cost_per_gb'], y=data['quality_score'],
                          mode='markers', name='Cost vs Quality',
                          marker=dict(size=8, color=self.color_palette[2])),
                row=2, col=1
            )
        
        # Cost distribution by provider
        if 'cost_per_gb' in data.columns:
            for i, provider in enumerate(data['provider_name'].unique()):
                provider_data = data[data['provider_name'] == provider]
                fig.add_trace(
                    go.Box(y=provider_data['cost_per_gb'], name=provider,
                          marker_color=self.color_palette[i % len(self.color_palette)]),
                    row=2, col=2
                )
        
        fig.update_layout(
            title_text="Cost Analysis Dashboard",
            template=self.theme,
            height=600,
            showlegend=True
        )
        
        return fig
    
    def _create_provider_comparison(self, data: pd.DataFrame) -> go.Figure:
        """Create provider comparison radar chart"""
        # Metrics for comparison
        metrics = ['performance_score', 'cost_efficiency', 'reliability_score', 
                  'support_rating', 'uptime_percentage']
        
        # Filter metrics that exist in data
        available_metrics = [m for m in metrics if m in data.columns]
        
        if not available_metrics:
            # Create sample comparison if no specific metrics available
            available_metrics = ['latency_ms', 'bandwidth_utilization', 'uptime_percentage']
            available_metrics = [m for m in available_metrics if m in data.columns]
        
        fig = go.Figure()
        
        # Normalize data for radar chart
        comparison_data = data.groupby('provider_name')[available_metrics].mean()
        
        # Normalize to 0-100 scale
        for metric in available_metrics:
            if metric == 'latency_ms':  # Lower is better for latency
                comparison_data[metric] = 100 - (comparison_data[metric] / comparison_data[metric].max() * 100)
            else:
                comparison_data[metric] = (comparison_data[metric] / comparison_data[metric].max() * 100)
        
        for i, provider in enumerate(comparison_data.index):
            fig.add_trace(go.Scatterpolar(
                r=comparison_data.loc[provider].values.tolist() + [comparison_data.loc[provider].values[0]],
                theta=available_metrics + [available_metrics[0]],
                fill='toself',
                name=provider,
                line_color=self.color_palette[i % len(self.color_palette)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Provider Performance Comparison",
            template=self.theme
        )
        
        return fig
    
    def _create_trend_analysis(self, data: pd.DataFrame) -> go.Figure:
        """Create trend analysis over time"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Performance Trends', 'Cost Trends'],
            shared_xaxes=True
        )
        
        # Generate time series if not available
        if 'date' not in data.columns:
            # Create synthetic time series
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            data_with_dates = []
            
            for provider in data['provider_name'].unique():
                provider_data = data[data['provider_name'] == provider].iloc[0]
                for date in dates:
                    row = provider_data.copy()
                    row['date'] = date
                    # Add some variation to make trends interesting
                    if 'performance_score' in data.columns:
                        row['performance_score'] += np.random.normal(0, 5)
                    if 'monthly_cost' in data.columns:
                        row['monthly_cost'] += np.random.normal(0, 100)
                    data_with_dates.append(row)
            
            trend_data = pd.DataFrame(data_with_dates)
        else:
            trend_data = data.copy()
        
        # Performance trends
        if 'performance_score' in trend_data.columns:
            for provider in trend_data['provider_name'].unique():
                provider_data = trend_data[trend_data['provider_name'] == provider]
                monthly_perf = provider_data.groupby(provider_data['date'].dt.to_period('M'))['performance_score'].mean()
                
                fig.add_trace(
                    go.Scatter(x=monthly_perf.index.astype(str), y=monthly_perf.values,
                              mode='lines+markers', name=f'{provider} Performance'),
                    row=1, col=1
                )
        
        # Cost trends
        if 'monthly_cost' in trend_data.columns:
            for provider in trend_data['provider_name'].unique():
                provider_data = trend_data[trend_data['provider_name'] == provider]
                monthly_cost = provider_data.groupby(provider_data['date'].dt.to_period('M'))['monthly_cost'].sum()
                
                fig.add_trace(
                    go.Scatter(x=monthly_cost.index.astype(str), y=monthly_cost.values,
                              mode='lines+markers', name=f'{provider} Cost'),
                    row=2, col=1
                )
        
        fig.update_layout(
            title_text="Trend Analysis Over Time",
            template=self.theme,
            height=600
        )
        
        return fig
    
    def _create_geographic_map(self, data: pd.DataFrame) -> go.Figure:
        """Create geographic distribution map"""
        fig = go.Figure()
        
        # Provider locations
        for provider in data['provider_name'].unique():
            provider_data = data[data['provider_name'] == provider]
            
            fig.add_trace(go.Scattermapbox(
                lat=provider_data['latitude'],
                lon=provider_data['longitude'],
                mode='markers',
                marker=dict(size=10),
                name=provider,
                text=provider_data['provider_name'],
                hovertemplate="<b>%{text}</b><br>" +
                            "Lat: %{lat}<br>" +
                            "Lon: %{lon}<br>" +
                            "<extra></extra>"
            ))
        
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=data['latitude'].mean(), lon=data['longitude'].mean()),
                zoom=3
            ),
            title="Provider Geographic Distribution",
            template=self.theme,
            height=500
        )
        
        return fig
    
    def create_cost_optimization_chart(self, current_costs: Dict, optimized_costs: Dict) -> go.Figure:
        """Create cost optimization comparison chart"""
        providers = list(current_costs.keys())
        current_values = list(current_costs.values())
        optimized_values = list(optimized_costs.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=providers,
            y=current_values,
            name='Current Costs',
            marker_color=self.color_palette[0]
        ))
        
        fig.add_trace(go.Bar(
            x=providers,
            y=optimized_values,
            name='Optimized Costs',
            marker_color=self.color_palette[1]
        ))
        
        # Add savings annotations
        for i, provider in enumerate(providers):
            savings = current_values[i] - optimized_values[i]
            savings_pct = (savings / current_values[i]) * 100
            fig.add_annotation(
                x=provider,
                y=max(current_values[i], optimized_values[i]) + max(current_values) * 0.05,
                text=f"Save: ${savings:,.0f}<br>({savings_pct:.1f}%)",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="green",
                font=dict(color="green", size=10)
            )
        
        fig.update_layout(
            title="Cost Optimization Analysis",
            xaxis_title="Provider",
            yaxis_title="Monthly Cost ($)",
            template=self.theme,
            barmode='group'
        )
        
        return fig
    
    def create_sla_compliance_chart(self, sla_data: pd.DataFrame) -> go.Figure:
        """Create SLA compliance visualization"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['SLA Compliance Rate', 'Violation Trends'],
            specs=[[{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Compliance rate by provider
        if 'compliance_rate' in sla_data.columns:
            fig.add_trace(
                go.Bar(x=sla_data['provider_name'], 
                      y=sla_data['compliance_rate'],
                      marker_color=self.color_palette[0],
                      name='Compliance Rate'),
                row=1, col=1
            )
        
        # Violation trends
        if 'violations_count' in sla_data.columns and 'month' in sla_data.columns:
            for provider in sla_data['provider_name'].unique():
                provider_data = sla_data[sla_data['provider_name'] == provider]
                fig.add_trace(
                    go.Scatter(x=provider_data['month'], 
                              y=provider_data['violations_count'],
                              mode='lines+markers',
                              name=f'{provider} Violations'),
                    row=1, col=2
                )
        
        fig.update_layout(
            title_text="SLA Compliance Dashboard",
            template=self.theme,
            height=400
        )
        
        return fig
    
    def export_chart_as_image(self, fig: go.Figure, filename: str = None, 
                            format: str = 'png', width: int = 1200, height: int = 800) -> str:
        """
        Export chart as image and return base64 string
        
        Args:
            fig: Plotly figure object
            filename: Optional filename to save
            format: Image format ('png', 'jpeg', 'svg', 'pdf')
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            Base64 encoded image string
        """
        img_bytes = fig.to_image(format=format, width=width, height=height)
        
        if filename:
            with open(filename, 'wb') as f:
                f.write(img_bytes)
        
        return base64.b64encode(img_bytes).decode()
    
    def create_executive_summary_chart(self, summary_data: Dict) -> go.Figure:
        """Create executive summary visualization with key metrics"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Cost Savings Potential', 'Performance Score', 
                          'Risk Assessment', 'ROI Timeline'],
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Cost savings indicator
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=summary_data.get('cost_savings_pct', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Cost Savings %"},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 25], 'color': "yellow"},
                    {'range': [25, 50], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ), row=1, col=1)
        
        # Performance score indicator
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=summary_data.get('overall_performance', 0),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Performance Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ]
            }
        ), row=1, col=2)
        
        # Risk assessment
        risk_levels = summary_data.get('risk_levels', {})
        if risk_levels:
            fig.add_trace(go.Bar(
                x=list(risk_levels.keys()),
                y=list(risk_levels.values()),
                marker_color=['red', 'yellow', 'green'],
                name='Risk Levels'
            ), row=2, col=1)
        
        # ROI timeline
        roi_timeline = summary_data.get('roi_timeline', {})
        if roi_timeline:
            fig.add_trace(go.Scatter(
                x=list(roi_timeline.keys()),
                y=list(roi_timeline.values()),
                mode='lines+markers',
                name='ROI Timeline',
                line=dict(color='purple', width=3)
            ), row=2, col=2)
        
        fig.update_layout(
            title_text="Executive Summary Dashboard",
            template=self.theme,
            height=600,
            showlegend=False
        )
        
        return fig

# Utility functions for chart styling and data preparation
def prepare_chart_data(data: pd.DataFrame, chart_type: str) -> pd.DataFrame:
    """Prepare and clean data for specific chart types"""
    cleaned_data = data.copy()
    
    # Handle missing values
    if chart_type == 'performance':
        # Fill missing performance metrics with median
        numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
        cleaned_data[numeric_cols] = cleaned_data[numeric_cols].fillna(
            cleaned_data[numeric_cols].median()
        )
    
    elif chart_type == 'cost':
        # Fill missing cost data with mean
        cost_cols = [col for col in cleaned_data.columns if 'cost' in col.lower()]
        for col in cost_cols:
            if col in cleaned_data.columns:
                cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].mean())
    
    return cleaned_data

def generate_color_palette(n_colors: int) -> List[str]:
    """Generate a professional color palette"""
    if n_colors <= 10:
        return px.colors.qualitative.Set3[:n_colors]
    else:
        # Generate custom colors for larger datasets
        colors = []
        for i in range(n_colors):
            hue = i / n_colors
            colors.append(f'hsl({int(hue * 360)}, 70%, 50%)')
        return colors