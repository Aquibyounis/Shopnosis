from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import dashboard

app = FastAPI(
    title="Dashboard API",
    description="FastAPI backend for dynamic dashboard generation",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(dashboard.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Dashboard API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 