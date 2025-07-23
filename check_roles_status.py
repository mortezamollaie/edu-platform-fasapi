#!/usr/bin/env python3
"""
Script to check the current status of roles and permissions in the database.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.account import Role, Permission


def check_roles_and_permissions():
    """
    Display current roles and their permissions.
    """
    db: Session = SessionLocal()
    
    try:
        # Get all roles
        roles = db.query(Role).all()
        print(f"📋 Total Roles: {len(roles)}")
        print("=" * 60)
        
        for role in roles:
            print(f"\n🎭 Role: {role.name}")
            print(f"   ID: {role.id}")
            print(f"   Permissions ({len(role.permissions)}):")
            
            if role.permissions:
                for perm in role.permissions:
                    print(f"     ✓ {perm.name}")
            else:
                print(f"     ⚠️  No permissions assigned")
        
        # Get all permissions
        all_permissions = db.query(Permission).all()
        print(f"\n\n📝 Total Permissions: {len(all_permissions)}")
        print("=" * 60)
        
        for perm in all_permissions:
            # Count how many roles have this permission
            role_count = len(perm.roles)
            print(f"🔑 {perm.name} (used by {role_count} role(s))")
        
        # Check for orphaned permissions (not assigned to any role)
        orphaned_permissions = [perm for perm in all_permissions if not perm.roles]
        if orphaned_permissions:
            print(f"\n\n⚠️  Orphaned Permissions ({len(orphaned_permissions)}):")
            print("=" * 60)
            for perm in orphaned_permissions:
                print(f"🔓 {perm.name}")
        
        print("\n" + "=" * 60)
        print("✅ Database status check completed!")
        
    except Exception as e:
        print(f"❌ Error checking database: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🔍 Checking Roles and Permissions Status...")
    print("=" * 60)
    check_roles_and_permissions()
