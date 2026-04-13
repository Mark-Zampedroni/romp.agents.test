from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: String
    role: str = "client"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    budget: Optional[float] = None
    original_scope: str
    current_scope: Optional[str] = None

class ProjectCreate(ProjectBase):
    client_id: int

class ProjectResponse(ProjectBase):
    id: int
    client_id: int
    status: str
    scope_changes: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskResponse(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    amount: float
    items: str
    due_date: Optional[datetime] = None

class InvoiceCreate(InvoiceBase):
    project_id: int
    client_id: int

class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    project_id: int
    client_id: int
    status: str
    issue_date: datetime
    
    class Config:
        from_attributes = True

class ClientHealthScore(BaseModel):
    client_id: int
    client_name: str
    health_score: float
    engagement_level: str
    total_interactions: int
    avg_response_time_hours: Optional[float] = None
    pending_invoices: int
    active_projects: int
