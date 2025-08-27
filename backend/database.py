from dotenv import load_dotenv
import os
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from datetime import datetime, timezone

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv('DB_URL')

if DB_URL:
    engine = create_engine(DB_URL)

class Base(DeclarativeBase):
    pass

class Role(Base):
    __tablename__ = 'roles'
    RoleID = Column(Integer, primary_key=True, autoincrement=True)
    RoleName = Column(String(50), nullable=False, unique=True)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(100), nullable=False, unique=True)
    Mobile = Column(String(15), nullable=False, unique=True)
    PasswordHash = Column(String(128), nullable=False)
    Role = Column(Integer, ForeignKey('roles.RoleID'), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.now(timezone.utc))

    role = relationship("Role", back_populates="users")
    service_requests = relationship("ServiceRequest", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class ServiceRequest(Base):
    __tablename__ = 'service_requests'
    RequestID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    ServiceType = Column(String(50), nullable=False)
    Description = Column(Text, nullable=True)
    FeeAmount = Column(Float, nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="service_requests")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    LogID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    Action = Column(String(255), nullable=False)
    Timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="audit_logs")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()