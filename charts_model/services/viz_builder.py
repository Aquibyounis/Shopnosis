import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class VizBuilder:
    """
    Builds various types of charts using Plotly
    """
    
    def __init__(self):
        self.chart_configs = {
            "bar": {"height": 400, "width": 600},
            "line": {"height": 400, "width": 600},
            "pie": {"height": 400, "width": 500},
            "scatter": {"height": 400, "width": 600},
            "heatmap": {"height": 500, "width": 700},
            "histogram": {"height": 400, "width": 600},
            "box": {"height": 400, "width": 600}
        }
    
    def build_all_charts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Build all possible charts based on data types
        """
        charts = []
        
        # Get column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Build charts based on data types
        if len(numeric_cols) > 0:
            charts.extend(self._build_numeric_charts(df, numeric_cols))
        
        if len(categorical_cols) > 0:
            charts.extend(self._build_categorical_charts(df, categorical_cols))
        
        if len(date_cols) > 0:
            charts.extend(self._build_time_series_charts(df, date_cols, numeric_cols))
        
        # Build correlation heatmap if multiple numeric columns
        if len(numeric_cols) > 1:
            correlation_chart = self._build_correlation_heatmap(df, numeric_cols)
            if correlation_chart:
                charts.append(correlation_chart)
        
        return charts
    
    def _build_numeric_charts(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build charts for numeric columns
        """
        charts = []
        
        for col in numeric_cols:
            # Histogram
            hist_chart = self._build_histogram(df, col)
            if hist_chart:
                charts.append(hist_chart)
            
            # Box plot
            box_chart = self._build_box_plot(df, col)
            if box_chart:
                charts.append(box_chart)
        
        # Scatter plot for two numeric columns
        if len(numeric_cols) >= 2:
            scatter_chart = self._build_scatter_plot(df, numeric_cols[0], numeric_cols[1])
            if scatter_chart:
                charts.append(scatter_chart)
        
        return charts
    
    def _build_categorical_charts(self, df: pd.DataFrame, categorical_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build charts for categorical columns
        """
        charts = []
        
        for col in categorical_cols:
            # Bar chart for value counts
            bar_chart = self._build_bar_chart(df, col)
            if bar_chart:
                charts.append(bar_chart)
            
            # Pie chart for top categories
            pie_chart = self._build_pie_chart(df, col)
            if pie_chart:
                charts.append(pie_chart)
        
        return charts
    
    def _build_time_series_charts(self, df: pd.DataFrame, date_cols: List[str], numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build time series charts
        """
        charts = []
        
        for date_col in date_cols:
            if len(numeric_cols) > 0:
                # Line chart for time series
                line_chart = self._build_line_chart(df, date_col, numeric_cols[0])
                if line_chart:
                    charts.append(line_chart)
        
        return charts
    
    def _build_histogram(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build histogram chart
        """
        try:
            fig = px.histogram(
                df, 
                x=column,
                title=f"Distribution of {column}",
                nbins=30,
                **self.chart_configs["histogram"]
            )
            
            return {
                "type": "histogram",
                "title": f"Distribution of {column}",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building histogram for {column}: {e}")
            return None
    
    def _build_box_plot(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build box plot chart
        """
        try:
            fig = px.box(
                df, 
                y=column,
                title=f"Box Plot of {column}",
                **self.chart_configs["box"]
            )
            
            return {
                "type": "box",
                "title": f"Box Plot of {column}",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building box plot for {column}: {e}")
            return None
    
    def _build_bar_chart(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build bar chart for categorical data
        """
        try:
            value_counts = df[column].value_counts().head(10)
            
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f"Top 10 Values in {column}",
                labels={'x': column, 'y': 'Count'},
                **self.chart_configs["bar"]
            )
            
            return {
                "type": "bar",
                "title": f"Top 10 Values in {column}",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building bar chart for {column}: {e}")
            return None
    
    def _build_pie_chart(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build pie chart for categorical data
        """
        try:
            value_counts = df[column].value_counts().head(8)
            
            fig = px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title=f"Distribution of {column}",
                **self.chart_configs["pie"]
            )
            
            return {
                "type": "pie",
                "title": f"Distribution of {column}",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building pie chart for {column}: {e}")
            return None
    
    def _build_line_chart(self, df: pd.DataFrame, date_column: str, value_column: str) -> Optional[Dict[str, Any]]:
        """
        Build line chart for time series
        """
        try:
            # Group by date and aggregate
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            grouped = df_copy.groupby(df_copy[date_column].dt.date)[value_column].mean()
            
            fig = px.line(
                x=grouped.index,
                y=grouped.values,
                title=f"{value_column} Over Time",
                labels={'x': date_column, 'y': value_column},
                **self.chart_configs["line"]
            )
            
            return {
                "type": "line",
                "title": f"{value_column} Over Time",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building line chart: {e}")
            return None
    
    def _build_scatter_plot(self, df: pd.DataFrame, x_column: str, y_column: str) -> Optional[Dict[str, Any]]:
        """
        Build scatter plot for two numeric columns
        """
        try:
            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=f"{x_column} vs {y_column}",
                **self.chart_configs["scatter"]
            )
            
            return {
                "type": "scatter",
                "title": f"{x_column} vs {y_column}",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building scatter plot: {e}")
            return None
    
    def _build_correlation_heatmap(self, df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
        """
        Build correlation heatmap
        """
        try:
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                title="Correlation Heatmap",
                color_continuous_scale='RdBu',
                aspect="auto",
                **self.chart_configs["heatmap"]
            )
            
            return {
                "type": "heatmap",
                "title": "Correlation Heatmap",
                "data": fig.to_dict(),
                "config": {"displayModeBar": False}
            }
        except Exception as e:
            print(f"Error building correlation heatmap: {e}")
            return None
    
    def build_custom_chart(self, df: pd.DataFrame, chart_type: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Build custom chart based on type and parameters
        """
        try:
            if chart_type == "bar":
                return self._build_custom_bar(df, **kwargs)
            elif chart_type == "line":
                return self._build_custom_line(df, **kwargs)
            elif chart_type == "scatter":
                return self._build_custom_scatter(df, **kwargs)
            else:
                return None
        except Exception as e:
            print(f"Error building custom {chart_type} chart: {e}")
            return None
    
    def _build_custom_bar(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = None) -> Dict[str, Any]:
        """
        Build custom bar chart
        """
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title or f"{y_col} by {x_col}",
            **self.chart_configs["bar"]
        )
        
        return {
            "type": "bar",
            "title": title or f"{y_col} by {x_col}",
            "data": fig.to_dict(),
            "config": {"displayModeBar": False}
        }
    
    def _build_custom_line(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = None) -> Dict[str, Any]:
        """
        Build custom line chart
        """
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title or f"{y_col} Over {x_col}",
            **self.chart_configs["line"]
        )
        
        return {
            "type": "line",
            "title": title or f"{y_col} Over {x_col}",
            "data": fig.to_dict(),
            "config": {"displayModeBar": False}
        }
    
    def _build_custom_scatter(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = None) -> Dict[str, Any]:
        """
        Build custom scatter plot
        """
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=title or f"{x_col} vs {y_col}",
            **self.chart_configs["scatter"]
        )
        
        return {
            "type": "scatter",
            "title": title or f"{x_col} vs {y_col}",
            "data": fig.to_dict(),
            "config": {"displayModeBar": False}
        } 