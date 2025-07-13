# 🚀 FastAPI Dashboard Backend

A powerful FastAPI backend for dynamic dashboard generation with automatic data analysis, visualization, and business insights.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Development](#development)

## ✨ Features

- **📊 Automatic Chart Generation**: Creates bar charts, line charts, histograms, scatter plots, and more using Plotly
- **📈 KPI Calculation**: Generates key performance indicators automatically
- **🔍 Smart Filtering**: Auto-detects and creates filters for categorical, numeric, and date columns
- **🤖 AI Insights**: Provides business recommendations and anomaly detection
- **📱 Responsive Layout**: Organizes dashboard components into responsive sections
- **🧹 Data Cleaning**: Automatically cleans and preprocesses uploaded CSV data
- **🎯 Type Detection**: Intelligently detects column types (numeric, categorical, date)

## 🏗️ Architecture

```
/backend
│
├── main.py                      # 🚀 FastAPI app entry point
│
├── routes/                      # 🌐 All API endpoints
│   └── dashboard.py             # /upload, /dashboard, /filters
│
├── services/                    # 🔧 Business logic & data engine
│   ├── cleaner.py               # Cleans, merges, formats CSV data
│   ├── viz_builder.py           # Builds all charts (Plotly: bar, line, heatmap, etc.)
│   ├── filter_builder.py        # Detects and generates filters from data
│   ├── kpi_builder.py           # Builds KPI cards (Sales, Profit, Margin)
│   └── recommender.py           # AI-based business recommendations
│
├── models/                      # 📦 Data models (optional)
│   └── schemas.py               # Pydantic schemas for requests/responses
│
├── utils/                       # 🧩 Reusable helpers
│   └── layout.py                # Organizes charts into dashboard sections
│
├── tests/                       # ✅ Unit testing
│   └── test_data.csv            # Sample input file
│
└── requirements.txt             # 📦 Python dependencies
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Shop_back_new
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📖 Usage

### 1. Upload CSV File

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@tests/test_data.csv"
```

**Response:**
```json
{
  "file_id": "file_1",
  "filename": "test_data.csv",
  "rows": 20,
  "columns": 7,
  "message": "File uploaded and processed successfully"
}
```

### 2. Get Available Filters

```bash
curl -X GET "http://localhost:8000/api/v1/filters/file_1"
```

**Response:**
```json
{
  "file_id": "file_1",
  "filters": {
    "sales": {
      "type": "range",
      "min": 150.25,
      "max": 1200.50,
      "current_min": 150.25,
      "current_max": 1200.50,
      "step": 10.5,
      "label": "Sales",
      "description": "Filter sales between 150.25 and 1200.50"
    },
    "category": {
      "type": "categorical",
      "options": [
        {"value": "Electronics", "label": "Electronics", "count": 10},
        {"value": "Furniture", "label": "Furniture", "count": 10}
      ],
      "selected": [],
      "label": "Category",
      "description": "Filter by category",
      "multi_select": true
    }
  },
  "message": "Filters generated successfully"
}
```

### 3. Generate Dashboard

```bash
curl -X POST "http://localhost:8000/api/v1/dashboard/file_1" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "sales": {
        "current_min": 500,
        "current_max": 1200
      }
    }
  }'
```

**Response:**
```json
{
  "file_id": "file_1",
  "charts": [
    {
      "type": "bar",
      "title": "Sales by Category",
      "data": { /* Plotly chart data */ },
      "config": {"displayModeBar": false}
    }
  ],
  "kpis": [
    {
      "id": "sum_sales",
      "title": "Total Sales",
      "value": 8500.25,
      "format": "number",
      "description": "Sum of all sales values",
      "trend": null,
      "color": "primary"
    }
  ],
  "recommendations": [
    {
      "type": "trend",
      "title": "Sales Trend Analysis",
      "description": "Sales shows a moderate increasing trend",
      "recommendation": "Consider scaling up operations",
      "severity": "medium",
      "data": {
        "trend_direction": "increasing",
        "change_percentage": 15.2,
        "strength": "moderate"
      }
    }
  ],
  "layout": {
    "sections": [
      {
        "id": "kpi_section",
        "title": "Key Performance Indicators",
        "type": "kpi_grid",
        "components": [ /* KPI components */ ]
      }
    ],
    "total_components": 8,
    "layout_type": "responsive_grid"
  },
  "message": "Dashboard generated successfully"
}
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/health` | GET | Health check endpoint |
| `/api/v1/upload` | POST | Upload CSV file for processing |
| `/api/v1/filters/{file_id}` | GET | Get available filters for dataset |
| `/api/v1/dashboard/{file_id}` | POST | Generate complete dashboard |

## 📁 Project Structure

| Path | Role |
|------|------|
| `main.py` | Starts the FastAPI server |
| `routes/dashboard.py` | Hosts `/upload`, `/dashboard`, and `/filters` APIs |
| `services/cleaner.py` | Cleans uploaded CSVs, detects types, handles nulls |
| `services/viz_builder.py` | Generates all visual charts using Plotly |
| `services/filter_builder.py` | Auto-detects filters (categorical, range, date) |
| `services/kpi_builder.py` | Calculates high-level metrics (KPI cards) |
| `services/recommender.py` | Creates AI business insights (optional) |
| `utils/layout.py` | Determines layout order of charts |
| `models/schemas.py` | Defines request and response structures using Pydantic |
| `tests/test_data.csv` | A test file for dev/testing |

## 🛠️ Development

### Running Tests

```bash
# Run with pytest (if installed)
pytest tests/

# Or run manually
python -m unittest discover tests
```

### Adding New Chart Types

1. Add new chart method in `services/viz_builder.py`
2. Update `build_all_charts()` method
3. Add corresponding schema in `models/schemas.py`

### Adding New KPI Types

1. Add new KPI method in `services/kpi_builder.py`
2. Update `build_kpis()` method
3. Add corresponding schema in `models/schemas.py`

### Adding New Filter Types

1. Add new filter method in `services/filter_builder.py`
2. Update `build_filters()` method
3. Add corresponding schema in `models/schemas.py`

## 🔧 Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Data Processing
MAX_FILE_SIZE=10485760  # 10MB
SUPPORTED_FORMATS=["csv"]
```

### Customizing Chart Styles

Edit `services/viz_builder.py` to customize chart configurations:

```python
self.chart_configs = {
    "bar": {"height": 400, "width": 600, "color": "blue"},
    "line": {"height": 400, "width": 600, "color": "green"},
    # Add more chart types...
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

**Made with ❤️ using FastAPI, Plotly, and Pandas** 