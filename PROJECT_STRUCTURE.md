# Project Structure

```
resume-analysis/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/                      # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # Authentication endpoints
│   │   │   ├── resume.py             # Resume endpoints
│   │   │   ├── job_description.py   # Job description endpoints
│   │   │   ├── analysis.py           # Analysis endpoints
│   │   │   └── dependencies.py      # Auth dependencies
│   │   │
│   │   ├── core/                     # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # App configuration
│   │   │   ├── database.py           # Database setup
│   │   │   └── security.py            # JWT & password hashing
│   │   │
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   ├── match_result.py
│   │   │   ├── skill.py
│   │   │   ├── syllabus.py
│   │   │   ├── interview_question.py
│   │   │   └── learning_resource.py
│   │   │
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   └── match_result.py
│   │   │
│   │   └── services/                 # Business Logic
│   │       ├── __init__.py
│   │       ├── resume_service.py
│   │       └── analysis_service.py
│   │
│   ├── main.py                       # FastAPI app entry point
│   ├── run.py                        # Startup script with path setup
│   ├── init_db.py                    # Database initialization
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment variables template
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/               # Reusable components
│   │   │   ├── Header.jsx            # Navigation header
│   │   │   └── ProtectedRoute.jsx    # Route protection
│   │   │
│   │   ├── context/                  # React Contexts
│   │   │   ├── AuthContext.jsx       # Authentication context
│   │   │   └── ThemeContext.jsx      # Theme context
│   │   │
│   │   ├── pages/                    # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ResumeAnalyzer.jsx
│   │   │   ├── JobPreparation.jsx
│   │   │   ├── Reports.jsx
│   │   │   └── Profile.jsx
│   │   │
│   │   ├── services/                 # API services
│   │   │   └── api.js                # Axios configuration
│   │   │
│   │   ├── App.jsx                   # Main app component
│   │   ├── main.jsx                  # React entry point
│   │   └── index.css                  # Global styles
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── ml/                               # AI/NLP Logic
│   ├── __init__.py
│   ├── resume_parser.py              # PDF/DOCX text extraction
│   ├── matcher.py                    # Resume-JD matching (TF-IDF)
│   ├── skill_extractor.py            # Skill extraction logic
│   └── job_preparation.py            # Preparation content generation
│
├── README.md                          # Main documentation
├── SETUP.md                           # Quick setup guide
├── PROJECT_STRUCTURE.md               # This file
└── .gitignore                         # Git ignore rules
```

## Key Files Explained

### Backend
- **main.py**: FastAPI application entry point, sets up CORS, includes routers
- **init_db.py**: Creates database tables and demo user
- **app/core/**: Core functionality (database, security, config)
- **app/api/**: REST API endpoints
- **app/models/**: Database models (SQLAlchemy)
- **app/services/**: Business logic layer

### Frontend
- **App.jsx**: Main app component with routing
- **context/**: React contexts for global state (auth, theme)
- **pages/**: Individual page components
- **components/**: Reusable UI components

### ML
- **resume_parser.py**: Extracts text from PDF/DOCX files
- **matcher.py**: Implements TF-IDF and cosine similarity for matching
- **skill_extractor.py**: Extracts and matches skills
- **job_preparation.py**: Generates syllabus, questions, resources

## Data Flow

1. User uploads resume → **resume_parser.py** extracts text
2. User creates/selects JD → Stored in database
3. User triggers analysis → **matcher.py** calculates similarity
4. **skill_extractor.py** identifies missing/present skills
5. **job_preparation.py** generates preparation content
6. Results stored in database and displayed in frontend

