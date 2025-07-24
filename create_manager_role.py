"""
Script to create a Manager role and assign all permissions to it.
This is a standalone script that connects to the database and sets up the manager role.
"""

import sys
import os
import argparse

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.account import Role, Permission
from app.models.user import User


def create_manager_role():
    """
    Create a Manager role and assign all existing permissions to it.
    If the role already exists, it will update it with all permissions.
    """
    db: Session = SessionLocal()
    
    try:
        # Check if Manager role already exists
        manager_role = db.query(Role).filter(Role.name == "Manager").first()
        
        if not manager_role:
            # Create Manager role
            manager_role = Role(name="Manager")
            db.add(manager_role)
            db.commit()
            db.refresh(manager_role)
            print("Manager role created successfully!")
        else:
            print("Manager role already exists. Updating permissions...")
        
        # Get all permissions
        all_permissions = db.query(Permission).all()
        
        if not all_permissions:
            print("No permissions found in the database. You may need to create permissions first.")
            return
        
        # Assign all permissions to the Manager role
        manager_role.permissions = all_permissions
        db.commit()
        db.refresh(manager_role)
        
        print(f"Manager role now has {len(all_permissions)} permissions:")
        for perm in all_permissions:
            print(f"   - {perm.name}")
        
        print("\nManager role setup completed successfully!")
        
    except Exception as e:
        print(f"Error creating manager role: {str(e)}")
        db.rollback()
    finally:
        db.close()


def create_default_permissions():
    """
    Create some default permissions if none exist.
    """
    db: Session = SessionLocal()
    
    default_permissions = [
        "read_users",
        "create_users", 
        "update_users",
        "delete_users",
        "manage_roles",
        "manage_permissions",
        "view_reports",
        "system_admin", 
        "manage_courses",
        "manage_chapters",
        "manage_lectures"
    ]
    
    try:
        existing_permissions = db.query(Permission).all()
        existing_names = [perm.name for perm in existing_permissions]
        
        created_count = 0
        for perm_name in default_permissions:
            if perm_name not in existing_names:
                new_permission = Permission(name=perm_name)
                db.add(new_permission)
                created_count += 1
        
        if created_count > 0:
            db.commit()
            print(f"Created {created_count} default permissions.")
        else:
            print("All default permissions already exist.")
            
    except Exception as e:
        print(f"Error creating default permissions: {str(e)}")
        db.rollback()
    finally:
        db.close()


def assign_manager_role_to_user(email: str):
    """
    Assign the Manager role to a user by their email address.
    """
    db: Session = SessionLocal()
    
    try:
        # Find the user by email
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"User with email '{email}' not found!")
            return False
        
        # Find the Manager role
        manager_role = db.query(Role).filter(Role.name == "Manager").first()
        
        if not manager_role:
            print("Manager role not found! Please create the Manager role first.")
            print("Run: python create_manager_role.py --create-permissions")
            return False
        
        # Check if user already has the Manager role
        if manager_role in user.roles:
            print(f"User '{email}' already has the Manager role!")
            return True
        
        # Assign Manager role to user
        user.roles.append(manager_role)
        db.commit()
        db.refresh(user)
        
        print(f"Manager role successfully assigned to user '{email}'!")
        print(f"   User now has {len(user.roles)} role(s):")
        for role in user.roles:
            print(f"   - {role.name}")
        
        return True
        
    except Exception as e:
        print(f"Error assigning manager role: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def interactive_assign_manager():
    """
    Interactive function to get email and assign manager role.
    """
    print("\nAssign Manager Role to User")
    print("=" * 40)
    
    email = input("Enter user email: ").strip()
    
    if not email:
        print("Email cannot be empty!")
        return
    
    if "@" not in email:
        print("Please enter a valid email address!")
        return
    
    print(f"\nAssigning Manager role to: {email}")
    success = assign_manager_role_to_user(email)
    
    if success:
        print("\nAssignment completed successfully!")
    else:
        print("\nAssignment failed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create Manager role and assign permissions or users")
    parser.add_argument("--create-permissions", action="store_true", 
                       help="Create all permissions and Manager role")
    parser.add_argument("--assign-user", type=str, 
                       help="Assign Manager role to a user by email")
    parser.add_argument("--interactive", action="store_true",
                       help="Interactive mode to assign Manager role")
    
    args = parser.parse_args()
    
    if args.create_permissions:
        print("Starting Manager Role Setup...")
        print("=" * 50)
        print("Creating default permissions first...")
        create_default_permissions()
        print()
        print("Creating manager role...")
        create_manager_role()
        print("=" * 50)
        print("Setup completed!")
    elif args.assign_user:
        assign_manager_role_to_user(args.assign_user)
    elif args.interactive:
        interactive_assign_manager()
    else:
        print("Manager Role Management Script")
        print("=" * 40)
        print("Usage:")
        print("  python create_manager_role.py --create-permissions")
        print("    Create all permissions and Manager role")
        print()
        print("  python create_manager_role.py --assign-user email@example.com")
        print("    Assign Manager role to a specific user")
        print()
        print("  python create_manager_role.py --interactive")
        print("    Interactive mode to assign Manager role")
