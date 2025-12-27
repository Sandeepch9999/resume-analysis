# AI-Based Resume Analyzer & Job Preparation Platform

A comprehensive full-stack AI web application that analyzes resumes against job descriptions, provides correction suggestions, identifies missing skills, and generates personalized job preparation roadmaps.

## 🚀 Features

- **Resume Analysis**: Upload and analyze PDF/DOCX resumes
- **Job Description Matching**: Compare resumes against job descriptions using AI/NLP
- **Match Scoring**: Get similarity scores and match classifications (Good/Partial/Poor Match)
- **Skill Gap Analysis**: Identify missing and present skills
- **Correction Suggestions**: Get actionable feedback to improve your resume
- **Job Preparation**: 
  - Personalized learning syllabus
  - Interview questions based on job requirements
  - Curated learning resources
- **Dashboard**: Visual analytics and insights
- **Reports**: Comprehensive analysis reports
- **Dark/Light Theme**: Modern UI with theme toggle
- **JWT Authentication**: Secure user authentication

## 🛠️ Tech Stack

### Frontend
- React.js 18
- Vite
- Tailwind CSS
- React Router
- Axios
- Recharts (for visualizations)

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL/MySQL
- JWT Authentication
- File upload handling

### AI/NLP
- TF-IDF Vectorization
- Cosine Similarity
- Skill extraction using keyword matching
- Resume text extraction (PDF/DOCX)

## 📁 Project Structure

```
resume-analysis/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, database, security
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── main.py           # FastAPI app entry point
│   ├── requirements.txt  # Python dependencies
│   └── init_db.py        # Database initialization script
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── context/      # React contexts (Auth, Theme)
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   ├── package.json
│   └── vite.config.js
├── ml/
│   ├── resume_parser.py      # Resume text extraction
│   ├── matcher.py            # Resume-JD matching logic
│   ├── skill_extractor.py    # Skill extraction
│   └── job_preparation.py    # Preparation content generation
└── README.md
```

## 🚦 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (or MySQL)
- pip
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyzer
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Initialize database:**
   ```bash
   python init_db.py
   ```
   This will create all tables and a demo user with credentials:
   - Email: `demo@project.com`
   - Password: `Demo@123`

6. **Run the backend server:**
   
   Option 1 (Recommended - handles Python path automatically):
   ```bash
   python run.py
   ```
   
   Option 2 (Manual):
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## 🔐 Demo Credentials

The application includes a demo account for testing:

- **Email**: `demo@project.com`
- **Password**: `Demo@123`

These credentials are displayed on the login page for easy access.

## 📖 Usage Guide

### 1. Login/Register
- Use the demo credentials or create a new account
- Demo credentials are clearly displayed on the login page

### 2. Upload Resume
- Navigate to "Resume Analyzer"
- Upload a PDF or DOCX resume file
- The system will extract text automatically

### 3. Create Job Description
- In the "Resume Analyzer" page, click "+ New JD"
- Enter job title, company (optional), and description
- Save the job description

### 4. Analyze Resume
- Select an uploaded resume
- Select a job description
- Click "Analyze Resume"
- View match score, skills analysis, and suggestions

### 5. View Job Preparation
- Navigate to "Job Preparation"
- Select an analysis result
- View personalized syllabus, interview questions, and learning resources

### 6. View Reports
- Navigate to "Reports"
- View all analysis results
- Click on any report to see detailed breakdown

## 🗄️ Database Schema

The application uses the following main tables:

- **users**: User accounts
- **resumes**: Uploaded resume files and extracted text
- **job_descriptions**: Job description entries
- **match_results**: Analysis results with similarity scores
- **skills**: Skill analysis (present/missing)
- **syllabus**: Learning syllabus topics
- **interview_questions**: Generated interview questions
- **learning_resources**: Curated learning resources

## 🔧 Configuration

### Backend Configuration
Edit `backend/app/core/config.py` or use environment variables in `.env` file.

### Frontend Configuration
The API URL can be configured in `frontend/src/services/api.js` or via environment variable `VITE_API_URL`.

## 🧪 Testing

### Backend API Testing
You can test the API using:
- FastAPI automatic docs: `http://localhost:8000/docs`
- Postman or similar tools

### Frontend Testing
The application includes error handling and loading states. Test with:
- Different resume formats (PDF, DOCX)
- Various job descriptions
- Theme switching
- Navigation between pages

## 🚀 Production Deployment

### Backend
1. Set proper `SECRET_KEY` in environment variables
2. Use a production database (PostgreSQL recommended)
3. Configure CORS for your frontend domain
4. Use a production ASGI server like Gunicorn with Uvicorn workers

### Frontend
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `dist` folder using a web server (Nginx, Apache, etc.)
3. Configure API URL in production environment

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Resumes
- `POST /api/resumes/upload` - Upload resume file
- `GET /api/resumes/` - Get all user resumes
- `GET /api/resumes/{id}` - Get specific resume

### Job Descriptions
- `POST /api/job-descriptions/` - Create job description
- `GET /api/job-descriptions/` - Get all job descriptions
- `GET /api/job-descriptions/{id}` - Get specific job description
- `DELETE /api/job-descriptions/{id}` - Delete job description

### Analysis
- `POST /api/analysis/analyze` - Analyze resume against JD
- `GET /api/analysis/results` - Get all analysis results
- `GET /api/analysis/results/{id}` - Get specific analysis result

## 🎨 UI Features

- **Glassmorphism Design**: Modern, glossy card-based UI
- **Dark/Light Theme**: Toggle between themes
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Header Navigation**: All navigation in header (no sidebar)
- **Visual Analytics**: Charts and graphs for insights

## 🤝 Contributing

This is a complete production-ready project suitable for:
- College final projects
- Portfolio showcase
- Recruiter evaluation
- Interview demonstrations

## 📄 License

This project is provided as-is for educational and portfolio purposes.

## 🐛 Troubleshooting

### Backend Issues
- Ensure PostgreSQL is running and accessible
- Check database connection string in `.env`
- Verify all Python dependencies are installed
- Check if port 8000 is available

### Frontend Issues
- Clear browser cache
- Check if backend is running on port 8000
- Verify API URL configuration
- Check browser console for errors

### Database Issues
- Run `python init_db.py` to recreate tables
- Ensure database user has proper permissions
- Check database connection string format

## 📧 Support

For issues or questions, please check:
1. Backend logs for API errors
2. Browser console for frontend errors
3. Database connection status
4. Environment variable configuration

---

**Built with ❤️ for recruiters and job seekers**

