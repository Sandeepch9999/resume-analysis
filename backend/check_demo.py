"""
Quick script to check and fix demo account.
Run this before trying to login.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash, verify_password
from app.models.user import User

def check_and_fix_demo():
    """Check and fix demo account."""
    print("=" * 60)
    print("Demo Account Check & Fix")
    print("=" * 60)
    
    # Ensure tables exist
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables verified")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    db = SessionLocal()
    try:
        demo_email = "demo@project.com"
        demo_password = "Demo@123"
        
        # Check if user exists
        user = db.query(User).filter(User.email == demo_email).first()
        
        if not user:
            print(f"\n❌ Demo user NOT found - Creating now...")
            user = User(
                email=demo_email,
                hashed_password=get_password_hash(demo_password),
                full_name="Demo User",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ Demo user created!")
        else:
            print(f"\n✅ Demo user found")
            print(f"   Email: {user.email}")
            print(f"   Active: {user.is_active}")
        
        # Verify password
        if verify_password(demo_password, user.hashed_password):
            print(f"✅ Password verification: SUCCESS")
        else:
            print(f"⚠️  Password verification: FAILED - Resetting...")
            user.hashed_password = get_password_hash(demo_password)
            user.is_active = True
            db.commit()
            print(f"✅ Password reset successful!")
        
        # Final verification
        user = db.query(User).filter(User.email == demo_email).first()
        if user and user.is_active and verify_password(demo_password, user.hashed_password):
            print("\n" + "=" * 60)
            print("✅ Demo Account is Ready!")
            print("=" * 60)
            print(f"Email:    {demo_email}")
            print(f"Password: {demo_password}")
            print("=" * 60)
            return True
        else:
            print("\n❌ Demo account setup failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = check_and_fix_demo()
    if not success:
        print("\n⚠️  Please check the error above and try again.")
        sys.exit(1)

