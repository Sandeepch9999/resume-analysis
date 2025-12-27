# Quick Fix for Demo Account

## 🚀 Fastest Solution (3 Steps)

### Step 1: Fix Demo Account
```bash
cd backend
python fix_demo_account.py
```

### Step 2: Start Backend
```bash
python run.py
```

### Step 3: Try Login
- Email: `demo@project.com`
- Password: `Demo@123`

---

## What the Fix Script Does

The `fix_demo_account.py` script will:
1. ✅ Check if demo user exists
2. ✅ Create demo user if missing
3. ✅ Reset password if broken
4. ✅ Verify password works
5. ✅ Show you the credentials

---

## If Still Not Working

### Check Backend is Running
```bash
# Should see: "Application startup complete"
# Should be accessible at: http://localhost:8000
```

### Check Database Connection
```bash
# Verify .env file has correct DATABASE_URL
cat backend/.env
```

### Test API Directly
```bash
# With backend running, test login endpoint
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@project.com&password=Demo@123"
```

Should return a token if working.

---

## Complete Reset

If nothing works:

```bash
cd backend

# 1. Fix account
python fix_demo_account.py

# 2. Initialize database
python init_db.py

# 3. Start server
python run.py
```

Then try login again!

---

## Demo Credentials

- **Email:** `demo@project.com`
- **Password:** `Demo@123`

These are shown on the login page UI.

