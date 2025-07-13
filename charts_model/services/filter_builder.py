import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class FilterBuilder:
    """
    Automatically detects and generates filters from data
    """
    
    def __init__(self):
        self.filter_types = {
            "categorical": "categorical",
            "range": "range", 
            "date": "date"
        }
    
    def build_filters(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Build all available filters for the dataset
        """
        filters = {}
        
        for column in df.columns:
            filter_config = self._detect_filter_type(df, column)
            if filter_config:
                filters[column] = filter_config
        
        return filters
    
    def _detect_filter_type(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Detect the appropriate filter type for a column
        """
        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(df[column]):
            return self._build_range_filter(df, column)
        
        # Check if column is datetime
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            return self._build_date_filter(df, column)
        
        # Check if column is categorical (object type with limited unique values)
        elif df[column].dtype == 'object':
            unique_count = df[column].nunique()
            if unique_count <= 50:  # Consider categorical if <= 50 unique values
                return self._build_categorical_filter(df, column)
            else:
                return self._build_text_filter(df, column)
        
        return None
    
    def _build_range_filter(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Build range filter for numeric columns
        """
        try:
            min_val = float(df[column].min())
            max_val = float(df[column].max())
            current_min = min_val
            current_max = max_val
            
            # Calculate step size for slider
            step = (max_val - min_val) / 100 if max_val != min_val else 1
            
            return {
                "type": "range",
                "min": min_val,
                "max": max_val,
                "current_min": current_min,
                "current_max": current_max,
                "step": step,
                "label": column.replace('_', ' ').title(),
                "description": f"Filter {column} between {min_val:.2f} and {max_val:.2f}"
            }
        except Exception as e:
            print(f"Error building range filter for {column}: {e}")
            return None
    
    def _build_date_filter(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Build date filter for datetime columns
        """
        try:
            # Convert to datetime if not already
            df_copy = df.copy()
            df_copy[column] = pd.to_datetime(df_copy[column])
            
            min_date = df_copy[column].min()
            max_date = df_copy[column].max()
            
            # Format dates for frontend
            min_date_str = min_date.strftime('%Y-%m-%d')
            max_date_str = max_date.strftime('%Y-%m-%d')
            
            return {
                "type": "date",
                "min_date": min_date_str,
                "max_date": max_date_str,
                "current_start": min_date_str,
                "current_end": max_date_str,
                "label": column.replace('_', ' ').title(),
                "description": f"Filter {column} between {min_date_str} and {max_date_str}"
            }
        except Exception as e:
            print(f"Error building date filter for {column}: {e}")
            return None
    
    def _build_categorical_filter(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Build categorical filter for categorical columns
        """
        try:
            # Get unique values and their counts
            value_counts = df[column].value_counts()
            
            # Limit to top 20 values to avoid overwhelming UI
            top_values = value_counts.head(20)
            
            options = [
                {
                    "value": str(val),
                    "label": str(val),
                    "count": int(count)
                }
                for val, count in top_values.items()
            ]
            
            return {
                "type": "categorical",
                "options": options,
                "selected": [],  # Initially no values selected
                "label": column.replace('_', ' ').title(),
                "description": f"Filter {column} by category",
                "multi_select": True
            }
        except Exception as e:
            print(f"Error building categorical filter for {column}: {e}")
            return None
    
    def _build_text_filter(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Build text filter for text columns with many unique values
        """
        try:
            return {
                "type": "text",
                "placeholder": f"Search in {column}...",
                "label": column.replace('_', ' ').title(),
                "description": f"Search text in {column}",
                "current_value": ""
            }
        except Exception as e:
            print(f"Error building text filter for {column}: {e}")
            return None
    
    def apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filters to the dataframe
        """
        filtered_df = df.copy()
        
        for column, filter_config in filters.items():
            if column not in filtered_df.columns:
                continue
            
            filter_type = filter_config.get("type")
            
            if filter_type == "range":
                filtered_df = self._apply_range_filter(filtered_df, column, filter_config)
            elif filter_type == "date":
                filtered_df = self._apply_date_filter(filtered_df, column, filter_config)
            elif filter_type == "categorical":
                filtered_df = self._apply_categorical_filter(filtered_df, column, filter_config)
            elif filter_type == "text":
                filtered_df = self._apply_text_filter(filtered_df, column, filter_config)
        
        return filtered_df
    
    def _apply_range_filter(self, df: pd.DataFrame, column: str, filter_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply range filter
        """
        current_min = filter_config.get("current_min")
        current_max = filter_config.get("current_max")
        
        if current_min is not None:
            df = df[df[column] >= current_min]
        if current_max is not None:
            df = df[df[column] <= current_max]
        
        return df
    
    def _apply_date_filter(self, df: pd.DataFrame, column: str, filter_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply date filter
        """
        current_start = filter_config.get("current_start")
        current_end = filter_config.get("current_end")
        
        if current_start:
            start_date = pd.to_datetime(current_start)
            df = df[df[column] >= start_date]
        
        if current_end:
            end_date = pd.to_datetime(current_end)
            df = df[df[column] <= end_date]
        
        return df
    
    def _apply_categorical_filter(self, df: pd.DataFrame, column: str, filter_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply categorical filter
        """
        selected_values = filter_config.get("selected", [])
        
        if selected_values:
            df = df[df[column].astype(str).isin(selected_values)]
        
        return df
    
    def _apply_text_filter(self, df: pd.DataFrame, column: str, filter_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply text filter
        """
        search_value = filter_config.get("current_value", "")
        
        if search_value:
            df = df[df[column].astype(str).str.contains(search_value, case=False, na=False)]
        
        return df
    
    def get_filter_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary of available filters
        """
        filters = self.build_filters(df)
        
        summary = {
            "total_filters": len(filters),
            "filter_types": {},
            "columns_with_filters": list(filters.keys())
        }
        
        for column, filter_config in filters.items():
            filter_type = filter_config.get("type")
            if filter_type not in summary["filter_types"]:
                summary["filter_types"][filter_type] = 0
            summary["filter_types"][filter_type] += 1
        
        return summary
    
    def validate_filter_config(self, filter_config: Dict[str, Any]) -> bool:
        """
        Validate filter configuration
        """
        required_fields = {
            "range": ["type", "min", "max"],
            "date": ["type", "min_date", "max_date"],
            "categorical": ["type", "options"],
            "text": ["type", "placeholder"]
        }
        
        filter_type = filter_config.get("type")
        if filter_type not in required_fields:
            return False
        
        for field in required_fields[filter_type]:
            if field not in filter_config:
                return False
        
        return True 