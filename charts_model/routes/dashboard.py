import os
import uuid
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Dict, Any, Optional
from services.cleaner import DataCleaner
from services.viz_builder import VizBuilder
from services.filter_builder import FilterBuilder
from services.kpi_builder import KPIBuilder
from services.recommender import Recommender
from utils.layout import LayoutManager
from models.schemas import DashboardResponse, FilterResponse, UploadResponse

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Map file_id to file path
file_registry: Dict[str, str] = {}

router = APIRouter()

def convert_ndarrays(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarrays(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarrays(i) for i in obj]
    else:
        return obj

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    print("[UPLOAD] Received file:", file.filename)
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    try:
        file_id = f"file_{uuid.uuid4().hex[:8]}"
        file_path = os.path.join(DATA_DIR, f"{file_id}.csv")
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        file_registry[file_id] = file_path
        df = pd.read_csv(file_path)
        cleaner = DataCleaner()
        cleaned_df = cleaner.clean_data(df)
        cleaned_df.to_csv(file_path, index=False)
        print(f"[UPLOAD] File saved as {file_path}, file_id={file_id}")
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            rows=cleaned_df.shape[0],
            columns=cleaned_df.shape[1],
            message="File uploaded and processed successfully"
        )
    except Exception as e:
        print("[UPLOAD][ERROR]", e)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/filters/{file_id}", response_model=FilterResponse)
async def get_filters(file_id: str):
    print(f"[FILTERS] file_id={file_id}")
    file_path = file_registry.get(file_id) or os.path.join(DATA_DIR, f"{file_id}.csv")
    if not os.path.exists(file_path):
        print(f"[FILTERS][ERROR] File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")
    try:
        df = pd.read_csv(file_path)
        filter_builder = FilterBuilder()
        filters = filter_builder.build_filters(df)
        print(f"[FILTERS] Generated filters for {file_id}")
        return FilterResponse(
            file_id=file_id,
            filters=filters,
            message="Filters generated successfully"
        )
    except Exception as e:
        print("[FILTERS][ERROR]", e)
        raise HTTPException(status_code=500, detail=f"Error generating filters: {str(e)}")

@router.post("/dashboard/{file_id}", response_model=DashboardResponse)
async def generate_dashboard(request: Request, file_id: str):
    print(f"[DASHBOARD] file_id={file_id}")
    file_path = file_registry.get(file_id) or os.path.join(DATA_DIR, f"{file_id}.csv")
    if not os.path.exists(file_path):
        print(f"[DASHBOARD][ERROR] File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")
    try:
        df = pd.read_csv(file_path)
        body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
        filters = body.get("filters") if isinstance(body, dict) else None
        print(f"[DASHBOARD] Filters: {filters}")
        if filters:
            df = apply_filters(df, filters)
        viz_builder = VizBuilder()
        kpi_builder = KPIBuilder()
        recommender = Recommender()
        layout_manager = LayoutManager()
        charts = viz_builder.build_all_charts(df)
        kpis = kpi_builder.build_kpis(df)
        recommendations = recommender.generate_recommendations(df)
        layout = layout_manager.organize_layout(charts, kpis, recommendations)
        # Convert all numpy arrays to lists for JSON serialization
        charts = convert_ndarrays(charts)
        kpis = convert_ndarrays(kpis)
        recommendations = convert_ndarrays(recommendations)
        layout = convert_ndarrays(layout)
        print(f"[DASHBOARD] Dashboard generated for {file_id}")
        return DashboardResponse(
            file_id=file_id,
            charts=charts,
            kpis=kpis,
            recommendations=recommendations,
            layout=layout,
            message="Dashboard generated successfully"
        )
    except Exception as e:
        print("[DASHBOARD][ERROR]", e)
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")

def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    print("[APPLY_FILTERS] Applying filters:", filters)
    filtered_df = df.copy()
    for column, filter_config in filters.items():
        if column in filtered_df.columns:
            if filter_config.get("type") == "range":
                min_val = filter_config.get("current_min", filter_config.get("min"))
                max_val = filter_config.get("current_max", filter_config.get("max"))
                if min_val is not None:
                    filtered_df = filtered_df[filtered_df[column] >= min_val]
                if max_val is not None:
                    filtered_df = filtered_df[filtered_df[column] <= max_val]
            elif filter_config.get("type") == "categorical":
                values = filter_config.get("selected") or filter_config.get("values", [])
                if values:
                    filtered_df = filtered_df[filtered_df[column].isin(values)]
            elif filter_config.get("type") == "date":
                start_date = filter_config.get("current_start") or filter_config.get("start_date")
                end_date = filter_config.get("current_end") or filter_config.get("end_date")
                if start_date:
                    filtered_df = filtered_df[filtered_df[column] >= start_date]
                if end_date:
                    filtered_df = filtered_df[filtered_df[column] <= end_date]
    print(f"[APPLY_FILTERS] Resulting shape: {filtered_df.shape}")
    return filtered_df 

@router.get("/files")
async def list_files():
    files = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".csv"):
            file_id = fname.replace(".csv", "")
            files.append({
                "file_id": file_id,
                "filename": fname,
            })
    return {"files": files}