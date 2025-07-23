#!/usr/bin/env python3
"""
Script to clean up duplicate or unnecessary roles and permissions.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.account import Role, Permission


def clean_duplicate_roles():
    """
    Clean up duplicate roles, keeping the one with the most permissions.
    """
    db: Session = SessionLocal()
    
    try:
        # Get all roles
        roles = db.query(Role).all()
        
        # Group roles by name (case-insensitive)
        role_groups = {}
        for role in roles:
            name_lower = role.name.lower()
            if name_lower not in role_groups:
                role_groups[name_lower] = []
            role_groups[name_lower].append(role)
        
        duplicates_found = False
        
        for name_lower, role_list in role_groups.items():
            if len(role_list) > 1:
                duplicates_found = True
                print(f"🔍 Found {len(role_list)} roles with name '{name_lower}':")
                
                # Sort by number of permissions (descending)
                role_list.sort(key=lambda r: len(r.permissions), reverse=True)
                
                # Keep the first one (most permissions)
                keep_role = role_list[0]
                print(f"   ✅ Keeping: {keep_role.name} (ID: {keep_role.id}) with {len(keep_role.permissions)} permissions")
                
                # Delete the rest
                for role_to_delete in role_list[1:]:
                    print(f"   🗑️  Deleting: {role_to_delete.name} (ID: {role_to_delete.id}) with {len(role_to_delete.permissions)} permissions")
                    db.delete(role_to_delete)
                
                print()
        
        if duplicates_found:
            db.commit()
            print("✅ Duplicate roles cleaned up successfully!")
        else:
            print("ℹ️  No duplicate roles found.")
        
    except Exception as e:
        print(f"❌ Error cleaning duplicate roles: {str(e)}")
        db.rollback()
    finally:
        db.close()


def clean_duplicate_permissions():
    """
    Clean up duplicate permissions.
    """
    db: Session = SessionLocal()
    
    try:
        # Get all permissions
        permissions = db.query(Permission).all()
        
        # Group permissions by name (case-insensitive)
        perm_groups = {}
        for perm in permissions:
            name_lower = perm.name.lower()
            if name_lower not in perm_groups:
                perm_groups[name_lower] = []
            perm_groups[name_lower].append(perm)
        
        duplicates_found = False
        
        for name_lower, perm_list in perm_groups.items():
            if len(perm_list) > 1:
                duplicates_found = True
                print(f"🔍 Found {len(perm_list)} permissions with name '{name_lower}':")
                
                # Sort by number of roles using this permission (descending)
                perm_list.sort(key=lambda p: len(p.roles), reverse=True)
                
                # Keep the first one (most used)
                keep_perm = perm_list[0]
                print(f"   ✅ Keeping: {keep_perm.name} (ID: {keep_perm.id}) used by {len(keep_perm.roles)} roles")
                
                # For the others, transfer their roles to the kept permission, then delete
                for perm_to_delete in perm_list[1:]:
                    print(f"   🔄 Transferring roles from: {perm_to_delete.name} (ID: {perm_to_delete.id})")
                    
                    # Add roles from the permission being deleted to the kept permission
                    for role in perm_to_delete.roles:
                        if keep_perm not in role.permissions:
                            role.permissions.append(keep_perm)
                    
                    # Now delete the duplicate permission
                    print(f"   🗑️  Deleting: {perm_to_delete.name}")
                    db.delete(perm_to_delete)
                
                print()
        
        if duplicates_found:
            db.commit()
            print("✅ Duplicate permissions cleaned up successfully!")
        else:
            print("ℹ️  No duplicate permissions found.")
        
    except Exception as e:
        print(f"❌ Error cleaning duplicate permissions: {str(e)}")
        db.rollback()
    finally:
        db.close()


def clean_orphaned_permissions():
    """
    Remove permissions that are not assigned to any role.
    """
    db: Session = SessionLocal()
    
    try:
        # Get all permissions
        all_permissions = db.query(Permission).all()
        orphaned_permissions = [perm for perm in all_permissions if not perm.roles]
        
        if orphaned_permissions:
            print(f"🔍 Found {len(orphaned_permissions)} orphaned permissions:")
            
            for perm in orphaned_permissions:
                print(f"   🗑️  Deleting: {perm.name}")
                db.delete(perm)
            
            db.commit()
            print("✅ Orphaned permissions cleaned up successfully!")
        else:
            print("ℹ️  No orphaned permissions found.")
        
    except Exception as e:
        print(f"❌ Error cleaning orphaned permissions: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🧹 Starting Database Cleanup...")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "--roles":
            print("🎭 Cleaning duplicate roles...")
            clean_duplicate_roles()
        elif action == "--permissions":
            print("🔑 Cleaning duplicate permissions...")
            clean_duplicate_permissions()
        elif action == "--orphaned":
            print("🔓 Cleaning orphaned permissions...")
            clean_orphaned_permissions()
        elif action == "--all":
            print("🎭 Cleaning duplicate roles...")
            clean_duplicate_roles()
            print("\n🔑 Cleaning duplicate permissions...")
            clean_duplicate_permissions()
            print("\n🔓 Cleaning orphaned permissions...")
            clean_orphaned_permissions()
        else:
            print("❌ Invalid option. Use: --roles, --permissions, --orphaned, or --all")
    else:
        print("Usage:")
        print("  python cleanup_database.py --roles      # Clean duplicate roles")
        print("  python cleanup_database.py --permissions # Clean duplicate permissions")
        print("  python cleanup_database.py --orphaned   # Clean orphaned permissions")
        print("  python cleanup_database.py --all        # Clean everything")
    
    print("=" * 60)
    print("✨ Cleanup completed!")
