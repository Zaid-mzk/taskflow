# TaskFlow

A full-stack task and project management application built with React, Flask, MySQL-compatible TiDB Cloud, JWT authentication, Docker, and Vercel.

**By [Zaid Khan](https://www.linkedin.com/in/zaidkhan2703/)**

TaskFlow allows users to create projects, organize tasks, track task status, and securely manage their own data through authenticated REST APIs.

[![CI](https://github.com/Zaid-mzk/taskflow/actions/workflows/ci.yml/badge.svg)](https://github.com/Zaid-mzk/taskflow/actions/workflows/ci.yml)

**Live Demo:** [https://taskflow-mu-sand.vercel.app](https://taskflow-mu-sand.vercel.app)

**API Health:** [https://taskflow-api-omega.vercel.app/api/health](https://taskflow-api-omega.vercel.app/api/health)

**GitHub Repository:** [https://github.com/Zaid-mzk/taskflow](https://github.com/Zaid-mzk/taskflow)

---

## Screenshots

### Dashboard

![TaskFlow Dashboard](docs/screenshots/dashboard.png)

### Project & Task Management

![TaskFlow Project](docs/screenshots/project.png)

### Authentication

![TaskFlow Signup](docs/screenshots/signup.png)

---

## Features

- User signup and login with JWT-based authentication
- Protected API routes scoped to the authenticated user
- User-specific project ownership and task access
- Full project CRUD
- Full task CRUD
- Task status management: To Do, In Progress, Done
- Task filtering by status
- Project dashboard with task counts
- Input validation and cross-user access protection
- RESTful Flask API
- Automated backend tests with Pytest
- Dockerized development and production environments
- Nginx-based frontend serving in the Docker deployment
- GitHub Actions CI
- Cloud deployment using Vercel and TiDB Cloud

---

## Tech Stack

**Frontend**

- React
- Vite
- Tailwind CSS
- React Router
- Axios
- Vercel

**Backend**

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-JWT-Extended
- PyMySQL
- Vercel

**Database**

- TiDB Cloud Starter (MySQL-compatible database)

**Testing**

- Pytest

**DevOps & Deployment**

- Docker
- Docker Compose
- Nginx
- GitHub Actions
- Vercel
- TiDB Cloud

---

## Architecture

### Production Architecture

```text
                         HTTPS
                           │
                           ▼
                     ┌─────────────┐
                     │    User     │
                     └──────┬──────┘
                            │
                            ▼
               ┌────────────────────────┐
               │ React + Vite Frontend  │
               │ Hosted on Vercel       │
               └────────────┬───────────┘
                            │
                       REST API + JWT
                            │
                            ▼
               ┌────────────────────────┐
               │ Flask Backend          │
               │ REST API + JWT Auth    │
               │ Hosted on Vercel       │
               └────────────┬───────────┘
                            │
                        SQLAlchemy
                            │
                            ▼
               ┌────────────────────────┐
               │ TiDB Cloud Starter     │
               │ MySQL-compatible DB   │
               └────────────────────────┘
```

### Request Flow

```text
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
TiDB Cloud (MySQL-compatible)
```

The frontend reads its backend URL from the `VITE_API_URL` environment variable. Locally, it points to the Flask development API; in production, it points to the deployed Vercel backend.

### Authentication Flow

```text
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
Axios sends Authorization: Bearer <token>
      │
      ▼
Protected route checks JWT
      │
      ▼
User ID extracted and used to scope queries
```

Protected routes require a valid JWT. The authenticated user's ID is extracted from the token and used to scope project and task queries, preventing unauthorized cross-user access.

---

## API Reference

All endpoints are prefixed with `/api`.

Protected endpoints require:

```http
Authorization: Bearer <JWT_TOKEN>
```

### Authentication

```http
POST /api/auth/signup
POST /api/auth/login
```

### Projects

```http
GET    /api/projects
POST   /api/projects
GET    /api/projects/<project_id>
DELETE /api/projects/<project_id>
```

### Tasks

```http
GET    /api/projects/<project_id>/tasks
POST   /api/projects/<project_id>/tasks
PATCH  /api/tasks/<task_id>
DELETE /api/tasks/<task_id>
```

Tasks can be filtered by status:

```http
GET /api/projects/<project_id>/tasks?status=<todo|in_progress|done>
```

---

## Validation

The API validates user input and returns appropriate HTTP status codes with JSON error responses.

Validated cases include:

- Required signup fields
- Email format
- Minimum password length
- Duplicate emails and usernames
- Required project names
- Required task titles
- Supported task statuses
- Task due-date format
- Empty task titles during updates
- Unauthorized access to other users' resources

---

## Testing

The backend test suite covers:

- User authentication
- Protected routes
- Project CRUD
- Task CRUD
- Task status updates
- Task filtering
- Input validation
- Cross-user access protection

Run the tests locally:

```bash
cd backend
pytest -v
```

---

## Continuous Integration

GitHub Actions runs on every push to `main` and on pull requests targeting `main`.

Two jobs run in parallel:

**Backend Tests**

```text
Python 3.11

→ Install dependencies

→ Run Pytest
```

**Frontend Build**

```text
Node.js 20

→ Install dependencies

→ Build with Vite
```

This verifies backend tests and frontend production builds before changes are merged.

---

## Running Locally with Docker

### Prerequisites

- Docker Desktop
- Git

Clone the repository:

```bash
git clone https://github.com/Zaid-mzk/taskflow.git

cd taskflow
```

Start the application:

```bash
docker compose up --build
```

Local endpoints:

| Service | URL |
|---------|-----|
| Frontend | [http://localhost:5173](http://localhost:5173) |
| Backend | [http://localhost:5000/api](http://localhost:5000/api) |
| MySQL | localhost:3306 |

Stop the stack:

```bash
docker compose down
```

To remove containers and the local database volume:

```bash
docker compose down -v
```

---

## Running Without Docker

### Backend

```bash
cd backend

python -m venv venv
```

Activate the virtual environment:

```bash
# macOS / Linux

source venv/bin/activate

# Windows PowerShell

venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
# macOS / Linux

cp .env.example .env

# Windows PowerShell

Copy-Item .env.example .env
```

Configure the database connection and secret values in `.env`, then run:

```bash
python run.py
```

### Frontend

```bash
cd frontend

npm install
```

Create the environment file:

```bash
# macOS / Linux

cp .env.example .env

# Windows PowerShell

Copy-Item .env.example .env
```

Set `VITE_API_URL` to your local Flask API URL, then start the development server:

```bash
npm run dev
```

---

## Environment Variables

### Backend

Configure these values in `backend/.env` for local development and in the Vercel project environment settings for production:

```text
SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret>
DATABASE_URL=<your-database-connection-string>
```

The backend uses `DATABASE_URL` to connect to the MySQL-compatible database hosted on TiDB Cloud. Set the connection string according to the database provider's connection instructions. Do not commit credentials or secret values to Git.

### Frontend

Configure `frontend/.env` locally and the corresponding environment variable in Vercel for production:

```text
VITE_API_URL=https://taskflow-api-omega.vercel.app/api
```

For local development, set this to the URL of your local Flask API, for example `http://localhost:5000/api`, if that matches your local configuration.

Secrets and environment-specific configuration should not be committed to Git.

---

## Docker

The local environment runs three services through Docker Compose:

```text
React Frontend
      │
      ▼
Flask Backend
      │
      ▼
    MySQL
```

The production frontend Docker build uses a multi-stage process:

1. Node.js installs dependencies.
2. Vite generates the production `dist` output.
3. Nginx Alpine serves the generated frontend.

The Docker production build accepts `VITE_API_URL` as a build argument so the frontend communicates with the configured backend. The live deployment described below uses Vercel for the frontend and backend, with TiDB Cloud for the database.

---

## Project Structure

```text
taskflow/

├── .github/
│   └── workflows/
│       └── ci.yml

├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   └── tasks.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── __init__.py

│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_projects.py
│   │   └── test_tasks.py

│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py

├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx

│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js

├── docs/
│   └── screenshots/
│       ├── dashboard.png
│       ├── project.png
│       └── signup.png

├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Deployment

TaskFlow's live deployment uses Vercel for the frontend and Flask API, with TiDB Cloud Starter providing the MySQL-compatible database.

- **Frontend** — React + Vite application hosted on Vercel: [taskflow-mu-sand.vercel.app](https://taskflow-mu-sand.vercel.app)
- **Backend API** — Flask REST API hosted on Vercel: [taskflow-api-omega.vercel.app](https://taskflow-api-omega.vercel.app/api/health)
- **Database** — TiDB Cloud Starter, a MySQL-compatible database accessed by the backend through `DATABASE_URL`

The frontend uses `VITE_API_URL` to communicate with the deployed backend. The backend's environment settings include `DATABASE_URL`, `SECRET_KEY`, and `JWT_SECRET_KEY`. Configure these values in the relevant Vercel project settings; never commit their values to the repository.

The frontend and backend are deployed as separate Vercel projects. Deployment behavior depends on the Vercel project configuration and connected Git repository.

Vercel Hobby and TiDB Cloud Starter have plan and usage limits; availability and capacity are subject to each provider's current terms.

---

## Author

**Zaid Khan**

- GitHub: [@Zaid-mzk](https://github.com/Zaid-mzk)
- LinkedIn: [zaidkhan2703](https://www.linkedin.com/in/zaidkhan2703/)
- Email: zaid270803@gmail.com

---

## Purpose

TaskFlow is an end-to-end task and project management application covering REST API design, JWT authentication, relational data modeling, CRUD operations, input validation, automated testing, containerization, CI, and cloud deployment.

The live application is available at [taskflow-mu-sand.vercel.app](https://taskflow-mu-sand.vercel.app).
