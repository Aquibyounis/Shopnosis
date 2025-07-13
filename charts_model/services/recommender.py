import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class Recommender:
    """
    Generates AI-based business insights and recommendations
    """
    
    def __init__(self):
        self.insight_types = {
            "trend": "trend_analysis",
            "anomaly": "anomaly_detection",
            "correlation": "correlation_analysis",
            "segmentation": "customer_segmentation",
            "forecast": "forecast_analysis"
        }
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate all possible recommendations for the dataset
        """
        recommendations = []
        
        # Get column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Generate different types of insights
        recommendations.extend(self._generate_trend_insights(df, date_cols, numeric_cols))
        recommendations.extend(self._generate_anomaly_insights(df, numeric_cols))
        recommendations.extend(self._generate_correlation_insights(df, numeric_cols))
        recommendations.extend(self._generate_segmentation_insights(df, categorical_cols, numeric_cols))
        recommendations.extend(self._generate_forecast_insights(df, date_cols, numeric_cols))
        
        return recommendations
    
    def _generate_trend_insights(self, df: pd.DataFrame, date_cols: List[str], numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Generate trend analysis insights
        """
        insights = []
        
        for date_col in date_cols:
            if numeric_cols:
                for num_col in numeric_cols:
                    trend_insight = self._analyze_trend(df, date_col, num_col)
                    if trend_insight:
                        insights.append(trend_insight)
        
        return insights
    
    def _generate_anomaly_insights(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Generate anomaly detection insights
        """
        insights = []
        
        for col in numeric_cols:
            anomaly_insight = self._detect_anomalies(df, col)
            if anomaly_insight:
                insights.append(anomaly_insight)
        
        return insights
    
    def _generate_correlation_insights(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Generate correlation analysis insights
        """
        insights = []
        
        if len(numeric_cols) >= 2:
            correlation_insight = self._analyze_correlations(df, numeric_cols)
            if correlation_insight:
                insights.append(correlation_insight)
        
        return insights
    
    def _generate_segmentation_insights(self, df: pd.DataFrame, categorical_cols: List[str], numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Generate customer segmentation insights
        """
        insights = []
        
        if categorical_cols and numeric_cols:
            segmentation_insight = self._perform_segmentation(df, categorical_cols, numeric_cols)
            if segmentation_insight:
                insights.append(segmentation_insight)
        
        return insights
    
    def _generate_forecast_insights(self, df: pd.DataFrame, date_cols: List[str], numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Generate forecast insights
        """
        insights = []
        
        for date_col in date_cols:
            if numeric_cols:
                for num_col in numeric_cols:
                    forecast_insight = self._generate_forecast(df, date_col, num_col)
                    if forecast_insight:
                        insights.append(forecast_insight)
        
        return insights
    
    def _analyze_trend(self, df: pd.DataFrame, date_column: str, value_column: str) -> Optional[Dict[str, Any]]:
        """
        Analyze trend for time series data
        """
        try:
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            
            # Group by date and calculate daily totals
            daily_totals = df_copy.groupby(df_copy[date_column].dt.date)[value_column].sum()
            
            if len(daily_totals) >= 3:
                # Calculate trend direction
                first_half = daily_totals.iloc[:len(daily_totals)//2].mean()
                second_half = daily_totals.iloc[len(daily_totals)//2:].mean()
                
                trend_direction = "increasing" if second_half > first_half else "decreasing"
                change_percentage = ((second_half - first_half) / first_half) * 100 if first_half != 0 else 0
                
                # Determine trend strength
                if abs(change_percentage) > 20:
                    strength = "strong"
                elif abs(change_percentage) > 10:
                    strength = "moderate"
                else:
                    strength = "weak"
                
                return {
                    "type": "trend",
                    "title": f"{value_column.replace('_', ' ').title()} Trend Analysis",
                    "description": f"The {value_column} shows a {strength} {trend_direction} trend with {abs(change_percentage):.1f}% change",
                    "recommendation": self._get_trend_recommendation(trend_direction, strength, value_column),
                    "severity": "high" if abs(change_percentage) > 20 else "medium" if abs(change_percentage) > 10 else "low",
                    "data": {
                        "trend_direction": trend_direction,
                        "change_percentage": change_percentage,
                        "strength": strength
                    }
                }
        except Exception as e:
            print(f"Error analyzing trend: {e}")
            return None
    
    def _detect_anomalies(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Detect anomalies in numeric data
        """
        try:
            # Calculate z-scores
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            anomalies = df[z_scores > 2]  # Values with z-score > 2
            
            if len(anomalies) > 0:
                anomaly_percentage = (len(anomalies) / len(df)) * 100
                
                return {
                    "type": "anomaly",
                    "title": f"Anomaly Detection in {column.replace('_', ' ').title()}",
                    "description": f"Found {len(anomalies)} anomalies ({anomaly_percentage:.1f}% of data) in {column}",
                    "recommendation": self._get_anomaly_recommendation(anomaly_percentage, column),
                    "severity": "high" if anomaly_percentage > 10 else "medium" if anomaly_percentage > 5 else "low",
                    "data": {
                        "anomaly_count": len(anomalies),
                        "anomaly_percentage": anomaly_percentage,
                        "max_anomaly_value": float(anomalies[column].max()),
                        "min_anomaly_value": float(anomalies[column].min())
                    }
                }
        except Exception as e:
            print(f"Error detecting anomalies: {e}")
            return None
    
    def _analyze_correlations(self, df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
        """
        Analyze correlations between numeric columns
        """
        try:
            corr_matrix = df[numeric_cols].corr()
            
            # Find strongest correlations
            strong_correlations = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:  # Strong correlation threshold
                        strong_correlations.append({
                            "col1": numeric_cols[i],
                            "col2": numeric_cols[j],
                            "correlation": corr_value
                        })
            
            if strong_correlations:
                # Sort by absolute correlation value
                strong_correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
                strongest = strong_correlations[0]
                
                return {
                    "type": "correlation",
                    "title": "Strong Correlation Detected",
                    "description": f"Strong correlation ({strongest['correlation']:.2f}) between {strongest['col1']} and {strongest['col2']}",
                    "recommendation": self._get_correlation_recommendation(strongest),
                    "severity": "medium",
                    "data": {
                        "strong_correlations": strong_correlations,
                        "total_correlations_analyzed": len(strong_correlations)
                    }
                }
        except Exception as e:
            print(f"Error analyzing correlations: {e}")
            return None
    
    def _perform_segmentation(self, df: pd.DataFrame, categorical_cols: List[str], numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
        """
        Perform customer segmentation analysis
        """
        try:
            # Prepare data for clustering
            if len(numeric_cols) >= 2:
                # Use first two numeric columns for clustering
                cluster_data = df[numeric_cols[:2]].dropna()
                
                if len(cluster_data) > 10:  # Need sufficient data for clustering
                    # Standardize data
                    scaler = StandardScaler()
                    scaled_data = scaler.fit_transform(cluster_data)
                    
                    # Perform K-means clustering
                    kmeans = KMeans(n_clusters=3, random_state=42)
                    clusters = kmeans.fit_predict(scaled_data)
                    
                    # Analyze clusters
                    cluster_analysis = []
                    for i in range(3):
                        cluster_data_i = cluster_data[clusters == i]
                        cluster_analysis.append({
                            "cluster_id": i,
                            "size": len(cluster_data_i),
                            "percentage": (len(cluster_data_i) / len(cluster_data)) * 100,
                            "avg_values": cluster_data_i.mean().to_dict()
                        })
                    
                    return {
                        "type": "segmentation",
                        "title": "Customer Segmentation Analysis",
                        "description": f"Identified {len(cluster_analysis)} distinct customer segments",
                        "recommendation": self._get_segmentation_recommendation(cluster_analysis),
                        "severity": "medium",
                        "data": {
                            "segments": cluster_analysis,
                            "features_used": numeric_cols[:2]
                        }
                    }
        except Exception as e:
            print(f"Error performing segmentation: {e}")
            return None
    
    def _generate_forecast(self, df: pd.DataFrame, date_column: str, value_column: str) -> Optional[Dict[str, Any]]:
        """
        Generate simple forecast insights
        """
        try:
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            
            # Group by date and calculate daily totals
            daily_totals = df_copy.groupby(df_copy[date_column].dt.date)[value_column].sum()
            
            if len(daily_totals) >= 7:  # Need at least a week of data
                # Simple linear trend projection
                x = np.arange(len(daily_totals))
                y = daily_totals.values
                
                # Fit linear trend
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                
                # Project next 7 days
                future_x = np.arange(len(daily_totals), len(daily_totals) + 7)
                future_y = p(future_x)
                
                avg_current = daily_totals.mean()
                avg_forecast = future_y.mean()
                forecast_change = ((avg_forecast - avg_current) / avg_current) * 100 if avg_current != 0 else 0
                
                return {
                    "type": "forecast",
                    "title": f"{value_column.replace('_', ' ').title()} Forecast",
                    "description": f"Projected {forecast_change:.1f}% change in {value_column} over next 7 days",
                    "recommendation": self._get_forecast_recommendation(forecast_change, value_column),
                    "severity": "high" if abs(forecast_change) > 20 else "medium" if abs(forecast_change) > 10 else "low",
                    "data": {
                        "forecast_change": forecast_change,
                        "current_average": avg_current,
                        "forecast_average": avg_forecast,
                        "forecast_period": "7 days"
                    }
                }
        except Exception as e:
            print(f"Error generating forecast: {e}")
            return None
    
    def _get_trend_recommendation(self, direction: str, strength: str, column: str) -> str:
        """
        Get recommendation based on trend analysis
        """
        if direction == "increasing":
            if strength == "strong":
                return f"Strong growth in {column}. Consider scaling up operations and marketing efforts."
            else:
                return f"Moderate growth in {column}. Monitor performance and consider targeted improvements."
        else:
            if strength == "strong":
                return f"Significant decline in {column}. Investigate root causes and implement corrective actions."
            else:
                return f"Moderate decline in {column}. Review strategies and consider optimization."
    
    def _get_anomaly_recommendation(self, percentage: float, column: str) -> str:
        """
        Get recommendation based on anomaly detection
        """
        if percentage > 10:
            return f"High anomaly rate in {column}. Investigate data quality and business processes."
        elif percentage > 5:
            return f"Moderate anomalies detected in {column}. Review data collection methods."
        else:
            return f"Low anomaly rate in {column}. Data quality appears good."
    
    def _get_correlation_recommendation(self, correlation: Dict[str, Any]) -> str:
        """
        Get recommendation based on correlation analysis
        """
        col1, col2 = correlation["col1"], correlation["col2"]
        corr_value = correlation["correlation"]
        
        if corr_value > 0.8:
            return f"Very strong positive correlation between {col1} and {col2}. Consider combining these metrics."
        elif corr_value > 0.7:
            return f"Strong correlation between {col1} and {col2}. Monitor both metrics together."
        else:
            return f"Moderate correlation between {col1} and {col2}. Analyze relationship further."
    
    def _get_segmentation_recommendation(self, segments: List[Dict[str, Any]]) -> str:
        """
        Get recommendation based on segmentation analysis
        """
        largest_segment = max(segments, key=lambda x: x["percentage"])
        
        return f"Largest segment represents {largest_segment['percentage']:.1f}% of customers. Focus marketing efforts on this segment."
    
    def _get_forecast_recommendation(self, change: float, column: str) -> str:
        """
        Get recommendation based on forecast analysis
        """
        if change > 20:
            return f"Strong projected growth in {column}. Prepare for increased demand and capacity."
        elif change > 10:
            return f"Moderate growth expected in {column}. Plan for gradual scaling."
        elif change < -20:
            return f"Significant decline projected in {column}. Investigate causes and implement recovery strategies."
        elif change < -10:
            return f"Moderate decline expected in {column}. Review strategies and optimize operations."
        else:
            return f"Stable forecast for {column}. Maintain current strategies and monitor performance."
    
    def generate_custom_insight(self, df: pd.DataFrame, insight_type: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Generate custom insight based on type and parameters
        """
        try:
            if insight_type == "trend":
                return self._analyze_trend(df, kwargs.get("date_column"), kwargs.get("value_column"))
            elif insight_type == "anomaly":
                return self._detect_anomalies(df, kwargs.get("column"))
            elif insight_type == "correlation":
                return self._analyze_correlations(df, kwargs.get("numeric_cols"))
            else:
                return None
        except Exception as e:
            print(f"Error generating custom {insight_type} insight: {e}")
            return None
    
    def get_insight_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary of available insights
        """
        insights = self.generate_recommendations(df)
        
        summary = {
            "total_insights": len(insights),
            "insight_types": {},
            "severity_distribution": {}
        }
        
        for insight in insights:
            insight_type = insight.get("type", "")
            severity = insight.get("severity", "low")
            
            if insight_type not in summary["insight_types"]:
                summary["insight_types"][insight_type] = 0
            summary["insight_types"][insight_type] += 1
            
            if severity not in summary["severity_distribution"]:
                summary["severity_distribution"][severity] = 0
            summary["severity_distribution"][severity] += 1
        
        return summary 