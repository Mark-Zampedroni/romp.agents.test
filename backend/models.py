from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class UserRole(str, enum.Enum):
    FREELANCER = "freelancer"
    CLIENT = "client"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default=UserRole.CLIENT)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="client")
    invoices = relationship("Invoice", back_populates="client")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    client_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="active")
    budget = Column(Float)
    original_scope = Column(Text)
    current_scope = Column(Text)
    scope_changes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    invoices = relationship("Invoice", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String, default="todo")
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    items = Column(Text)
    
    project = relationship("Project", back_populates="invoices")
    client = relationship("User", back_populates="invoices")

class ClientInteraction(Base):
    __tablename__ = "client_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    interaction_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
