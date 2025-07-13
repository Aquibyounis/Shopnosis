import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class KPIBuilder:
    """
    Builds KPI cards and business metrics
    """
    
    def __init__(self):
        self.kpi_types = {
            "sum": "sum",
            "average": "mean",
            "count": "count",
            "percentage": "percentage",
            "growth": "growth",
            "ratio": "ratio"
        }
    
    def build_kpis(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Build all possible KPIs for the dataset
        """
        kpis = []
        
        # Get column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Build basic KPIs
        kpis.extend(self._build_basic_kpis(df, numeric_cols))
        
        # Build categorical KPIs
        kpis.extend(self._build_categorical_kpis(df, categorical_cols, numeric_cols))
        
        # Build time-based KPIs
        if date_cols:
            kpis.extend(self._build_time_based_kpis(df, date_cols, numeric_cols))
        
        # Build derived KPIs
        kpis.extend(self._build_derived_kpis(df, numeric_cols))
        
        return kpis
    
    def _build_basic_kpis(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build basic KPIs for numeric columns
        """
        kpis = []
        
        for col in numeric_cols:
            # Total
            total_kpi = self._build_sum_kpi(df, col)
            if total_kpi:
                kpis.append(total_kpi)
            
            # Average
            avg_kpi = self._build_average_kpi(df, col)
            if avg_kpi:
                kpis.append(avg_kpi)
            
            # Count
            count_kpi = self._build_count_kpi(df, col)
            if count_kpi:
                kpis.append(count_kpi)
        
        return kpis
    
    def _build_categorical_kpis(self, df: pd.DataFrame, categorical_cols: List[str], numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build KPIs for categorical columns
        """
        kpis = []
        
        for cat_col in categorical_cols:
            # Top category by count
            top_category_kpi = self._build_top_category_kpi(df, cat_col)
            if top_category_kpi:
                kpis.append(top_category_kpi)
            
            # If we have numeric columns, build KPIs by category
            if numeric_cols:
                for num_col in numeric_cols:
                    category_sum_kpi = self._build_category_sum_kpi(df, cat_col, num_col)
                    if category_sum_kpi:
                        kpis.append(category_sum_kpi)
        
        return kpis
    
    def _build_time_based_kpis(self, df: pd.DataFrame, date_cols: List[str], numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build time-based KPIs
        """
        kpis = []
        
        for date_col in date_cols:
            if numeric_cols:
                for num_col in numeric_cols:
                    # Growth rate
                    growth_kpi = self._build_growth_kpi(df, date_col, num_col)
                    if growth_kpi:
                        kpis.append(growth_kpi)
                    
                    # Period comparison
                    period_kpi = self._build_period_comparison_kpi(df, date_col, num_col)
                    if period_kpi:
                        kpis.append(period_kpi)
        
        return kpis
    
    def _build_derived_kpis(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
        """
        Build derived KPIs (ratios, percentages, etc.)
        """
        kpis = []
        
        # Build ratio KPIs if we have at least 2 numeric columns
        if len(numeric_cols) >= 2:
            ratio_kpi = self._build_ratio_kpi(df, numeric_cols[0], numeric_cols[1])
            if ratio_kpi:
                kpis.append(ratio_kpi)
        
        # Build percentage KPIs
        for col in numeric_cols:
            percentage_kpi = self._build_percentage_kpi(df, col)
            if percentage_kpi:
                kpis.append(percentage_kpi)
        
        return kpis
    
    def _build_sum_kpi(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build sum KPI
        """
        try:
            total = df[column].sum()
            
            return {
                "id": f"sum_{column}",
                "title": f"Total {column.replace('_', ' ').title()}",
                "value": float(total),
                "format": "number",
                "description": f"Sum of all {column} values",
                "trend": None,
                "color": "primary"
            }
        except Exception as e:
            print(f"Error building sum KPI for {column}: {e}")
            return None
    
    def _build_average_kpi(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build average KPI
        """
        try:
            avg = df[column].mean()
            
            return {
                "id": f"avg_{column}",
                "title": f"Average {column.replace('_', ' ').title()}",
                "value": float(avg),
                "format": "number",
                "description": f"Average of {column} values",
                "trend": None,
                "color": "info"
            }
        except Exception as e:
            print(f"Error building average KPI for {column}: {e}")
            return None
    
    def _build_count_kpi(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build count KPI
        """
        try:
            count = len(df)
            
            return {
                "id": f"count_{column}",
                "title": f"Total Records",
                "value": int(count),
                "format": "number",
                "description": f"Total number of records",
                "trend": None,
                "color": "success"
            }
        except Exception as e:
            print(f"Error building count KPI for {column}: {e}")
            return None
    
    def _build_top_category_kpi(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build top category KPI
        """
        try:
            value_counts = df[column].value_counts()
            if len(value_counts) > 0:
                top_category = value_counts.index[0]
                top_count = value_counts.iloc[0]
                
                return {
                    "id": f"top_{column}",
                    "title": f"Top {column.replace('_', ' ').title()}",
                    "value": str(top_category),
                    "format": "text",
                    "description": f"Most common {column} ({top_count} occurrences)",
                    "trend": None,
                    "color": "warning"
                }
        except Exception as e:
            print(f"Error building top category KPI for {column}: {e}")
            return None
    
    def _build_category_sum_kpi(self, df: pd.DataFrame, cat_column: str, num_column: str) -> Optional[Dict[str, Any]]:
        """
        Build category sum KPI
        """
        try:
            grouped = df.groupby(cat_column)[num_column].sum()
            if len(grouped) > 0:
                top_category = grouped.idxmax()
                top_sum = grouped.max()
                
                return {
                    "id": f"sum_{num_column}_by_{cat_column}",
                    "title": f"Top {cat_column.replace('_', ' ').title()} by {num_column.replace('_', ' ').title()}",
                    "value": str(top_category),
                    "format": "text",
                    "description": f"Category with highest {num_column} sum ({top_sum:.2f})",
                    "trend": None,
                    "color": "primary"
                }
        except Exception as e:
            print(f"Error building category sum KPI: {e}")
            return None
    
    def _build_growth_kpi(self, df: pd.DataFrame, date_column: str, value_column: str) -> Optional[Dict[str, Any]]:
        """
        Build growth KPI
        """
        try:
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            
            # Group by date and calculate daily totals
            daily_totals = df_copy.groupby(df_copy[date_column].dt.date)[value_column].sum()
            
            if len(daily_totals) >= 2:
                # Calculate growth rate
                first_value = daily_totals.iloc[0]
                last_value = daily_totals.iloc[-1]
                
                if first_value != 0:
                    growth_rate = ((last_value - first_value) / first_value) * 100
                    
                    return {
                        "id": f"growth_{value_column}",
                        "title": f"{value_column.replace('_', ' ').title()} Growth",
                        "value": f"{growth_rate:.1f}%",
                        "format": "percentage",
                        "description": f"Growth rate from first to last date",
                        "trend": "up" if growth_rate > 0 else "down",
                        "color": "success" if growth_rate > 0 else "danger"
                    }
        except Exception as e:
            print(f"Error building growth KPI: {e}")
            return None
    
    def _build_period_comparison_kpi(self, df: pd.DataFrame, date_column: str, value_column: str) -> Optional[Dict[str, Any]]:
        """
        Build period comparison KPI
        """
        try:
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            
            # Split data into two periods
            mid_date = df_copy[date_column].median()
            period1 = df_copy[df_copy[date_column] < mid_date][value_column].sum()
            period2 = df_copy[df_copy[date_column] >= mid_date][value_column].sum()
            
            if period1 != 0:
                change_percentage = ((period2 - period1) / period1) * 100
                
                return {
                    "id": f"period_comparison_{value_column}",
                    "title": f"{value_column.replace('_', ' ').title()} Period Change",
                    "value": f"{change_percentage:.1f}%",
                    "format": "percentage",
                    "description": f"Change from first half to second half of period",
                    "trend": "up" if change_percentage > 0 else "down",
                    "color": "success" if change_percentage > 0 else "danger"
                }
        except Exception as e:
            print(f"Error building period comparison KPI: {e}")
            return None
    
    def _build_ratio_kpi(self, df: pd.DataFrame, column1: str, column2: str) -> Optional[Dict[str, Any]]:
        """
        Build ratio KPI
        """
        try:
            sum1 = df[column1].sum()
            sum2 = df[column2].sum()
            
            if sum2 != 0:
                ratio = sum1 / sum2
                
                return {
                    "id": f"ratio_{column1}_{column2}",
                    "title": f"{column1.replace('_', ' ').title()} / {column2.replace('_', ' ').title()}",
                    "value": f"{ratio:.2f}",
                    "format": "ratio",
                    "description": f"Ratio of {column1} to {column2}",
                    "trend": None,
                    "color": "info"
                }
        except Exception as e:
            print(f"Error building ratio KPI: {e}")
            return None
    
    def _build_percentage_kpi(self, df: pd.DataFrame, column: str) -> Optional[Dict[str, Any]]:
        """
        Build percentage KPI
        """
        try:
            total = df[column].sum()
            if total != 0:
                # Calculate percentage of total for each value
                percentages = (df[column] / total) * 100
                avg_percentage = percentages.mean()
                
                return {
                    "id": f"percentage_{column}",
                    "title": f"Average {column.replace('_', ' ').title()} %",
                    "value": f"{avg_percentage:.1f}%",
                    "format": "percentage",
                    "description": f"Average percentage contribution of {column}",
                    "trend": None,
                    "color": "secondary"
                }
        except Exception as e:
            print(f"Error building percentage KPI for {column}: {e}")
            return None
    
    def build_custom_kpi(self, df: pd.DataFrame, kpi_type: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Build custom KPI based on type and parameters
        """
        try:
            if kpi_type == "sum":
                return self._build_sum_kpi(df, kwargs.get("column"))
            elif kpi_type == "average":
                return self._build_average_kpi(df, kwargs.get("column"))
            elif kpi_type == "count":
                return self._build_count_kpi(df, kwargs.get("column"))
            elif kpi_type == "growth":
                return self._build_growth_kpi(df, kwargs.get("date_column"), kwargs.get("value_column"))
            else:
                return None
        except Exception as e:
            print(f"Error building custom {kpi_type} KPI: {e}")
            return None
    
    def get_kpi_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary of available KPIs
        """
        kpis = self.build_kpis(df)
        
        summary = {
            "total_kpis": len(kpis),
            "kpi_types": {},
            "columns_with_kpis": []
        }
        
        for kpi in kpis:
            kpi_id = kpi.get("id", "")
            if "sum_" in kpi_id:
                summary["kpi_types"]["sum"] = summary["kpi_types"].get("sum", 0) + 1
            elif "avg_" in kpi_id:
                summary["kpi_types"]["average"] = summary["kpi_types"].get("average", 0) + 1
            elif "count_" in kpi_id:
                summary["kpi_types"]["count"] = summary["kpi_types"].get("count", 0) + 1
            elif "growth_" in kpi_id:
                summary["kpi_types"]["growth"] = summary["kpi_types"].get("growth", 0) + 1
        
        return summary 