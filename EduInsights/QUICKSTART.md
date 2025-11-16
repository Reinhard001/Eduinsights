# Quick Start Guide

## Get EduInsight Running in 5 Minutes

### Using Docker (Easiest)

```powershell
# 1. Start the containers
docker-compose up --build

# 2. In a new terminal, create admin user
docker-compose exec web python backend/manage.py createsuperuser

# 3. Train the model with sample data
docker-compose exec web python backend/ml/train_model.py --csv backend/students_sample.csv

# 4. Access the app
# Open browser: http://localhost:8000 (Beautiful landing page)
# Dashboard: http://localhost:8000 (Login first)
# Student list: http://localhost:8000/students/
# Admin panel: http://localhost:8000/admin
```

### Without Docker

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Set up database (ensure PostgreSQL is running)
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Train model
python ml/train_model.py --csv students_sample.csv

# 6. Run server
python manage.py runserver

# 7. Access at http://localhost:8000
```

## Explore the Frontend

1. **Visit Landing Page**: http://localhost:8000
   - Beautiful hero section with features
   - Learn about the system capabilities

2. **Login to Dashboard**: http://localhost:8000/admin (then return to home)
   - View statistics cards
   - See at-risk students
   - Check performance charts

3. **Browse Students**: http://localhost:8000/students/
   - Search by name or ID
   - Filter by status
   - View student cards

4. **Get Predictions**: Click any student → "Get Prediction"
   - See AI analysis
   - View probability charts
   - Read recommendations

## Test the API

```powershell
# List students
curl http://localhost:8000/api/students/

# Get prediction for student ID 1
curl http://localhost:8000/api/students/1/predict/
```

## Add Sample Data via Admin

1. Login to http://localhost:8000/admin
2. Click "Students" → "Add Student"
3. Create a student (e.g., ID: S001, Name: John Doe)
4. Click "Performance Records" → "Add Performance Record"
5. Fill in:
   - Student: John Doe
   - Term: Fall 2025
   - Attendance: 65
   - Avg Assignment: 55
   - Midterm: 50
   - Missing: 2
   - Participation: 60
   - LMS Hours: 3
6. Save and test prediction!

## Troubleshooting

**Can't connect to database?**
- Check PostgreSQL is running
- Verify credentials in `.env` file

**Model not found error?**
- Train the model first (step 3/5 above)

**Port 8000 in use?**
- Change port: `python manage.py runserver 8001`

**Import errors?**
- Activate virtual environment
- Reinstall: `pip install -r requirements.txt`

## Next Steps

- Read `README.md` for detailed documentation
- Check `USER_MANUAL.md` for usage instructions
- See `DEVELOPER_DOCS.md` for architecture details
- Review `PRESENTATION_CONTENT.md` for project overview

**Need help?** Open an issue or contact the development team.
