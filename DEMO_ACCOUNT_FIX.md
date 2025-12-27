# Demo Account Fix Guide

If the demo account is not working, follow these steps:

## 🔧 Quick Fix

### Step 1: Run the Fix Script

```bash
cd backend
python fix_demo_account.py
```

This will:
- ✅ Check if demo user exists
- ✅ Create demo user if missing
- ✅ Reset password if needed
- ✅ Verify login works

### Step 2: Verify Database

Make sure your database is set up:

```bash
cd backend
python init_db.py
```

### Step 3: Test Login

Test if login works:

```bash
cd backend
python test_login.py
```

(Requires backend to be running)

---

## 🐛 Common Issues & Solutions

### Issue 1: "User not found" or "Incorrect password"

**Solution:**
```bash
cd backend
python fix_demo_account.py
```

### Issue 2: Database connection error

**Solution:**
1. Check your `.env` file has correct `DATABASE_URL`
2. Make sure PostgreSQL/MySQL is running
3. Verify database exists

### Issue 3: Backend not running

**Solution:**
```bash
cd backend
python run.py
```

### Issue 4: Password hash mismatch

**Solution:**
The fix script will automatically reset the password. Run:
```bash
python fix_demo_account.py
```

---

## 📝 Manual Verification

### Check if demo user exists in database:

```python
# Run in Python shell
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == "demo@project.com").first()
print(f"User found: {user is not None}")
if user:
    print(f"Email: {user.email}")
    print(f"Is Active: {user.is_active}")
db.close()
```

### Test password verification:

```python
from app.core.security import verify_password, get_password_hash

# Test
hashed = get_password_hash("Demo@123")
print(f"Verification: {verify_password('Demo@123', hashed)}")
```

---

## ✅ Demo Account Credentials

- **Email:** `demo@project.com`
- **Password:** `Demo@123`

These credentials are displayed on the login page.

---

## 🔄 Complete Reset

If nothing works, completely reset:

```bash
cd backend

# 1. Drop and recreate database (CAUTION: deletes all data)
# Or just delete the demo user manually

# 2. Reinitialize
python init_db.py

# 3. Verify
python fix_demo_account.py
```

---

## 📞 Still Not Working?

1. Check backend logs for errors
2. Verify database connection
3. Check if user table exists
4. Verify password hashing is working
5. Check backend is running on port 8000

Run the fix script first - it will diagnose and fix most issues automatically!

