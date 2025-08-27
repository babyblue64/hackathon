#! /usr/bin/env python3

from sqlalchemy.orm import Session
from database import Role, get_db

def seed_roles(db: Session):
    role_names = ["Admin", "Officer", "Citizen"]
    for name in role_names:
        existing = db.query(Role).filter_by(RoleName=name).first()
        if not existing:
            db.add(Role(RoleName=name))
    db.commit()

db = next(get_db())

seed_roles(db)
