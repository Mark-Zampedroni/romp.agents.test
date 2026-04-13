# ClientFlow - Client Portal MVP

A full-stack client portal software for freelancers and consultants.

## Features

- **Freelancer Dashboard**: Overview of projects, clients, and revenue
- **Project Management**: Create and track projects with scope tracking
- **Scope Guardian**: Track scope changes vs original contract
- **Invoicing**: Create and manage invoices
- **Client Health Score**: AI-powered client engagement metrics

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: SQLite (development)

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:3000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## API Endpoints

- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create project
- `PUT /api/v1/projects/{id}/scope` - Update scope (Scope Guardian)
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/invoices` - List invoices
- `POST /api/v1/invoices` - Create invoice
- `GET /api/v1/clients/{id}/health` - Get client health score
- `POST /api/v1/clients/{id}/interactions` - Log client interaction

## Project Structure

```
repo/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── routes.py        # API routes
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.tsx      # Main React app
    │   ├── main.tsx     # Entry point
    │   └── index.css    # Styles
    ├── package.json
    └── vite.config.ts
```

## License

MIT
