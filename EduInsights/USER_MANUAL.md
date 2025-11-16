# EduInsight - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [For Teachers](#for-teachers)
4. [For Students](#for-students)
5. [Understanding Predictions](#understanding-predictions)
6. [FAQ](#faq)

---

## Introduction

**EduInsight** is an AI-powered system that helps identify students at risk of failing and provides personalized study recommendations. It analyzes multiple factors including attendance, assignment scores, and engagement to predict performance.

### Key Benefits

**For Teachers:**
- Identify at-risk students early
- Get data-driven insights on what's affecting performance
- Receive actionable intervention suggestions
- Track cohort performance trends

**For Students:**
- Understand your current academic standing
- Get personalized study recommendations
- Track your progress over time
- Access resources tailored to your needs

---

## Getting Started

### Accessing the System

1. Open your web browser
2. Navigate to: `http://localhost:8000` (or your institution's URL)
3. Click "Login" in the top right corner
4. Enter your username and password

### First Time Login

**Teachers:** Contact your system administrator for an account with teacher privileges.

**Students:** Your teacher will provide login credentials linked to your student ID.

---

## For Teachers

### Dashboard Overview

After logging in, you'll see:
- **Total Students**: Number of students in the system
- **At-Risk Students**: Students predicted to fail
- **Recent Records**: Latest performance data uploads

### Adding Students

#### Method 1: Manual Entry

1. Click **Admin Panel** in the navigation
2. Select **Students** → **Add Student**
3. Fill in:
   - Student ID (unique identifier)
   - Full Name
   - Age (optional)
   - Gender (optional)
4. Click **Save**

#### Method 2: CSV Upload (Bulk Import)

1. Prepare a CSV file with this format:
   ```csv
   student_id,full_name,age,gender
   S001,John Doe,20,M
   S002,Jane Smith,21,F
   ```

2. Navigate to **Import Data** section
3. Click **Choose File** and select your CSV
4. Click **Upload**
5. Review the import summary

### Adding Performance Records

For each student, you need to add performance data:

1. Go to **Admin Panel** → **Performance Records** → **Add Performance Record**
2. Select the **Student**
3. Enter the **Term** (e.g., "Fall 2025")
4. Fill in metrics:
   - **Attendance Rate**: Percentage (0-100)
   - **Average Assignment Score**: Percentage (0-100)
   - **Midterm Score**: Percentage (0-100)
   - **Missing Assignments**: Number of assignments not submitted
   - **Participation**: Engagement score (0-100)
   - **LMS Hours**: Hours spent on Learning Management System
   - **Final Grade** (optional): If already known
   - **Passed** (optional): Yes/No if outcome is known
5. Click **Save**

### Training the ML Model

After adding sufficient data (recommended: 50+ records):

1. Open a terminal/command prompt
2. Run the training command:
   ```powershell
   python backend/ml/train_model.py --csv backend/students_sample.csv
   ```
3. Wait for training to complete
4. Check for "Model saved successfully" message

**Note:** You should retrain the model periodically as more data becomes available.

### Viewing Predictions

#### For Individual Students:

1. Go to **API** → **Students** (or use the web interface)
2. Find the student you want to check
3. Click on their **Predict** link
4. View the prediction results:
   - Pass/Fail probability
   - Top contributing factors
   - Personalized recommendations

#### Understanding Results:

**Prediction:** 
- `0` = At risk of failing
- `1` = Likely to pass

**Probabilities:**
- `[0.85, 0.15]` means 85% chance of failing, 15% chance of passing

**Top Features:**
Shows which factors have the most impact on the prediction (e.g., low assignment scores, poor attendance)

**Recommendations:**
Specific, actionable suggestions to help the student improve

### Taking Action

When you identify at-risk students:

1. **Review the recommendations** provided by the system
2. **Contact the student** for a one-on-one meeting
3. **Create an action plan** based on the specific factors identified
4. **Follow up regularly** to track improvement
5. **Document interventions** for future reference

### Best Practices

- **Update data regularly**: Weekly or bi-weekly updates provide better predictions
- **Act early**: Don't wait until midterms; intervene as soon as concerns arise
- **Personalize interventions**: Use the specific factors identified for each student
- **Track outcomes**: Note which interventions work best
- **Maintain privacy**: Only share predictions with relevant staff

---

## For Students

### Viewing Your Dashboard

1. Log in to the system
2. Your dashboard shows:
   - Current performance metrics
   - Prediction status
   - Personalized recommendations

### Understanding Your Metrics

**Attendance Rate:**
- Percentage of classes attended
- Target: 75% or higher
- Impact: Strong predictor of success

**Assignment Scores:**
- Your average on completed assignments
- Target: 60% or higher
- Impact: Shows grasp of material

**Midterm Score:**
- Your midterm exam performance
- Target: 50% or higher
- Impact: Measures core understanding

**Missing Assignments:**
- Number of assignments not submitted
- Target: 0 missing assignments
- Impact: Indicates engagement and time management

**Participation:**
- Engagement in discussions, forums, activities
- Target: 70% or higher
- Impact: Shows active learning

**LMS Hours:**
- Time spent on course materials online
- Target: 4+ hours per week
- Impact: Correlates with material mastery

### Interpreting Your Prediction

**"Likely to Pass":**
- You're on track! Keep up your current habits
- Review recommendations for optimization

**"At Risk":**
- Don't panic! This is an early warning
- Focus on the specific areas flagged
- Seek help from teachers or tutors
- Follow the personalized recommendations

### Following Recommendations

The system provides specific actions based on YOUR data:

**Example Recommendations:**

1. **"Focus on assignment practice"**
   - Do 3 practice problems per week
   - Seek feedback from teacher
   - Use office hours for clarification

2. **"Improve attendance"**
   - Watch recorded lectures if you missed class
   - Arrange catch-up sessions with peers
   - Contact teacher about attendance barriers

3. **"Increase LMS engagement"**
   - Spend 4+ hours per week on course materials
   - Complete optional readings
   - Watch supplementary videos

4. **"Seek tutoring"**
   - Schedule 2 tutoring sessions per week
   - Focus on core concepts from midterm
   - Join study groups

### Tracking Your Progress

- Check your dashboard weekly
- Compare current metrics to previous weeks
- Celebrate improvements!
- Adjust study habits based on what's working

---

## Understanding Predictions

### How It Works

The AI model analyzes six key factors:
1. Attendance patterns
2. Assignment performance
3. Midterm results
4. Assignment completion rate
5. Participation/engagement
6. Time spent on course materials

It compares your data to patterns from past students who succeeded or struggled.

### What the Model Considers

**High Impact Factors:**
- Consistent attendance
- Strong assignment scores
- Good midterm performance

**Warning Signs:**
- Missing multiple assignments
- Attendance below 75%
- Low LMS engagement
- Declining participation

### Limitations

- Predictions are **guidance, not certainty**
- Many factors affect success (health, personal circumstances, motivation)
- The model improves over time with more data
- Always combine AI insights with human judgment

### Privacy & Data Use

- Your data is used **only** for educational support
- Predictions are shared only with authorized teachers
- You can request to see all data stored about you
- Personal information (age, gender) is optional

---

## FAQ

### For Teachers

**Q: How much data do I need to train the model?**
A: Minimum 50 records, but 200+ is recommended for better accuracy.

**Q: How often should I retrain the model?**
A: Every term, or when you have 50+ new records.

**Q: What if a prediction seems wrong?**
A: Use your professional judgment. The model is a tool, not a replacement for teacher expertise.

**Q: Can I customize the recommendation logic?**
A: Yes! Edit `backend/students/views.py` in the `generate_recommendations` function.

**Q: How do I export predictions for all students?**
A: Use the API endpoint `/api/students/` and iterate through students programmatically.

### For Students

**Q: Will this affect my grade?**
A: No. This is a support tool to help you succeed. It doesn't determine grades.

**Q: What if I'm marked "at risk" but feel I'm doing fine?**
A: Talk to your teacher. There may be factors the model doesn't capture, or your recent improvements may not yet be reflected.

**Q: Can I see the predictions for other students?**
A: No. You can only see your own data.

**Q: How accurate are the predictions?**
A: The model aims for 78%+ accuracy, but many factors influence final outcomes.

**Q: Who can see my data?**
A: Only your teachers and authorized academic staff.

### General

**Q: Is my data secure?**
A: Yes. The system uses industry-standard security practices.

**Q: Can I delete my data?**
A: Contact your institution's admin following their data retention policies.

**Q: Does this work for all subjects?**
A: It's most effective when consistent metrics (attendance, assignments) are tracked.

**Q: What if I don't have midterm scores yet?**
A: The model can work with partial data, but predictions are more accurate with complete information.

---

## Getting Help

**Technical Issues:**
- Contact your system administrator
- Check the troubleshooting section in developer docs

**Academic Support:**
- Talk to your teacher or academic advisor
- Use the recommendations as a starting point

**Questions About Predictions:**
- Discuss with your teacher
- Request a detailed explanation of factors

---

## Contact & Support

**System Administrator:** [admin@institution.edu]
**Academic Support:** [support@institution.edu]
**Technical Help:** [helpdesk@institution.edu]

---

**Remember: EduInsight is here to help you succeed! Use it as a tool for early intervention and personalized support. 📚✨**
