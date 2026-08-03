# EDUINSIGHT AI

EDUINSIGHT AI is an educational management platform designed to simplify course management, assignment submission, grading, and student performance analysis. The project follows a layered architecture to ensure maintainability, scalability, and clean code practices.

---

## Project Status

Current Phase: Repository Layer Completed

### Completed

- Project structure
- Domain models
- Repository layer (CRUD operations)
- Repository testing

### In Progress

- Controller layer

### Upcoming

- Views
- Application logic
- Authentication
- Database integration
- Analytics
- Machine Learning features

---

# Project Structure

```text
EDUINSIGHT_AI/
│
├── app.py
├── README.md
├── requirements.txt
│
├── config/
├── controllers/
├── models/
├── repositories/
├── services/
├── interfaces/
├── utils/
├── views/
├── data/
└── test/
```

---

# Architecture

```text
                User
                  │
                  ▼
            Controllers
                  │
                  ▼
           Repositories
                  │
                  ▼
               Models
```

---

# Models

- Student
- Teacher
- Course
- Exercise
- Submission
- Grade
- Notification

---

# Repositories

Completed repositories:

- StudentRepository
- TeacherRepository
- CourseRepository
- ExerciseRepository
- SubmissionRepository
- GradeRepository
- NotificationRepository

Each repository provides:

- Create
- Read
- Update
- Delete
- Search
- Count

---

# Development Roadmap

## Phase 1 — Foundation

- [x] Project structure
- [x] Models
- [x] Repositories

---

## Phase 2 — Business Logic

- [ ] StudentController
- [ ] TeacherController
- [ ] CourseController
- [ ] ExerciseController
- [ ] SubmissionController
- [ ] GradeController
- [ ] NotificationController

---

## Phase 3 — User Interface

- [ ] Main Menu
- [ ] Student Interface
- [ ] Teacher Interface
- [ ] Dashboard
- [ ] Navigation

---

## Phase 4 — Data Persistence

- [ ] SQLite Database
- [ ] Data Access Layer
- [ ] Data Validation

---

## Phase 5 — Analytics

- [ ] Student Performance Analytics
- [ ] Reports
- [ ] Charts
- [ ] Statistics

---

## Phase 6 — Artificial Intelligence

- [ ] Student Performance Prediction
- [ ] Recommendation System
- [ ] Learning Analytics
- [ ] AI Assistant

---

# Testing

Repository tests can be executed using:

```bash
python -m test.test_student_repository
python -m test.test_teacher_repository
python -m test.test_course_repository
python -m test.test_exercise_repository
python -m test.test_submission_repository
python -m test.test_grade_repository
python -m test.test_notification_repository
```

---

# Technologies

Current

- Python
- Object-Oriented Programming (OOP)

Planned

- Rich
- SQLite
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Plotly

---

# Current Progress

```text
Project Structure
        │
        ▼
Models
        │
        ▼
Repositories
        │
        ▼
Controllers
        │
        ▼
Views
        │
        ▼
Application
        │
        ▼
Database
        │
        ▼
Analytics
        │
        ▼
Machine Learning
```

---

# Design Principles

The project follows the following software engineering principles:

- Object-Oriented Programming (OOP)
- Layered Architecture
- Separation of Concerns
- Repository Pattern
- Modular Design
- Maintainable and Scalable Code

---

# License

This project is intended for educational purposes and personal learning.