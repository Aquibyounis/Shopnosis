from typing import Dict, List, Any, Optional
import random

class LayoutManager:
    """
    Organizes charts, KPIs, and recommendations into dashboard sections
    """
    
    def __init__(self):
        self.layout_configs = {
            "kpi": {"width": 3, "height": 1},
            "chart": {"width": 6, "height": 2},
            "recommendation": {"width": 12, "height": 1}
        }
        
        self.section_priorities = {
            "kpis": 1,
            "charts": 2,
            "recommendations": 3
        }
    
    def organize_layout(self, charts: List[Dict[str, Any]], kpis: List[Dict[str, Any]], recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Organize all components into a structured layout
        """
        layout = {
            "sections": [],
            "total_components": len(charts) + len(kpis) + len(recommendations),
            "layout_type": "responsive_grid"
        }
        
        # Create KPI section
        if kpis:
            kpi_section = self._create_kpi_section(kpis)
            layout["sections"].append(kpi_section)
        
        # Create chart sections
        if charts:
            chart_sections = self._create_chart_sections(charts)
            layout["sections"].extend(chart_sections)
        
        # Create recommendations section
        if recommendations:
            recommendation_section = self._create_recommendation_section(recommendations)
            layout["sections"].append(recommendation_section)
        
        return layout
    
    def _create_kpi_section(self, kpis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create KPI section layout
        """
        # Group KPIs by priority/type
        grouped_kpis = self._group_kpis_by_type(kpis)
        
        return {
            "id": "kpi_section",
            "title": "Key Performance Indicators",
            "type": "kpi_grid",
            "priority": self.section_priorities["kpis"],
            "layout": {
                "columns": 4,
                "rows": max(1, len(kpis) // 4 + (1 if len(kpis) % 4 > 0 else 0)),
                "gap": "16px"
            },
            "components": [
                {
                    "id": kpi["id"],
                    "type": "kpi_card",
                    "data": kpi,
                    "position": {
                        "row": i // 4,
                        "col": i % 4,
                        "width": self.layout_configs["kpi"]["width"],
                        "height": self.layout_configs["kpi"]["height"]
                    }
                }
                for i, kpi in enumerate(kpis)
            ]
        }
    
    def _create_chart_sections(self, charts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create chart sections based on chart types
        """
        sections = []
        
        # Group charts by type
        grouped_charts = self._group_charts_by_type(charts)
        
        for chart_type, type_charts in grouped_charts.items():
            section = {
                "id": f"chart_section_{chart_type}",
                "title": f"{chart_type.replace('_', ' ').title()} Charts",
                "type": "chart_grid",
                "priority": self.section_priorities["charts"],
                "layout": {
                    "columns": 2,
                    "rows": max(1, len(type_charts) // 2 + (1 if len(type_charts) % 2 > 0 else 0)),
                    "gap": "20px"
                },
                "components": [
                    {
                        "id": f"chart_{i}",
                        "type": "chart",
                        "data": chart,
                        "position": {
                            "row": i // 2,
                            "col": i % 2,
                            "width": self.layout_configs["chart"]["width"],
                            "height": self.layout_configs["chart"]["height"]
                        }
                    }
                    for i, chart in enumerate(type_charts)
                ]
            }
            sections.append(section)
        
        return sections
    
    def _create_recommendation_section(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create recommendations section layout
        """
        # Sort recommendations by severity
        sorted_recommendations = sorted(recommendations, key=lambda x: self._get_severity_score(x.get("severity", "low")), reverse=True)
        
        return {
            "id": "recommendation_section",
            "title": "Business Insights & Recommendations",
            "type": "recommendation_list",
            "priority": self.section_priorities["recommendations"],
            "layout": {
                "columns": 1,
                "rows": len(recommendations),
                "gap": "12px"
            },
            "components": [
                {
                    "id": f"recommendation_{i}",
                    "type": "recommendation_card",
                    "data": recommendation,
                    "position": {
                        "row": i,
                        "col": 0,
                        "width": self.layout_configs["recommendation"]["width"],
                        "height": self.layout_configs["recommendation"]["height"]
                    }
                }
                for i, recommendation in enumerate(sorted_recommendations)
            ]
        }
    
    def _group_kpis_by_type(self, kpis: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group KPIs by their type/format
        """
        grouped = {}
        
        for kpi in kpis:
            kpi_format = kpi.get("format", "number")
            if kpi_format not in grouped:
                grouped[kpi_format] = []
            grouped[kpi_format].append(kpi)
        
        return grouped
    
    def _group_charts_by_type(self, charts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group charts by their type
        """
        grouped = {}
        
        for chart in charts:
            chart_type = chart.get("type", "unknown")
            if chart_type not in grouped:
                grouped[chart_type] = []
            grouped[chart_type].append(chart)
        
        return grouped
    
    def _get_severity_score(self, severity: str) -> int:
        """
        Get numeric score for severity level
        """
        severity_scores = {
            "high": 3,
            "medium": 2,
            "low": 1
        }
        return severity_scores.get(severity, 1)
    
    def create_custom_layout(self, components: List[Dict[str, Any]], layout_type: str = "grid") -> Dict[str, Any]:
        """
        Create custom layout for components
        """
        if layout_type == "grid":
            return self._create_grid_layout(components)
        elif layout_type == "list":
            return self._create_list_layout(components)
        elif layout_type == "masonry":
            return self._create_masonry_layout(components)
        else:
            return self._create_default_layout(components)
    
    def _create_grid_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create grid layout
        """
        return {
            "type": "grid",
            "columns": 3,
            "gap": "16px",
            "components": [
                {
                    "id": f"component_{i}",
                    "data": component,
                    "position": {
                        "row": i // 3,
                        "col": i % 3,
                        "width": 4,
                        "height": 2
                    }
                }
                for i, component in enumerate(components)
            ]
        }
    
    def _create_list_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create list layout
        """
        return {
            "type": "list",
            "direction": "vertical",
            "gap": "12px",
            "components": [
                {
                    "id": f"component_{i}",
                    "data": component,
                    "position": {
                        "row": i,
                        "col": 0,
                        "width": 12,
                        "height": 1
                    }
                }
                for i, component in enumerate(components)
            ]
        }
    
    def _create_masonry_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create masonry layout
        """
        return {
            "type": "masonry",
            "columns": 3,
            "gap": "16px",
            "components": [
                {
                    "id": f"component_{i}",
                    "data": component,
                    "position": {
                        "row": i // 3,
                        "col": i % 3,
                        "width": 4,
                        "height": random.randint(1, 3)  # Random height for masonry effect
                    }
                }
                for i, component in enumerate(components)
            ]
        }
    
    def _create_default_layout(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create default layout
        """
        return {
            "type": "default",
            "components": [
                {
                    "id": f"component_{i}",
                    "data": component,
                    "position": {
                        "row": i,
                        "col": 0,
                        "width": 12,
                        "height": 2
                    }
                }
                for i, component in enumerate(components)
            ]
        }
    
    def optimize_layout(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize layout for better performance and user experience
        """
        optimized_layout = layout.copy()
        
        # Optimize section order based on priority
        if "sections" in optimized_layout:
            optimized_layout["sections"].sort(key=lambda x: x.get("priority", 999))
        
        # Add responsive breakpoints
        optimized_layout["responsive"] = {
            "breakpoints": {
                "xs": {"max_width": 576, "columns": 1},
                "sm": {"max_width": 768, "columns": 2},
                "md": {"max_width": 992, "columns": 3},
                "lg": {"max_width": 1200, "columns": 4},
                "xl": {"min_width": 1201, "columns": 4}
            }
        }
        
        return optimized_layout
    
    def get_layout_summary(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of layout structure
        """
        summary = {
            "total_sections": len(layout.get("sections", [])),
            "total_components": layout.get("total_components", 0),
            "section_types": {},
            "component_types": {}
        }
        
        for section in layout.get("sections", []):
            section_type = section.get("type", "unknown")
            if section_type not in summary["section_types"]:
                summary["section_types"][section_type] = 0
            summary["section_types"][section_type] += 1
            
            for component in section.get("components", []):
                component_type = component.get("type", "unknown")
                if component_type not in summary["component_types"]:
                    summary["component_types"][component_type] = 0
                summary["component_types"][component_type] += 1
        
        return summary 