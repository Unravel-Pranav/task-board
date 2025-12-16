# TaskFlow - Smart Task Board 📋✨

A beautiful, full-stack task management application built with **FastAPI** (Python) and **React** with **Tailwind CSS**.

![TaskFlow Preview](https://via.placeholder.com/800x400/0f172a/22c55e?text=TaskFlow+Task+Board)

## ✨ Features

### Core Features
- ✅ **Add Tasks** - Create new tasks with priority levels
- 📋 **List Tasks** - View all tasks with beautiful UI
- ✔️ **Mark Complete** - Toggle task completion with satisfying animations
- 🗑️ **Delete Tasks** - Remove tasks you no longer need
- 📊 **Progress Tracking** - Visual progress ring and statistics

### Unique Features 🎯
- 🎉 **Confetti Celebration** - Celebrate when completing tasks!
- 🎨 **Priority System** - High/Medium/Low with color-coded badges
- 🔍 **Smart Filtering** - Filter by All/Pending/Completed
- 🌈 **Glass Morphism UI** - Modern, beautiful design
- ✨ **Smooth Animations** - Framer Motion powered transitions

## 🏗️ Architecture

### Backend (FastAPI - MVC Pattern)
```
backend/
├── models/          # Data models (Task)
│   └── task_model.py
├── schemas/         # Pydantic schemas for validation
│   └── task_schema.py
├── services/        # Business logic layer
│   └── task_service.py
├── repositories/    # Data access layer (in-memory storage)
│   └── task_repo.py
├── routers/         # API route definitions
│   └── task_router.py
└── main.py          # FastAPI application entry
```

### Frontend (React + Tailwind)
```
frontend/
├── src/
│   ├── App.jsx      # Main application component
│   ├── main.jsx     # React entry point
│   └── index.css    # Tailwind + custom styles
├── package.json
└── vite.config.js
```

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks with statistics |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get a specific task |
| PATCH | `/api/tasks/{id}` | Update a task |
| PATCH | `/api/tasks/{id}/toggle` | Toggle task completion |
| DELETE | `/api/tasks/{id}` | Delete a task |
| GET | `/api/tasks/stats` | Get task statistics |
| GET | `/api/health` | Health check endpoint |

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- Pydantic v2 for validation
- Uvicorn ASGI server

**Frontend:**
- React 18
- Tailwind CSS 3
- Framer Motion (animations)
- Canvas Confetti (celebrations)

## 📦 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- uv (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd task-board
```

2. **Install Python dependencies**
```bash
uv pip install -e .
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
```

4. **Run development servers**

Backend:
```bash
uvicorn backend.main:app --reload --port 8000
```

Frontend (in another terminal):
```bash
cd frontend
npm run dev
```

5. **Open in browser**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/api/docs

### Production Build

```bash
cd frontend
npm run build
cd ..
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## 🎨 Design Highlights

- **Glass Morphism** - Modern frosted glass effect
- **Gradient Accents** - Beautiful green-to-teal gradients
- **Floating Orbs** - Animated background elements
- **Micro-interactions** - Hover effects and animations
- **Responsive** - Works on all device sizes

## 📝 Assignment Requirements Checklist

- [x] Clean Python backend code (FastAPI)
- [x] Well-designed REST APIs
- [x] Frontend connected to backend
- [x] Visually clean and polished UI
- [x] Add task functionality
- [x] Task list with title, checkbox, delete
- [x] Progress indicator (percentage + visual ring)
- [x] Unique feature: Confetti celebrations + Priority system

## 🙏 Credits

Built with ❤️ for the assignment task.

---

**Author:** [Your Name]  
**Date:** December 2024

