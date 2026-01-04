# Land Truth MVP

A Python-based Land Registry Management System with FastAPI backend and Streamlit frontend.

## Project Structure

```
land_truth_mvp/
├── backend/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

## Services

- **Database (db)**: PostgreSQL 15 on port 5432
- **Backend (backend)**: FastAPI application on port 8000
- **Frontend (frontend)**: Streamlit application on port 8501

## Getting Started

1. **Clone the repository**
   ```bash
   cd land_truth_mvp
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

3. **Build and start services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development

- Backend code goes in `./backend`
- Frontend code goes in `./frontend`
- Both services support hot-reload for development

## Stopping Services

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```
