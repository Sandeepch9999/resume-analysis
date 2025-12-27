"""
Initialize database and create demo user.
Run this script once to set up the database and demo user.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash, verify_password
from app.models.user import User

def init_db():
    """Initialize database and create demo user."""
    print("=" * 60)
    print("Database Initialization")
    print("=" * 60)
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return
    
    db = SessionLocal()
    try:
        demo_email = "demo@project.com"
        demo_password = "Demo@123"
        
        # Check if demo user exists
        demo_user = db.query(User).filter(User.email == demo_email).first()
        
        if not demo_user:
            # Create demo user
            print(f"\n📝 Creating demo user...")
            demo_user = User(
                email=demo_email,
                hashed_password=get_password_hash(demo_password),
                full_name="Demo User",
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print("✅ Demo user created successfully!")
        else:
            print(f"\nℹ️  Demo user already exists")
            # Verify password works
            if verify_password(demo_password, demo_user.hashed_password):
                print("✅ Password verification: SUCCESS")
            else:
                print("⚠️  Password verification failed - resetting...")
                demo_user.hashed_password = get_password_hash(demo_password)
                demo_user.is_active = True
                db.commit()
                print("✅ Password reset successful!")
        
        print("\n" + "=" * 60)
        print("Demo Account Credentials")
        print("=" * 60)
        print(f"Email:    {demo_email}")
        print(f"Password: {demo_password}")
        print("=" * 60)
        print("\n✅ Database initialization complete!")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

