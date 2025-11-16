# EduInsight — AI-Powered Student Performance Prediction System

![EduInsight](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange)

## 🎯 Overview

**EduInsight** is an AI-powered system that predicts student performance and provides personalized study recommendations. Built with Django and scikit-learn, it helps educators identify at-risk students early and suggests targeted interventions.

### Key Features

- 📊 **Performance Prediction**: Predict pass/fail probability using machine learning
- 🎯 **Personalized Recommendations**: Rule-based study suggestions tailored to each student
- 📈 **Explainable AI**: See which factors contribute most to predictions
- 👥 **Teacher Dashboard**: View at-risk students and cohort analytics
- 📁 **CSV Upload**: Bulk import student performance data
- 🔌 **REST API**: Easy integration with other systems

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────────┐
│   Web UI        │────────▶│   Django Backend     │
│ (Students &     │         │   + REST API         │
│  Teachers)      │◀────────│                      │
└─────────────────┘         └──────────┬───────────┘
                                       │
                            ┌──────────┼───────────┐
                            │          │           │
                      ┌─────▼────┐ ┌──▼───────┐ ┌─▼────────┐
                      │PostgreSQL│ │ML Model  │ │File      │
                      │          │ │(RF)      │ │Storage   │
                      └──────────┘ └──────────┘ └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+ and PostgreSQL

### Option 1: Using Docker (Recommended)

1. **Clone and navigate to the project**:
   ```powershell
   cd c:\Users\Aureli\Desktop\EduInsights
   ```

2. **Start the services**:
   ```powershell
   docker-compose up --build
   ```

3. **Create a superuser** (in a new terminal):
   ```powershell
   docker-compose exec web python backend/manage.py createsuperuser
   ```

4. **Access the application**:
   - **Landing Page**: http://localhost:8000
   - **Dashboard**: http://localhost:8000 (after login)
   - **Student List**: http://localhost:8000/students/
   - **Admin Panel**: http://localhost:8000/admin
   - **API**: http://localhost:8000/api/students/

### Option 2: Local Development (Without Docker)

1. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL** and update `.env` file with your database credentials

4. **Run migrations**:
   ```powershell
   python manage.py migrate
   ```

5. **Create superuser**:
   ```powershell
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```powershell
   python manage.py runserver
   ```

## 🤖 Training the ML Model

1. **Prepare your CSV file** with this schema:
   ```csv
   student_id,attendance_rate,avg_assignment_score,midterm_score,missing_assignments,participation,lms_hours,passed
   ```

2. **Train the model** (inside Docker container or local environment):
   ```powershell
   # Using Docker:
   docker-compose exec web python backend/ml/train_model.py --csv backend/students_sample.csv
   
   # Or locally:
   python backend/ml/train_model.py --csv backend/students_sample.csv
   ```

3. **Model saved** to `backend/ml/model_store/rf_model.joblib`

## 📊 Using the System

### For Teachers

1. **Login** to the admin panel at http://localhost:8000/admin
2. **Add students** manually or prepare CSV import
3. **Upload performance records** for each student
4. **Train the model** using the provided script
5. **View predictions** via API: `GET /api/students/{id}/predict/`

### Web Interface Pages

- **`/`** - Beautiful landing page with features overview
- **`/`** - Main dashboard (when logged in) with statistics and at-risk students
- **`/students/`** - Student list with search and filter capabilities
- **`/students/{id}/`** - Individual student detail page with AI predictions
- **`/admin/`** - Django admin panel for data management

### API Endpoints

- `GET /api/students/` - List all students
- `GET /api/students/{id}/` - Get student details
- `GET /api/students/{id}/predict/` - Get prediction and recommendations
- `POST /api/students/` - Create new student

### Example API Response

```json
{
  "student": "John Doe",
  "prediction": "1",
  "probabilities": [0.15, 0.85],
  "top_features": [
    ["avg_assignment_score", 0.35],
    ["attendance_rate", 0.28],
    ["midterm_score", 0.22]
  ],
  "recommendations": [
    "Focus on assignment practice: try 3 weekly practice problems and seek feedback.",
    "Keep up the good work. Maintain current study habits and continue practice."
  ]
}
```

## 📁 Project Structure

```
EduInsights/
├── backend/
│   ├── eduinsight/           # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── students/             # Main Django app
│   │   ├── models.py         # Student & PerformanceRecord models
│   │   ├── views.py          # API views & prediction logic
│   │   ├── serializers.py    # DRF serializers
│   │   ├── urls.py
│   │   └── admin.py
│   ├── ml/                   # Machine learning pipeline
│   │   ├── train_model.py    # Training script
│   │   └── model_store/      # Saved models
│   ├── manage.py
│   ├── requirements.txt
│   └── students_sample.csv   # Sample training data
├── docker-compose.yml
├── Dockerfile
├── .env
└── README.md
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key
DEBUG=1
POSTGRES_DB=eduinsight
POSTGRES_USER=eduinsight
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Model Features

The ML model uses these features:
- `attendance_rate` (0-100%)
- `avg_assignment_score` (0-100)
- `midterm_score` (0-100)
- `missing_assignments` (count)
- `participation` (0-100)
- `lms_hours` (hours spent on LMS)

## 🎓 Study Recommendations Logic

The system provides recommendations based on:

- **Low Attendance (<75%)**: Watch recorded lectures, arrange tutoring
- **Low Assignment Score (<60%)**: Practice problems, seek feedback
- **Low Midterm (<50%)**: Core concept revision, tutoring sessions
- **Low LMS Hours (<2)**: Increase engagement to 4+ hours/week

## 🧪 Testing

Run tests (after setup):

```powershell
# Inside Docker:
docker-compose exec web python backend/manage.py test

# Or locally:
python manage.py test
```

## 📈 Future Enhancements

- [ ] SHAP integration for better explainability
- [ ] LLM-powered personalized study plans
- [ ] Mobile-friendly UI with charts
- [ ] Automated retraining pipeline
- [ ] Teacher intervention tracking
- [ ] Student progress monitoring dashboard
- [ ] Email notifications for at-risk students

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Enable proper authentication/authorization
- Consider data privacy regulations (GDPR, FERPA)
- Use environment-specific `.env` files

## 📝 License

This project is for educational purposes. Modify and use as needed.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions, please open a GitHub issue or contact the development team.

---

**Built with ❤️ using Django, PostgreSQL, and scikit-learn**
