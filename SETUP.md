# Quick Setup Guide

## Prerequisites Installation

### 1. Install Python 3.9+
Download from: https://www.python.org/downloads/

### 2. Install Node.js 18+
Download from: https://nodejs.org/

### 3. Install PostgreSQL
Download from: https://www.postgresql.org/download/

Or use MySQL if preferred.

## Step-by-Step Setup

### Backend Setup

1. **Open terminal in project root**

2. **Navigate to backend:**
   ```bash
   cd backend
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

5. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE resume_analyzer;
   ```

7. **Create `.env` file in backend folder:**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/resume_analyzer
   SECRET_KEY=your-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   Replace `username` and `password` with your PostgreSQL credentials.

8. **Initialize database:**
   ```bash
   python init_db.py
   ```
   This creates tables and demo user (demo@project.com / Demo@123)

9. **Start backend server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. **Open new terminal in project root**

2. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

3. **Install Node packages:**
   ```bash
   npm install
   ```

4. **Start frontend server:**
   ```bash
   npm run dev
   ```

## Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Login Credentials

- Email: `demo@project.com`
- Password: `Demo@123`

## Troubleshooting

### Backend won't start
- Check if PostgreSQL is running
- Verify DATABASE_URL in .env file
- Ensure port 8000 is not in use

### Frontend won't start
- Check if Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Ensure port 3000 is not in use

### Database connection error
- Verify PostgreSQL is running
- Check database credentials in .env
- Ensure database `resume_analyzer` exists

