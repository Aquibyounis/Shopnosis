import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
import re

class DataCleaner:
    """
    Handles data cleaning, type detection, and preprocessing
    """
    
    def __init__(self):
        self.numeric_columns = []
        self.categorical_columns = []
        self.date_columns = []
        self.text_columns = []
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main cleaning pipeline
        """
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Detect column types
        self._detect_column_types(cleaned_df)
        
        # Clean each column type
        cleaned_df = self._clean_numeric_columns(cleaned_df)
        cleaned_df = self._clean_categorical_columns(cleaned_df)
        cleaned_df = self._clean_date_columns(cleaned_df)
        cleaned_df = self._clean_text_columns(cleaned_df)
        
        # Handle missing values
        cleaned_df = self._handle_missing_values(cleaned_df)
        
        # Remove duplicates
        cleaned_df = cleaned_df.drop_duplicates()
        
        return cleaned_df
    
    def _detect_column_types(self, df: pd.DataFrame):
        """
        Automatically detect column types
        """
        for column in df.columns:
            # Skip if column is empty
            if df[column].isna().all():
                self.text_columns.append(column)
                continue
            
            # Try to detect numeric columns
            if self._is_numeric_column(df[column]):
                self.numeric_columns.append(column)
            # Try to detect date columns
            elif self._is_date_column(df[column]):
                self.date_columns.append(column)
            # Try to detect categorical columns
            elif self._is_categorical_column(df[column]):
                self.categorical_columns.append(column)
            else:
                self.text_columns.append(column)
    
    def _is_numeric_column(self, series: pd.Series) -> bool:
        """
        Check if column contains numeric data
        """
        # Try to convert to numeric
        try:
            pd.to_numeric(series, errors='coerce')
            # Check if at least 80% of non-null values are numeric
            numeric_count = pd.to_numeric(series, errors='coerce').notna().sum()
            total_count = series.notna().sum()
            return numeric_count / total_count > 0.8 if total_count > 0 else False
        except:
            return False
    
    def _is_date_column(self, series: pd.Series) -> bool:
        """
        Check if column contains date data
        """
        # Common date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        # Check if column name suggests date
        date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
        column_lower = series.name.lower()
        if any(keyword in column_lower for keyword in date_keywords):
            return True
        
        # Check sample values for date patterns
        sample_values = series.dropna().head(10)
        date_count = 0
        
        for value in sample_values:
            if pd.api.types.is_datetime64_any_dtype(series):
                date_count += 1
            elif isinstance(value, str):
                for pattern in date_patterns:
                    if re.match(pattern, str(value)):
                        date_count += 1
                        break
        
        return date_count / len(sample_values) > 0.7 if len(sample_values) > 0 else False
    
    def _is_categorical_column(self, series: pd.Series) -> bool:
        """
        Check if column is categorical
        """
        # Check if unique values are limited (categorical)
        unique_ratio = series.nunique() / len(series)
        return unique_ratio < 0.5 and series.nunique() < 50
    
    def _clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean numeric columns
        """
        for column in self.numeric_columns:
            if column in df.columns:
                # Convert to numeric, coercing errors to NaN
                df[column] = pd.to_numeric(df[column], errors='coerce')
                
                # Remove outliers using IQR method
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Replace outliers with NaN
                df.loc[(df[column] < lower_bound) | (df[column] > upper_bound), column] = np.nan
        
        return df
    
    def _clean_categorical_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean categorical columns
        """
        for column in self.categorical_columns:
            if column in df.columns:
                # Convert to string and strip whitespace
                df[column] = df[column].astype(str).str.strip()
                
                # Handle case variations
                df[column] = df[column].str.title()
                
                # Replace empty strings with NaN
                df[column] = df[column].replace(['', 'nan', 'None', 'null'], np.nan)
        
        return df
    
    def _clean_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean date columns
        """
        for column in self.date_columns:
            if column in df.columns:
                try:
                    # Try to parse dates
                    df[column] = pd.to_datetime(df[column], errors='coerce')
                except:
                    # If conversion fails, keep as is
                    pass
        
        return df
    
    def _clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean text columns
        """
        for column in self.text_columns:
            if column in df.columns:
                # Convert to string and strip whitespace
                df[column] = df[column].astype(str).str.strip()
                
                # Replace empty strings with NaN
                df[column] = df[column].replace(['', 'nan', 'None', 'null'], np.nan)
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values based on column type
        """
        for column in df.columns:
            if column in self.numeric_columns:
                # Fill numeric columns with median
                df[column] = df[column].fillna(df[column].median())
            elif column in self.categorical_columns:
                # Fill categorical columns with mode
                mode_value = df[column].mode()
                if not mode_value.empty:
                    df[column] = df[column].fillna(mode_value.iloc[0])
                else:
                    df[column] = df[column].fillna('Unknown')
            elif column in self.date_columns:
                # Fill date columns with forward fill then backward fill
                df[column] = df[column].fillna(method='ffill').fillna(method='bfill')
            else:
                # Fill text columns with 'Unknown'
                df[column] = df[column].fillna('Unknown')
        
        return df
    
    def get_column_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get information about cleaned columns
        """
        return {
            "numeric_columns": self.numeric_columns,
            "categorical_columns": self.categorical_columns,
            "date_columns": self.date_columns,
            "text_columns": self.text_columns,
            "total_columns": len(df.columns),
            "total_rows": len(df)
        } 