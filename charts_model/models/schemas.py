from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Upload Response Schema
class UploadResponse(BaseModel):
    file_id: str = Field(..., description="Unique identifier for the uploaded file")
    filename: str = Field(..., description="Original filename")
    rows: int = Field(..., description="Number of rows in the dataset")
    columns: int = Field(..., description="Number of columns in the dataset")
    message: str = Field(..., description="Status message")

# Filter Schema
class FilterOption(BaseModel):
    value: str = Field(..., description="Filter option value")
    label: str = Field(..., description="Filter option label")
    count: int = Field(..., description="Count of records with this value")

class RangeFilter(BaseModel):
    type: str = Field("range", description="Filter type")
    min: float = Field(..., description="Minimum value")
    max: float = Field(..., description="Maximum value")
    current_min: float = Field(..., description="Current minimum value")
    current_max: float = Field(..., description="Current maximum value")
    step: float = Field(..., description="Step size for slider")
    label: str = Field(..., description="Filter label")
    description: str = Field(..., description="Filter description")

class DateFilter(BaseModel):
    type: str = Field("date", description="Filter type")
    min_date: str = Field(..., description="Minimum date")
    max_date: str = Field(..., description="Maximum date")
    current_start: str = Field(..., description="Current start date")
    current_end: str = Field(..., description="Current end date")
    label: str = Field(..., description="Filter label")
    description: str = Field(..., description="Filter description")

class CategoricalFilter(BaseModel):
    type: str = Field("categorical", description="Filter type")
    options: List[FilterOption] = Field(..., description="Available filter options")
    selected: List[str] = Field(default=[], description="Currently selected values")
    label: str = Field(..., description="Filter label")
    description: str = Field(..., description="Filter description")
    multi_select: bool = Field(default=True, description="Whether multiple selections are allowed")

class TextFilter(BaseModel):
    type: str = Field("text", description="Filter type")
    placeholder: str = Field(..., description="Placeholder text")
    label: str = Field(..., description="Filter label")
    description: str = Field(..., description="Filter description")
    current_value: str = Field(default="", description="Current search value")

# Filter Response Schema
class FilterResponse(BaseModel):
    file_id: str = Field(..., description="File identifier")
    filters: Dict[str, Union[RangeFilter, DateFilter, CategoricalFilter, TextFilter]] = Field(..., description="Available filters")
    message: str = Field(..., description="Status message")

# Chart Schema
class ChartData(BaseModel):
    type: str = Field(..., description="Chart type")
    title: str = Field(..., description="Chart title")
    data: Dict[str, Any] = Field(..., description="Chart data (Plotly format)")
    config: Dict[str, Any] = Field(default={"displayModeBar": False}, description="Chart configuration")

# KPI Schema
class KPIData(BaseModel):
    id: str = Field(..., description="KPI identifier")
    title: str = Field(..., description="KPI title")
    value: Union[float, int, str] = Field(..., description="KPI value")
    format: str = Field(..., description="Value format (number, percentage, text, etc.)")
    description: str = Field(..., description="KPI description")
    trend: Optional[str] = Field(None, description="Trend direction (up, down, stable)")
    color: str = Field(..., description="KPI color theme")

# Recommendation Schema
class RecommendationData(BaseModel):
    type: str = Field(..., description="Recommendation type")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Recommendation description")
    recommendation: str = Field(..., description="Actionable recommendation")
    severity: str = Field(..., description="Severity level (high, medium, low)")
    data: Dict[str, Any] = Field(..., description="Additional data for the recommendation")

# Layout Schema
class ComponentPosition(BaseModel):
    row: int = Field(..., description="Row position")
    col: int = Field(..., description="Column position")
    width: int = Field(..., description="Component width")
    height: int = Field(..., description="Component height")

class LayoutComponent(BaseModel):
    id: str = Field(..., description="Component identifier")
    type: str = Field(..., description="Component type")
    data: Union[ChartData, KPIData, RecommendationData] = Field(..., description="Component data")
    position: ComponentPosition = Field(..., description="Component position")

class SectionLayout(BaseModel):
    columns: int = Field(..., description="Number of columns")
    rows: int = Field(..., description="Number of rows")
    gap: str = Field(..., description="Gap between components")

class DashboardSection(BaseModel):
    id: str = Field(..., description="Section identifier")
    title: str = Field(..., description="Section title")
    type: str = Field(..., description="Section type")
    priority: int = Field(..., description="Section priority")
    layout: SectionLayout = Field(..., description="Section layout configuration")
    components: List[LayoutComponent] = Field(..., description="Section components")

class DashboardLayout(BaseModel):
    sections: List[DashboardSection] = Field(..., description="Dashboard sections")
    total_components: int = Field(..., description="Total number of components")
    layout_type: str = Field(..., description="Layout type")

# Dashboard Response Schema
class DashboardResponse(BaseModel):
    file_id: str = Field(..., description="File identifier")
    charts: List[ChartData] = Field(..., description="Generated charts")
    kpis: List[KPIData] = Field(..., description="Generated KPIs")
    recommendations: List[RecommendationData] = Field(..., description="Generated recommendations")
    layout: DashboardLayout = Field(..., description="Dashboard layout")
    message: str = Field(..., description="Status message")

# Error Response Schema
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")

# Health Check Schema
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    version: str = Field(default="1.0.0", description="API version")

# API Info Schema
class APIInfo(BaseModel):
    title: str = Field(default="Dashboard API", description="API title")
    description: str = Field(default="FastAPI backend for dynamic dashboard generation", description="API description")
    version: str = Field(default="1.0.0", description="API version")
    status: str = Field(default="running", description="API status")

# Filter Request Schema
class FilterRequest(BaseModel):
    filters: Dict[str, Any] = Field(..., description="Filter configuration to apply")

# Custom Chart Request Schema
class CustomChartRequest(BaseModel):
    chart_type: str = Field(..., description="Type of chart to create")
    x_column: Optional[str] = Field(None, description="X-axis column")
    y_column: Optional[str] = Field(None, description="Y-axis column")
    title: Optional[str] = Field(None, description="Chart title")

# Custom KPI Request Schema
class CustomKPIRequest(BaseModel):
    kpi_type: str = Field(..., description="Type of KPI to create")
    column: Optional[str] = Field(None, description="Column for KPI calculation")
    date_column: Optional[str] = Field(None, description="Date column for time-based KPIs")
    value_column: Optional[str] = Field(None, description="Value column for time-based KPIs")

# Custom Insight Request Schema
class CustomInsightRequest(BaseModel):
    insight_type: str = Field(..., description="Type of insight to generate")
    column: Optional[str] = Field(None, description="Column for analysis")
    date_column: Optional[str] = Field(None, description="Date column for time-based insights")
    value_column: Optional[str] = Field(None, description="Value column for time-based insights")
    numeric_cols: Optional[List[str]] = Field(None, description="Numeric columns for correlation analysis")

# Summary Response Schema
class SummaryResponse(BaseModel):
    file_id: str = Field(..., description="File identifier")
    total_rows: int = Field(..., description="Total number of rows")
    total_columns: int = Field(..., description="Total number of columns")
    column_types: Dict[str, int] = Field(..., description="Count of each column type")
    data_quality: Dict[str, Any] = Field(..., description="Data quality metrics")
    message: str = Field(..., description="Status message") 