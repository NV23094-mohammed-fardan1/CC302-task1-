# 🎯 TaskMaster Pro — ToDo App

A full-featured task management web application built with **Flask** and **SQLite**, containerized with Docker, and deployed via CI/CD pipelines on GitHub Actions.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Run Locally](#run-locally)
  - [Run with Docker](#run-with-docker)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Reference](#api-reference)
- [Branching Strategy](#branching-strategy)
- [DockerHub](#dockerhub)

---

## ✨ Features

- **Task Management** — Create, edit, delete, and complete tasks
- **Task Details** — Add descriptions, categories, priorities, due dates, and tags
- **Filtering & Search** — Filter tasks by category, priority, and status; full-text search
- **Dashboard Stats** — Live statistics: total, completed, pending, overdue, and due-today counts
- **Productivity Chart** — 7-day completion chart powered by Chart.js
- **Priority Levels** — High / Medium / Low with visual indicators
- **Categories** — Work, Personal, Study, Health, Finance, Shopping, Other
- **Export** — Download tasks as JSON or CSV
- **Dark/Light Theme** — Toggle between themes
- **Keyboard Shortcuts** — `Ctrl+K` (search), `Ctrl+N` (new task), `Esc` (clear filters)
- **Live Clock** — Real-time date/time display in sidebar
- **Responsive UI** — Bootstrap 5 with animated stat cards and task list

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3.1, Flask-SQLAlchemy |
| Database | SQLite (via SQLAlchemy ORM) |
| Frontend | HTML5, Bootstrap 5, Bootstrap Icons, Chart.js |
| Templating | Jinja2 |
| Testing | pytest |
| Linting | flake8 |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## 📁 Project Structure

```
CC302-task1/
├── app.py                  # Main Flask application & routes
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── .dockerignore
├── .gitignore
├── tests/
│   └── test_app.py         # Smoke tests
├── templates/
│   ├── base.html           # Base layout (sidebar, navbar, JS)
│   ├── index.html          # Main dashboard & task list
│   └── edit.html           # Edit task page
└── static/
    └── style.css           # Custom styles
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip
- Docker (optional)

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/NV23094-mohammed-fardan1/CC302-task1-.git
cd CC302-task1-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open your browser at **http://localhost:5000**

### Run Tests

```bash
pytest tests/ -v
```

### Run Linting

```bash
flake8 . --count --max-line-length=120 --statistics
```

---

## 🐳 Run with Docker

```bash
# Build the image
docker build -t todo-app .

# Run the container
docker run -p 5000:5000 todo-app
```

Or pull directly from DockerHub:

```bash
docker pull nv23094mohammedfardan/todo-app:latest
docker run -p 5000:5000 nv23094mohammedfardan/todo-app:latest
```

---

## ⚙️ CI/CD Pipeline

### Continuous Integration (`ci.yml`)

Triggered on every push or pull request to `main` or `dev`.

| Step | Action |
|---|---|
| Checkout | Pulls latest code |
| Setup Python | Installs Python 3.11 |
| Install deps | `pip install -r requirements.txt` |
| Lint | `flake8` with max line length 120 |
| Test | `pytest tests/ -v` |

### Continuous Delivery (`cd.yml`)

Triggered on a published **GitHub Release**.

| Step | Action |
|---|---|
| Checkout | Pulls tagged code |
| Docker Buildx | Sets up multi-platform builder |
| DockerHub Login | Authenticates using repository secrets |
| Extract version | Strips `v` prefix from tag (e.g. `v2.0.2` → `2.0.2`) |
| Build & Push | Pushes `<version>` and `latest` tags to DockerHub |

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token |

---

## 📡 API Reference

### `GET /api/stats`

Returns task statistics and 7-day productivity data.

**Response:**

```json
{
  "stats": {
    "total": 15,
    "completed": 8,
    "pending": 7,
    "overdue": 2,
    "due_today": 1,
    "due_this_week": 4,
    "high_priority": 3,
    "medium_priority": 2,
    "low_priority": 2,
    "completion_rate": 53,
    "recent_completions": 5,
    "category_stats": { "Work": 5, "Personal": 3 }
  },
  "productivity": {
    "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "counts": [2, 0, 3, 1, 2, 0, 0]
  }
}
```

### Other Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Main dashboard with task list |
| POST | `/add` | Add a new task |
| GET | `/complete/<id>` | Toggle task completion |
| GET | `/delete/<id>` | Delete a task |
| GET/POST | `/edit/<id>` | View/update a task |

---

## 🌿 Branching Strategy

```
main
 └── dev
      ├── Features/Backend
      ├── Features/Frontend
      └── Features/Docker
```

- **`main`** — Stable production branch; receives releases from `dev`
- **`dev`** — Integration branch; all features merge here first
- **`Features/*`** — Isolated feature branches created from `dev`

Pull Requests flow: `Features/* → dev → main`

---

## 🐋 DockerHub

**Image:** [`nv23094mohammedfardan/todo-app`](https://hub.docker.com/r/nv23094mohammedfardan/todo-app)

| Tag | Description |
|---|---|
| `latest` | Most recent stable build |
| `2.0.2` | Release v2.0.2 |

---

## 📄 License

© Mohammed Fardan — All rights reserved.
