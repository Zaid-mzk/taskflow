# TaskFlow

A full-stack task and project management application inspired by tools like Trello and Asana. Users can create an account, manage projects, and organize tasks through status-based workflows.

## Tech Stack

* **Frontend:** React, Vite, Tailwind CSS, React Router
* **Backend:** Flask, Flask-SQLAlchemy, Flask-JWT-Extended
* **Database:** MySQL
* **Authentication:** JWT
* **Testing:** Pytest
* **Containerization:** Docker, Docker Compose
* **CI:** GitHub Actions

## Features

* JWT-based user signup and login
* Protected API routes
* User-specific project and task ownership
* Create, view, and delete projects
* Create, view, update, and delete tasks
* Task status management:

  * To Do
  * In Progress
  * Done
* Filter tasks by status
* Dashboard with per-project task counts
* RESTful backend API
* Automated backend tests
* Dockerized frontend, backend, and MySQL services
* GitHub Actions CI pipeline

## Architecture

```text
                    ┌────────────────────┐
                    │   React Frontend   │
                    │   Vite + Tailwind  │
                    └─────────┬──────────┘
                              │
                              │ REST API
                              │ JWT
                              ▼
                    ┌────────────────────┐
                    │   Flask Backend    │
                    │  REST API + Auth   │
                    └─────────┬──────────┘
                              │
                              │ SQLAlchemy
                              ▼
                    ┌────────────────────┐
                    │       MySQL        │
                    │   TaskFlow Data    │
                    └────────────────────┘
```

## Project Structure

```text
taskflow/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── models.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Running Locally with Docker

Docker Compose is the recommended way to run the complete application.

### Prerequisites

* Docker Desktop
* Git

### Start the application

```bash
git clone <your-repository-url>
cd taskflow

docker compose up --build
```

Once the containers are running:

* **Frontend:** http://localhost:5173
* **Backend API:** http://localhost:5000/api
* **MySQL:** localhost:3306

### Stop the application

```bash
docker compose down
```

The MySQL volume is preserved when using the command above.

To remove the containers **and** database volume:

```bash
docker compose down -v
```

> The `-v` option deletes the local MySQL data volume.

## Running Without Docker

### Backend

```bash
cd backend

python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

Update the database configuration in `.env`, then start Flask:

```bash
python run.py
```

### Frontend

In another terminal:

```bash
cd frontend
npm install
```

Create the environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Start the development server:

```bash
npm run dev
```

## Testing

The backend includes **17 automated pytest tests** covering authentication, authorization, projects, tasks, validation, status updates, filtering, and cross-user access protection.

Run the tests locally:

```bash
cd backend
pytest -v
```

Or run them through Docker:

```bash
docker compose up -d --build backend
docker compose exec backend pytest -v
```

Current test result:

```text
17 passed
```

### Test Coverage Includes

* Successful signup
* Duplicate email rejection
* Missing authentication fields
* Successful login
* Invalid password handling
* Protected route authentication
* Project creation and listing
* Project validation
* Individual project retrieval
* Project deletion
* Cross-user project access protection
* Task creation and listing
* Task validation
* Task status updates
* Invalid task status rejection
* Task deletion
* Task filtering by status

## API Overview

All API routes except signup and login require:

```text
Authorization: Bearer <JWT_TOKEN>
```

### Authentication

```text
POST /api/auth/signup
POST /api/auth/login
```

### Projects

```text
GET    /api/projects
POST   /api/projects
GET    /api/projects/<id>
DELETE /api/projects/<id>
```

### Tasks

```text
GET    /api/projects/<id>/tasks
POST   /api/projects/<id>/tasks
PATCH  /api/tasks/<id>
DELETE /api/tasks/<id>
```

Task filtering:

```text
GET /api/projects/<id>/tasks?status=todo
GET /api/projects/<id>/tasks?status=in_progress
GET /api/projects/<id>/tasks?status=done
```

## Security

TaskFlow uses JWT-based authentication for protected API routes.

Project and task access is scoped to the authenticated user, preventing one user from accessing another user's projects or tasks.

Development credentials are provided through Docker environment variables for local use. Production deployments should use securely generated secrets supplied through the hosting platform's environment-variable configuration rather than committing secrets to the repository.

## CI/CD

GitHub Actions is configured to run automatically on pushes.

The CI workflow:

1. Installs backend dependencies
2. Runs the pytest test suite
3. Builds the frontend

This helps catch backend regressions and frontend build failures before deployment.

## Deployment

Deployment is planned for a future stage.

Potential hosting architecture:

```text
Frontend → Vercel
Backend  → Render / Railway
Database → Managed MySQL provider
```

Once the application is deployed, this section will be updated with the actual production URLs.

## Screenshots / Demo

Coming soon.

After deployment, this section will include:

* Live application
* GitHub repository
* Dashboard screenshot
* Project/task management screenshot
* API/architecture overview

## Resume Highlights

Current project bullets:

* Built a full-stack task and project management application using React, Flask REST API, JWT authentication, and MySQL.
* Designed and implemented RESTful CRUD workflows for projects and tasks with user-level ownership and authorization checks.
* Containerized the frontend, backend, and MySQL database with Docker Compose and configured GitHub Actions CI to run automated tests and frontend builds.

After deployment, these bullets can be updated with measurable production results such as deployment URL, test coverage, performance, or usage metrics.

## License

This project is intended as a portfolio project.
