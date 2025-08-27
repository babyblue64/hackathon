#! /usr/bin/env python3

from database import Base, engine, get_db
from database import Role, User

# Create tables (optional if already migrated)
Base.metadata.create_all(bind=engine)

# Get a DB session
db = next(get_db())

# Print all roles
roles = db.query(Role).all()
for role in roles:
    print(f"RoleID: {role.RoleID}, RoleName: {role.RoleName}")

# Print demo admin user info
admin = db.query(User).filter_by(Email="admin@example.com").first()
if admin:
    print(f"Admin Name: {admin.Name}, RoleID: {admin.Role}")
else:
    print("Demo Admin user not found.")