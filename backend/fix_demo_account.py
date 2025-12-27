"""
Fix and verify demo account.
Run this script to check/create/reset the demo account.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash, verify_password
from app.models.user import User

def fix_demo_account():
    """Check, create, or reset demo account."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("=" * 60)
        print("Demo Account Setup")
        print("=" * 60)
        
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == "demo@project.com").first()
        
        demo_email = "demo@project.com"
        demo_password = "Demo@123"
        
        if demo_user:
            print(f"\n✅ Demo user found in database")
            print(f"   Email: {demo_email}")
            print(f"   Full Name: {demo_user.full_name}")
            print(f"   Is Active: {demo_user.is_active}")
            
            # Test password
            if verify_password(demo_password, demo_user.hashed_password):
                print(f"   ✅ Password verification: SUCCESS")
            else:
                print(f"   ⚠️  Password verification: FAILED")
                print(f"   🔄 Resetting password...")
                demo_user.hashed_password = get_password_hash(demo_password)
                demo_user.is_active = True
                db.commit()
                print(f"   ✅ Password reset successful!")
        else:
            print(f"\n❌ Demo user NOT found")
            print(f"   🔄 Creating demo user...")
            
            # Create demo user
            demo_user = User(
                email=demo_email,
                hashed_password=get_password_hash(demo_password),
                full_name="Demo User",
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"   ✅ Demo user created successfully!")
        
        print("\n" + "=" * 60)
        print("Demo Account Credentials")
        print("=" * 60)
        print(f"Email:    {demo_email}")
        print(f"Password: {demo_password}")
        print("=" * 60)
        
        # Verify login works
        print("\n🧪 Testing login...")
        test_user = db.query(User).filter(User.email == demo_email).first()
        if test_user and verify_password(demo_password, test_user.hashed_password):
            print("✅ Login test: SUCCESS - Demo account is ready!")
        else:
            print("❌ Login test: FAILED - Please check password hashing")
        
        print("\n✅ Demo account setup complete!")
        print("\nYou can now login with:")
        print(f"   Email: {demo_email}")
        print(f"   Password: {demo_password}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_demo_account()

