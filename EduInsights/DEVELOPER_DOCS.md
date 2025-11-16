# EduInsight - Developer Documentation

## Table of Contents
1. [Setup & Installation](#setup--installation)
2. [Architecture Overview](#architecture-overview)
3. [Database Schema](#database-schema)
4. [API Documentation](#api-documentation)
5. [ML Pipeline](#ml-pipeline)
6. [Deployment](#deployment)
7. [Testing](#testing)
8. [Contributing](#contributing)

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional but recommended)

### Quick Start with Docker

```powershell
# Clone the repository
cd c:\Users\Aureli\Desktop\EduInsights

# Start services
docker-compose up --build

# Create superuser (in new terminal)
docker-compose exec web python backend/manage.py createsuperuser

# Access at http://localhost:8000
```

### Local Development Setup

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up database (ensure PostgreSQL is running)
# Update .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## Architecture Overview

### Components

1. **Django Backend** (`backend/eduinsight/`)
   - Settings, URL routing, WSGI configuration
   - Handles authentication, request routing

2. **Students App** (`backend/students/`)
   - Models: Student, PerformanceRecord
   - Views: REST API endpoints
   - Serializers: Data transformation
   - Admin: Django admin interface

3. **ML Pipeline** (`backend/ml/`)
   - Training script: `train_model.py`
   - Model storage: `model_store/`
   - Inference: Integrated into Django views

4. **Database**
   - PostgreSQL for production
   - SQLite for quick local testing

### Request Flow

```
Client Request
    ↓
Django URL Router
    ↓
View Function/Class
    ↓
├─→ Database Query (PostgreSQL)
├─→ ML Model Inference (joblib)
└─→ Response Serialization
    ↓
JSON Response
```

---

## Database Schema

### Student Model
```python
- user: OneToOneField(User) - Link to Django auth
- student_id: CharField(50) - Unique identifier
- full_name: CharField(200)
- age: IntegerField (optional)
- gender: CharField(20) (optional)
```

### PerformanceRecord Model
```python
- student: ForeignKey(Student)
- term: CharField(50)
- attendance_rate: FloatField (0-100)
- avg_assignment_score: FloatField
- midterm_score: FloatField
- missing_assignments: IntegerField
- participation: FloatField
- lms_hours: FloatField
- final_grade: FloatField (optional)
- passed: BooleanField (optional)
- created_at: DateTimeField (auto)
```

### Relationships
- One Student → Many PerformanceRecords
- One User → One Student (optional)

---

## API Documentation

### Base URL
`http://localhost:8000/api/`

### Endpoints

#### List All Students
```http
GET /api/students/
```

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "S001",
    "full_name": "John Doe",
    "age": 20,
    "gender": "M",
    "records": [...]
  }
]
```

#### Get Student Details
```http
GET /api/students/{id}/
```

#### Create Student
```http
POST /api/students/
Content-Type: application/json

{
  "student_id": "S999",
  "full_name": "Jane Smith",
  "age": 21,
  "gender": "F"
}
```

#### Get Prediction
```http
GET /api/students/{id}/predict/
```

**Response:**
```json
{
  "student": "John Doe",
  "prediction": "0",
  "probabilities": [0.85, 0.15],
  "top_features": [
    ["avg_assignment_score", 0.35],
    ["attendance_rate", 0.28],
    ["midterm_score", 0.22]
  ],
  "recommendations": [
    "Focus on assignment practice: try 3 weekly practice problems...",
    "Attendance is low. Watch recorded lectures..."
  ]
}
```

### Error Responses

**No Performance Records:**
```json
{
  "error": "No performance records for student"
}
```

**Model Not Found:**
```json
{
  "error": "Model not found. Train model first."
}
```

---

## ML Pipeline

### Training Process

1. **Prepare CSV Data**
   - Required columns: all features + `passed` (0/1)
   - Clean data (no missing values in required fields)

2. **Run Training Script**
   ```powershell
   python backend/ml/train_model.py --csv backend/students_sample.csv
   ```

3. **Output**
   - Model saved to: `backend/ml/model_store/rf_model.joblib`
   - Training metrics printed to console

### Model Features

The model expects these features in order:
1. `attendance_rate` (0-100)
2. `avg_assignment_score` (0-100)
3. `midterm_score` (0-100)
4. `missing_assignments` (integer)
5. `participation` (0-100)
6. `lms_hours` (float)

### Inference

The model is loaded on-demand in the `predict` view:
```python
model = joblib.load(MODEL_PATH)
X = np.array([[attendance, assignment, midterm, missing, participation, hours]])
prediction = model.predict(X)
probabilities = model.predict_proba(X)
```

### Recommendation Logic

Recommendations are generated based on thresholds:
- Attendance < 75% → Attendance improvement
- Assignment score < 60% → Practice problems
- Midterm < 50% → Tutoring sessions
- LMS hours < 2 → Increase engagement

---

## Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` in environment variables
- [ ] Set `DEBUG=0`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (not SQLite)
- [ ] Set up HTTPS with SSL certificate
- [ ] Configure static file serving (WhiteNoise included)
- [ ] Set up logging and monitoring
- [ ] Create backup strategy for database
- [ ] Review security settings

### Docker Production Deployment

```powershell
# Build production image
docker-compose -f docker-compose.prod.yml build

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Environment Variables (Production)

```env
SECRET_KEY=<generate-strong-secret-key>
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
POSTGRES_DB=eduinsight_prod
POSTGRES_USER=eduinsight_prod
POSTGRES_PASSWORD=<strong-password>
POSTGRES_HOST=<production-db-host>
POSTGRES_PORT=5432
```

---

## Testing

### Running Tests

```powershell
# All tests
python manage.py test

# Specific app
python manage.py test students

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

Example test file: `students/tests.py`

```python
from django.test import TestCase
from .models import Student, PerformanceRecord

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id="TEST001",
            full_name="Test Student"
        )
    
    def test_student_creation(self):
        self.assertEqual(self.student.student_id, "TEST001")
        self.assertEqual(str(self.student), "Test Student (TEST001)")
```

---

## Contributing

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

### Git Workflow

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and commit: `git commit -m "Add new feature"`
3. Push branch: `git push origin feature/new-feature`
4. Create pull request

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

---

## Troubleshooting

### Common Issues

**Issue:** `psycopg2` installation fails
**Solution:** Install PostgreSQL development headers or use `psycopg2-binary`

**Issue:** Model file not found
**Solution:** Train the model first: `python ml/train_model.py --csv students_sample.csv`

**Issue:** Database connection refused
**Solution:** Check PostgreSQL is running and credentials in `.env` are correct

**Issue:** Port 8000 already in use
**Solution:** Kill the process or use a different port: `python manage.py runserver 8001`

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Support

For questions or issues:
- Open a GitHub issue
- Contact the development team
- Check the troubleshooting section

---

**Happy coding! 🚀**
