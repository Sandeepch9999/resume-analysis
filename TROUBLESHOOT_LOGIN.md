# Troubleshooting Login Errors

## 🔍 Common Login Errors & Solutions

### Error: "Incorrect email or password"

**Solution:**
```bash
cd backend
python check_demo.py
```

This will:
- Check if demo user exists
- Create it if missing
- Reset password if broken
- Verify everything works

---

### Error: "User not found"

**Cause:** Demo user doesn't exist in database

**Solution:**
```bash
cd backend
python check_demo.py
```

Or manually:
```bash
python init_db.py
```

---

### Error: "Network Error" or "Connection Refused"

**Cause:** Backend server is not running

**Solution:**
```bash
cd backend
python run.py
```

Make sure you see:
```
Application startup complete
Uvicorn running on http://0.0.0.0:8000
```

---

### Error: "CORS policy" or "CORS error"

**Cause:** Frontend can't connect to backend

**Solution:**
1. Check backend is running on port 8000
2. Check frontend is running on port 3000
3. Verify CORS settings in `backend/main.py`

---

### Error: "Account is inactive"

**Cause:** User account is marked as inactive

**Solution:**
```bash
cd backend
python check_demo.py
```

This will activate the demo account.

---

## 🧪 Test Login Step-by-Step

### Step 1: Verify Backend is Running

```bash
# In backend directory
python run.py
```

Should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Check Demo Account

```bash
# In another terminal
cd backend
python check_demo.py
```

Should see:
```
✅ Demo Account is Ready!
Email:    demo@project.com
Password: Demo@123
```

### Step 3: Test API Directly

```bash
# Test with curl (if you have it)
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@project.com&password=Demo@123"
```

Should return a JSON with `access_token`.

### Step 4: Check Frontend

1. Open browser console (F12)
2. Try to login
3. Check for errors in console
4. Check Network tab for API calls

---

## 🔧 Quick Fix Commands

```bash
# Complete reset
cd backend
python check_demo.py    # Fix account
python run.py           # Start server
```

Then try login again.

---

## 📝 Debug Checklist

- [ ] Backend is running (port 8000)
- [ ] Frontend is running (port 3000)
- [ ] Database is connected (check .env)
- [ ] Demo user exists (run check_demo.py)
- [ ] Demo user is active
- [ ] Password is correct (Demo@123)
- [ ] No CORS errors in browser console
- [ ] API endpoint is accessible

---

## 🐛 Still Not Working?

1. **Check browser console** - Look for JavaScript errors
2. **Check network tab** - See what API calls are being made
3. **Check backend logs** - Look for Python errors
4. **Verify credentials** - Make sure you're using:
   - Email: `demo@project.com`
   - Password: `Demo@123` (case-sensitive!)

---

## 💡 Pro Tips

1. **Clear browser cache** - Sometimes old tokens cause issues
2. **Use incognito mode** - Test without cache/cookies
3. **Check database directly** - Verify user exists:
   ```python
   from app.core.database import SessionLocal
   from app.models.user import User
   db = SessionLocal()
   user = db.query(User).filter(User.email == "demo@project.com").first()
   print(user)
   ```

---

## ✅ Success Indicators

When login works, you should:
- See token in browser localStorage
- Redirect to dashboard
- See user info in header
- No errors in console

If all these work, login is successful!

