#! /usr/bin/env python3

from sqlalchemy.orm import Session 
from database import User, Role, get_db
from auth import hash_password

def seed_demo_admin(db: Session):
    admin_role = db.query(Role).filter_by(RoleName="Admin").first()
    if not admin_role:
        raise Exception("Admin role not found. Run seed_roles first.")

    existing_admin = db.query(User).filter_by(Email="admin@example.com").first()
    if not existing_admin:
        password_hash = hash_password("Admin@123")
        demo_admin = User(
            Name="Demo Admin",
            Email="admin@example.com",
            Mobile="1234567890",
            PasswordHash=password_hash,
            Role=admin_role.RoleID
        )
        db.add(demo_admin)
        db.commit()

db = next(get_db())

seed_demo_admin(db)
