from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import crud
import models
from schemas import (
    UserCreate, UserResponse, ProjectCreate, ProjectResponse,
    TaskCreate, TaskResponse, InvoiceCreate, InvoiceResponse,
    ClientHealthScore
)

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()

@router.get("/projects", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db, skip=skip, limit=limit)

@router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}/scope", response_model=ProjectResponse)
def update_project_scope(project_id: int, new_scope: str, reason: str, db: Session = Depends(get_db)):
    return crud.update_scope(db, project_id=project_id, new_scope=new_scope, change_reason=reason)

@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(project_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_tasks(db, project_id=project_id)

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.put("/tasks/{task_id}/status", response_model=TaskResponse)
def update_task(task_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_task_status(db, task_id=task_id, status=status)

@router.get("/invoices", response_model=List[InvoiceResponse])
def list_invoices(client_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_invoices(db, client_id=client_id)

@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_invoice(db=db, invoice=invoice)

@router.get("/clients/{client_id}/health", response_model=ClientHealthScore)
def get_client_health(client_id: int, db: Session = Depends(get_db)):
    return crud.calculate_client_health(db, client_id=client_id)

@router.post("/clients/{client_id}/interactions")
def log_client_interaction(client_id: int, project_id: int, interaction_type: str, notes: str, db: Session = Depends(get_db)):
    return crud.log_interaction(db, client_id=client_id, project_id=project_id, interaction_type=interaction_type, notes=notes)
