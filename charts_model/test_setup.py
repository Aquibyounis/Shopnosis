#!/usr/bin/env python3
"""
Test script to verify the FastAPI dashboard backend setup
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🔍 Testing imports...")
    
    try:
        from services.cleaner import DataCleaner
        print("✅ DataCleaner imported successfully")
        
        from services.viz_builder import VizBuilder
        print("✅ VizBuilder imported successfully")
        
        from services.filter_builder import FilterBuilder
        print("✅ FilterBuilder imported successfully")
        
        from services.kpi_builder import KPIBuilder
        print("✅ KPIBuilder imported successfully")
        
        from services.recommender import Recommender
        print("✅ Recommender imported successfully")
        
        from utils.layout import LayoutManager
        print("✅ LayoutManager imported successfully")
        
        from models.schemas import UploadResponse, DashboardResponse
        print("✅ Pydantic schemas imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_cleaning():
    """Test data cleaning functionality"""
    print("\n🧹 Testing data cleaning...")
    
    try:
        from services.cleaner import DataCleaner
        # Create sample data
        data = {
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'product': ['Laptop', 'Phone', 'Desk'],
            'sales': [1200.50, 800.00, 450.75],
            'quantity': [2, 1, 1]
        }
        df = pd.DataFrame(data)
        
        # Test cleaner
        cleaner = DataCleaner()
        cleaned_df = cleaner.clean_data(df)
        
        print(f"✅ Data cleaned successfully: {cleaned_df.shape}")
        print(f"   Numeric columns: {cleaner.numeric_columns}")
        print(f"   Categorical columns: {cleaner.categorical_columns}")
        print(f"   Date columns: {cleaner.date_columns}")
        
        return True
    except Exception as e:
        print(f"❌ Data cleaning error: {e}")
        return False

def test_chart_generation():
    """Test chart generation functionality"""
    print("\n📊 Testing chart generation...")
    
    try:
        from services.viz_builder import VizBuilder
        # Create sample data
        data = {
            'category': ['Electronics', 'Furniture', 'Electronics', 'Furniture'],
            'sales': [1200.50, 450.75, 800.00, 150.25],
            'profit': [300.25, 112.50, 200.00, 37.50]
        }
        df = pd.DataFrame(data)
        
        # Test viz builder
        viz_builder = VizBuilder()
        charts = viz_builder.build_all_charts(df)
        
        print(f"✅ Generated {len(charts)} charts")
        for chart in charts:
            print(f"   - {chart['type']}: {chart['title']}")
        
        return True
    except Exception as e:
        print(f"❌ Chart generation error: {e}")
        return False

def test_filter_generation():
    """Test filter generation functionality"""
    print("\n🔍 Testing filter generation...")
    
    try:
        from services.filter_builder import FilterBuilder
        # Create sample data
        data = {
            'category': ['Electronics', 'Furniture', 'Electronics', 'Furniture'],
            'sales': [1200.50, 450.75, 800.00, 150.25],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']
        }
        df = pd.DataFrame(data)
        
        # Test filter builder
        filter_builder = FilterBuilder()
        filters = filter_builder.build_filters(df)
        
        print(f"✅ Generated {len(filters)} filters")
        for column, filter_config in filters.items():
            print(f"   - {column}: {filter_config['type']}")
        
        return True
    except Exception as e:
        print(f"❌ Filter generation error: {e}")
        return False

def test_kpi_generation():
    """Test KPI generation functionality"""
    print("\n📈 Testing KPI generation...")
    
    try:
        from services.kpi_builder import KPIBuilder
        # Create sample data
        data = {
            'category': ['Electronics', 'Furniture', 'Electronics', 'Furniture'],
            'sales': [1200.50, 450.75, 800.00, 150.25],
            'profit': [300.25, 112.50, 200.00, 37.50]
        }
        df = pd.DataFrame(data)
        
        # Test KPI builder
        kpi_builder = KPIBuilder()
        kpis = kpi_builder.build_kpis(df)
        
        print(f"✅ Generated {len(kpis)} KPIs")
        for kpi in kpis:
            print(f"   - {kpi['title']}: {kpi['value']}")
        
        return True
    except Exception as e:
        print(f"❌ KPI generation error: {e}")
        return False

def test_recommendation_generation():
    """Test recommendation generation functionality"""
    print("\n🤖 Testing recommendation generation...")
    
    try:
        from services.recommender import Recommender
        # Create sample data
        data = {
            'category': ['Electronics', 'Furniture', 'Electronics', 'Furniture'],
            'sales': [1200.50, 450.75, 800.00, 150.25],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']
        }
        df = pd.DataFrame(data)
        
        # Test recommender
        recommender = Recommender()
        recommendations = recommender.generate_recommendations(df)
        
        print(f"✅ Generated {len(recommendations)} recommendations")
        for rec in recommendations:
            print(f"   - {rec['title']}: {rec['severity']}")
        
        return True
    except Exception as e:
        print(f"❌ Recommendation generation error: {e}")
        return False

def test_layout_organization():
    """Test layout organization functionality"""
    print("\n📱 Testing layout organization...")
    
    try:
        from utils.layout import LayoutManager
        # Create sample components
        charts = [
            {"type": "bar", "title": "Sales Chart", "data": {}, "config": {}}
        ]
        kpis = [
            {"id": "test_kpi", "title": "Total Sales", "value": 1000, "format": "number", "description": "Test", "color": "primary"}
        ]
        recommendations = [
            {"type": "trend", "title": "Test Recommendation", "description": "Test", "recommendation": "Test", "severity": "medium", "data": {}}
        ]
        
        # Test layout manager
        layout_manager = LayoutManager()
        layout = layout_manager.organize_layout(charts, kpis, recommendations)
        
        print(f"✅ Layout organized successfully")
        print(f"   Total components: {layout['total_components']}")
        print(f"   Sections: {len(layout['sections'])}")
        
        return True
    except Exception as e:
        print(f"❌ Layout organization error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 FastAPI Dashboard Backend - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_cleaning,
        test_chart_generation,
        test_filter_generation,
        test_kpi_generation,
        test_recommendation_generation,
        test_layout_organization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The backend is ready to use.")
        print("\nTo start the server, run:")
        print("   python main.py")
        print("\nThe API will be available at: http://localhost:8000")
        print("API documentation at: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 