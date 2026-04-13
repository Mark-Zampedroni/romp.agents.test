from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import models, crud, os
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper function to serve index.html
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# Create app
app = FastAPI(title="ClientFlow API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], expose_headers=["*"], max_age=600)

# ============ API ROUTES ============

@app.get("/api/v1/projects")
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@app.post("/api/v1/projects")
def create_project(title: str, description: str = "", client_id: int = 1, budget: float = 0, original_scope: str = "", db: Session = Depends(get_db)):
    return crud.create_project(db, title, description, client_id, budget, original_scope)

@app.put("/api/v1/projects/{project_id}/scope")
def update_scope(project_id: int, new_scope: str, reason: str, db: Session = Depends(get_db)):
    return crud.update_scope(db, project_id, new_scope, reason)

@app.get("/api/v1/tasks")
def list_tasks(project_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_tasks(db, project_id)

@app.post("/api/v1/tasks")
def create_task(title: str, project_id: int, description: str = "", db: Session = Depends(get_db)):
    return crud.create_task(db, title, project_id, description)

@app.put("/api/v1/tasks/{task_id}/status")
def update_task(task_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_task_status(db, task_id, status)

@app.get("/api/v1/invoices")
def list_invoices(db: Session = Depends(get_db)):
    return crud.get_invoices(db)

@app.post("/api/v1/invoices")
def create_invoice(project_id: int, client_id: int, amount: float, items: str, db: Session = Depends(get_db)):
    return crud.create_invoice(db, project_id, client_id, amount, items)

@app.get("/api/v1/clients/{client_id}/health")
def get_client_health(client_id: int, db: Session = Depends(get_db)):
    return crud.calculate_client_health(db, client_id)

@app.post("/api/v1/clients/{client_id}/interactions")
def log_interaction(client_id: int, project_id: int, interaction_type: str, notes: str, db: Session = Depends(get_db)):
    return crud.log_interaction(db, client_id, project_id, interaction_type, notes)

@app.get("/api/v1/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/api/v1/users")
def create_user(email: str, full_name: str, password: str, role: str = "client", db: Session = Depends(get_db)):
    return crud.create_user(db, email, full_name, password, role)

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# ============ FRONTEND ROUTES ============

# Define all frontend routes explicitly BEFORE catch-all
frontend_routes = [
    "/",
    "/dashboard",
    "/projects",
    "/invoices",
    "/clients",
    "/settings",
]

for route in frontend_routes:
    app.add_api_route(route, serve_index, methods=["GET"], include_in_schema=False)

# Catch-all for any other non-API path (SPA routing)
@app.get("/{full_path:path}", include_in_schema=False)
def catch_all(full_path: str):
    # Don't serve index.html for API paths
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    return serve_index()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
