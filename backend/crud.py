from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import models
from database import get_db
from schemas import (
    UserCreate, UserResponse, ProjectCreate, ProjectResponse,
    TaskCreate, TaskResponse, InvoiceCreate, InvoiceResponse,
    ClientHealthScore
)
from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def create_project(db: Session, project: ProjectCreate):
    db_project = models.Project(
        title=project.title,
        description=project.description,
        client_id=project.client_id,
        budget=project.budget,
        original_scope=project.original_scope,
        current_scope=project.current_scope or project.original_scope
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_scope(db: Session, project_id: int, new_scope: str, change_reason: str):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    old_scope = project.current_scope
    change_entry = f"[{datetime.now().isoformat()}] Changed from: {old_scope[:50]}... To: {new_scope[:50]}... Reason: {change_reason}\n"
    
    project.scope_changes = (project.scope_changes or "") + change_entry
    project.current_scope = new_scope
    project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(project)
    return project

def get_tasks(db: Session, project_id: Optional[int] = None):
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    return query.all()

def create_task(db: Session, task: TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        status=task.status,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, task_id: int, status: str):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    db.commit()
    db.refresh(task)
    return task

def get_invoices(db: Session, client_id: Optional[int] = None):
    query = db.query(models.Invoice)
    if client_id:
        query = query.filter(models.Invoice.client_id == client_id)
    return query.all()

def generate_invoice_number() -> str:
    return f"INV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

def create_invoice(db: Session, invoice: InvoiceCreate):
    db_invoice = models.Invoice(
        invoice_number=generate_invoice_number(),
        project_id=invoice.project_id,
        client_id=invoice.client_id,
        amount=invoice.amount,
        items=invoice.items,
        due_date=invoice.due_date,
        status="pending"
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def log_interaction(db: Session, client_id: int, project_id: int, interaction_type: str, notes: str):
    interaction = models.ClientInteraction(
        client_id=client_id,
        project_id=project_id,
        interaction_type=interaction_type,
        notes=notes
    )
    db.add(interaction)
    db.commit()
    return interaction

def calculate_client_health(db: Session, client_id: int) -> ClientHealthScore:
    client = db.query(models.User).filter(models.User.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    interactions = db.query(models.ClientInteraction).filter(
        models.ClientInteraction.client_id == client_id
    ).all()
    
    active_projects = db.query(models.Project).filter(
        models.Project.client_id == client_id,
        models.Project.status == "active"
    ).count()
    
    pending_invoices = db.query(models.Invoice).filter(
        models.Invoice.client_id == client_id,
        models.Invoice.status == "pending"
    ).count()
    
    total_interactions = len(interactions)
    
    score = 50
    if total_interactions > 10:
        score += 20
    elif total_interactions > 5:
        score += 10
    
    if pending_invoices == 0:
        score += 20
    elif pending_invoices <= 2:
        score += 10
    
    if active_projects > 0:
        score += 10
    
    score = min(100, max(0, score))
    
    if score >= 80:
        engagement = "high"
    elif score >= 50:
        engagement = "medium"
    else:
        engagement = "low"
    
    return ClientHealthScore(
        client_id=client_id,
        client_name=client.full_name,
        health_score=score,
        engagement_level=engagement,
        total_interactions=total_interactions,
        pending_invoices=pending_invoices,
        active_projects=active_projects
    )
