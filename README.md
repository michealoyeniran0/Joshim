# Joshim — Online Tutoring Platform

Joshim is a live tutoring platform designed to connect children and teenagers with qualified tutors through interactive online learning.

The platform supports course discovery, parent/child registration, student accounts, tutor-led learning, enrolment, payments, profile management, and administrative course management.

## Live Demo

**Website:** https://joshim.onrender.com

## Project Overview

Joshim was developed to provide a simple and accessible way for parents to find learning opportunities for their children and manage their children's participation in online tutoring.

The platform was built as a full-stack web application, covering both the user-facing learning experience and the administrative side of the tutoring business.

## Key Features

### Student and Parent Features

- Parent/child registration
- Secure user authentication
- Login and logout
- Password reset functionality
- Student dashboard
- Profile management
- Profile photo upload
- Course browsing
- Course enrolment
- Learning schedule information
- Live class access
- Responsive mobile interface

### Course Management

Administrators can:

- Create courses
- Edit courses
- Delete courses
- Manage course descriptions
- Manage course prices
- Add course video links
- Manage course enrolments
- View student information
- Manage payment information

### Payment Integration

Joshim includes Paystack integration for handling course payments.

Payment-related records are stored in the application's database and linked to users and courses.

### Communication

The platform supports email communication through Gmail SMTP, including password-reset functionality.

### International Learning Support

The landing page provides live time information for:

- Nigeria
- United Kingdom
- United States

This helps international students and parents understand the availability of live tutoring across different time zones.

## Technology Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Limiter
- Flask-Mail

### Frontend

- HTML5
- CSS3
- JavaScript
- Responsive design

### Database

- PostgreSQL for production
- SQLite for local development

### Payments

- Paystack

### Deployment

- Render
- Gunicorn

## Application Architecture

Joshim uses a modular Flask application structure.

```text
joshim/
│
├── app/
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── student.py
│   │   ├── admin.py
│   │   └── payment.py
│   │
│   ├── services/
│   │   └── email_services.py
│   │
│   ├── static/
│   │   ├── images/
│   │   ├── css/
│   │   └── javascript/
│   │
│   └── templates/
│
├── instance/
├── config.py
├── requirements.txt
├── run.py
└── README.md