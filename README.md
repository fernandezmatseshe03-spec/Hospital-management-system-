# CarePoint Hospital Management System

A Flask + SQLite hospital management system prototype.

## Features

- Patient registration
- Patient login
- Staff login
- Password hashing
- Role-based access
- Patient profiles
- Appointment requests
- Appointment management
- Medical assistance requests
- Staff responses
- Medical records
- Staff management
- Administrator account creation
- Responsive interface
- SQLite database

## User Roles

### Patient

Patients can:

- Register
- Login
- Update their profile
- Request appointments
- Send medical assistance requests
- View appointment status
- View staff responses
- View medical records

### Doctor

Doctors can:

- View patients
- View appointments
- Manage appointments
- Respond to medical requests
- Create medical records

### Nurse

Nurses can:

- View patients
- Manage appointments
- Respond to medical requests
- Create medical records

### Receptionist

Receptionists can:

- View patients
- Manage appointments
- Respond to medical requests

### Administrator

Administrators can:

- Access staff dashboard
- View patients
- Manage appointments
- Respond to medical requests
- Create medical records
- Create staff accounts

## Demo Administrator

Email:

admin@carepoint.test

Password:

Admin123!

Change these credentials before using the application outside local development.

## Installation

Install the dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Then open:

http://127.0.0.1:5000

## Database

SQLite is used for local development.

The database file:

hospital.db

is automatically created when the application starts.

## Important Security Notice

This is a development and portfolio prototype.

Do not use it to store real patient medical information without implementing appropriate production security measures, including:

- HTTPS
- CSRF protection
- Secure session configuration
- Strong secret management
- Database access controls
- Audit logging
- Backups
- Data encryption
- Access-control policies
- Privacy and consent workflows
- Appropriate healthcare/legal compliance