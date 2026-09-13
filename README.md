# TaskFlow

A full-stack task and project management application built with React, Flask, MySQL, JWT authentication, Docker, and Railway.

TaskFlow allows users to create projects, organize tasks, manage task status, and securely access their own data through authenticated REST APIs.

[![CI](https://github.com/Zaid-mzk/taskflow/actions/workflows/ci.yml/badge.svg)](https://github.com/Zaid-mzk/taskflow/actions/workflows/ci.yml)

## Live Demo

**Production:**  
https://taskflow-production-bf08.up.railway.app

**Backend Health:**  
https://distinguished-eagerness-production-5caa.up.railway.app/api/health

## Features

- User signup and login
- JWT-based authentication
- Protected API routes
- User-specific project ownership
- User-specific task access
- Project creation, listing, retrieval, and deletion
- Task creation, listing, updating, and deletion
- Task status management
  - To Do
  - In Progress
  - Done
- Task filtering by status
- Project dashboard with task counts
- Input validation
- Cross-user access protection
- RESTful Flask API
- Automated backend tests with pytest
- Dockerized development environment
- Production Docker image for the frontend
- Nginx-based frontend serving
- GitHub Actions CI
- Railway production deployment
- Managed MySQL database

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- React Router
- Axios

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-JWT-Extended
- PyMySQL

### Database

- MySQL

### Testing

- Pytest

### DevOps

- Docker
- Docker Compose
- Nginx
- GitHub Actions
- Railway

## Architecture

### Production Architecture

```text
                         HTTPS
                           │
                           ▼
                ┌──────────────────────┐
                │   React + Vite       │
                │   Frontend           │
                │   Docker + Nginx     │
                │   Railway            │
                └──────────┬───────────┘
                           │
                           │ REST API
                           │ JWT
                           ▼
                ┌──────────────────────┐
                │   Flask Backend      │
                │   REST API           │
                │   JWT Authentication │
                │   Railway            │
                └──────────┬───────────┘
                           │
                           │ SQLAlchemy
                           ▼
                ┌──────────────────────┐
                │   MySQL Database     │
                │   Railway            │
                └──────────────────────┘
Request Flow
User
 │
 ▼
React Frontend
 │
 │ Axios + JWT
 ▼
Flask REST API
 │
 │ SQLAlchemy
 ▼
MySQL

The frontend uses the VITE_API_URL environment variable to determine the backend API URL.

For local development, the frontend can use the local Flask API.

For production, VITE_API_URL points to the deployed Railway backend.

Authentication & Authorization

TaskFlow uses JWT-based authentication for protected API routes.

Authentication Flow
Signup / Login
      │
      ▼
Flask validates credentials
      │
      ▼
JWT access token generated
      │
      ▼
Frontend stores token
      │
      ▼
Axios sends:
Authorization: Bearer <token>

Protected routes require a valid JWT.

The authenticated user's ID is extracted from the JWT and used to scope project access.

Project queries are restricted to projects owned by the authenticated user.

Task access is also checked through the task's owning project, preventing users from accessing or modifying another user's tasks.

API
Base API
/api
Authentication
POST /api/auth/signup
POST /api/auth/login
Projects
GET    /api/projects
POST   /api/projects
GET    /api/projects/<project_id>
DELETE /api/projects/<project_id>
Tasks
GET    /api/projects/<project_id>/tasks
POST   /api/projects/<project_id>/tasks
PATCH  /api/tasks/<task_id>
DELETE /api/tasks/<task_id>
Task Filtering
GET /api/projects/<project_id>/tasks?status=todo
GET /api/projects/<project_id>/tasks?status=in_progress
GET /api/projects/<project_id>/tasks?status=done

Protected endpoints require:

Authorization: Bearer <JWT_TOKEN>
Validation

The API validates important user input, including:

Required signup fields
Email format
Minimum password length
Duplicate email addresses
Duplicate usernames
Required project names
Required task titles
Supported task statuses
Task due-date format
Empty task titles during updates

Invalid requests return appropriate HTTP status codes and JSON error responses.

Testing

The backend includes automated pytest tests covering:

User signup
Duplicate registration handling
Authentication validation
User login
Invalid credentials
Protected routes
Project creation
Project retrieval
Project deletion
Project validation
Cross-user project access protection
Task creation
Task validation
Task status updates
Invalid task statuses
Task deletion
Task filtering

The current test suite contains:

17 tests

Run the test suite locally:

cd backend
pytest -v
Continuous Integration

GitHub Actions runs automatically for:

Pushes to main
Pull requests targeting main

The CI pipeline contains two jobs.

Backend Tests
Checkout repository
        ↓
Setup Python 3.11
        ↓
Install backend dependencies
        ↓
Run pytest
Frontend Build
Checkout repository
        ↓
Setup Node.js 20
        ↓
Install frontend dependencies
        ↓
Run Vite production build

This helps catch backend regressions and frontend build failures before changes are merged or deployed.

Docker

TaskFlow includes Docker configuration for local development and production deployment.

Local Docker Architecture
Docker Compose
     │
     ├── Frontend
     ├── Backend
     └── MySQL

The frontend and backend are containerized and communicate with the MySQL database through the Docker Compose network.

Production Frontend

The frontend uses a multi-stage Docker build.

Node.js
   │
   ├── Install dependencies
   ├── Build React application
   └── Generate dist/
            │
            ▼
      Nginx Alpine
            │
            ▼
     Serve production UI

The React application is built with Node.js and the generated production files are served by Nginx.

The frontend Docker build accepts VITE_API_URL as a build argument so the production React bundle can communicate with the deployed backend.

Environment Variables
Backend

Create:

backend/.env

based on:

backend/.env.example

Important configuration values include:

SECRET_KEY
JWT_SECRET_KEY
DATABASE_URL

For production, the backend uses the Railway-provided DATABASE_URL to connect to the managed MySQL database.

Local development can use the database configuration provided in the environment file.

Frontend

Create:

frontend/.env

based on:

frontend/.env.example

For production, the frontend requires:

VITE_API_URL=https://<backend-domain>/api

Environment-specific configuration and secrets should not be committed to Git.

Running Locally with Docker
Prerequisites
Docker Desktop
Git
Clone the Repository
git clone https://github.com/Zaid-mzk/taskflow.git
cd taskflow
Start the Application
docker compose up --build

Typical local endpoints:

Frontend: http://localhost:5173
Backend:  http://localhost:5000/api
MySQL:    localhost:3306
Stop the Application
docker compose down

To remove the containers and local database volume:

docker compose down -v

The -v option removes the local MySQL data volume.

Running Without Docker
Backend

Create a virtual environment:

cd backend
python -m venv venv

Windows PowerShell:

venv\Scripts\Activate.ps1

macOS/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create the environment file.

Windows PowerShell:

Copy-Item .env.example .env

macOS/Linux:

cp .env.example .env

Configure the database values in .env, then start Flask:

python run.py
Frontend

In another terminal:

cd frontend
npm install

Create the environment file.

Windows PowerShell:

Copy-Item .env.example .env

macOS/Linux:

cp .env.example .env

Start the Vite development server:

npm run dev
Project Structure
taskflow/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   └── tasks.py
│   │   │
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_projects.py
│   │   └── test_tasks.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.js
│   │   │   └── index.js
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── ProjectView.jsx
│   │   │   └── Signup.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
Deployment

TaskFlow is deployed using Railway.

Production Architecture
GitHub
  │
  │ Push to main
  ▼
Railway
  │
  ├── Frontend Service
  │     └── Docker + Nginx
  │
  ├── Backend Service
  │     └── Docker + Gunicorn
  │
  └── MySQL Service

The frontend and backend are deployed as separate Railway services.

The backend connects to the Railway MySQL service through the production DATABASE_URL.

The frontend uses the production VITE_API_URL to communicate with the deployed backend.

GitHub → Railway automatic deployments provide the deployment workflow whenever changes are pushed to the production branch.

Production Verification

The deployed application has been manually verified for:

User signup
User login
JWT authentication
Logout
Protected routes
Project CRUD operations
Task CRUD operations
Task status updates
Task filtering
Data persistence
Cross-user access protection
Frontend-to-backend communication
Backend-to-database communication
Screenshots

Screenshots of the production application can be added here.

Recommended screenshots:

Login page
Signup page
Dashboard
Project view
Task management
Task status filtering
Resume Highlights
Built a full-stack task and project management application using React, Flask, MySQL, JWT authentication, and RESTful APIs.
Implemented user-scoped authorization for projects and tasks, including cross-user access protection and input validation.
Containerized the application with Docker, configured a production Nginx frontend, implemented GitHub Actions CI, and deployed the frontend, backend, and MySQL database on Railway.
Future Improvements

Potential future improvements include:

Task assignment between users
Project member management
Pagination for large task collections
Search and advanced filtering
Task priorities
Due-date reminders
Activity history
Role-based authorization
Automated deployment verification
Expanded integration and end-to-end testing
License

This project was built as a portfolio project to demonstrate full-stack software engineering, REST API development, authentication, database integration, containerization, CI/CD, and cloud deployment.


### One correction from the previous version

I made the **production frontend Docker explanation more precise** this time: `VITE_API_URL` is passed into the Docker **build stage**, because that was the actual issue we encountered and fixed.

Now:

1. Replace the entire `README.md` with the content above.
2. Save it.
3. **Do not commit yet.**

Then tell me **`saved`**. We'll do one final README verification before committing it.