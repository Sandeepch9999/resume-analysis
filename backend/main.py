import sys
from pathlib import Path

# Add project root to Python path to access ml module
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import auth, resume, job_description, analysis, preparation_plan

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Analyzer API",
    description="AI-Based Resume Analyzer & Job Preparation Platform",
    version="1.0.0"
)

# --- CORS CONFIGURATION (UPDATED) ---
# We use ["*"] to allow ALL connections. This fixes the Network Error.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(job_description.router)
app.include_router(analysis.router)
app.include_router(preparation_plan.router)

@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}