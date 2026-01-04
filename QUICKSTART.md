# Land Truth Registry - Quick Start Guide

## 🚀 Start the Application

```bash
cd land_truth_mvp
docker-compose up --build
```

Wait for all services to start (about 30-60 seconds).

## 🌱 Seed Demo Data

In a new terminal:

```bash
docker-compose exec backend python seed_data.py
```

## 🌐 Access the Application

- **Frontend Dashboard**: http://localhost:8501
- **Backend API Docs**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000

## 🛑 Stop the Application

```bash
docker-compose down
```

To remove all data:

```bash
docker-compose down -v
```

## 📝 Quick Test

1. Open http://localhost:8501
2. Navigate to "Dashboard"
3. View the map with 3 demo assets
4. Select an asset to view its timeline
5. Try "Register Asset" to add a new property
6. Try "Log Evidence" to add proof for an asset

## 🔍 Verify Installation

```bash
# Check all services are running
docker-compose ps

# Check database tables
docker-compose exec db psql -U postgres -d land_registry -c "\dt"

# Test API
curl http://localhost:8000/assets/
```

## 📊 Git History

```bash
git log --oneline
```

Expected commits:
- build: finalize phase 1 mvp structure
- chore(seed): add zimbabwean demo data script
- feat(ui): implement timeline dashboard and registry forms
- feat(api): implement crud and genesis versioning logic
- feat(schemas): add pydantic validation models
- feat(db): implement immutable asset and evidence schemas
