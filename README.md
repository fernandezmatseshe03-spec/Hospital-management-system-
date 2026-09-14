<<<<<<< HEAD
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
=======
# 🏥 Hospital Management System

A full-stack Hospital Management System designed to streamline the management of patients, appointments, medical information, and hospital staff activities through a centralized web application.

## 📌 Project Overview

The Hospital Management System provides a digital platform for managing interactions between patients and hospital staff.

Patients can create accounts, provide their details, request medical assistance, and manage appointments, while authorized hospital staff can manage patient information and appointments through dedicated dashboards.

The project was developed as a practical full-stack web development project using Python and Flask for the backend, together with HTML, CSS, and JavaScript for the frontend.

## ✨ Key Features

### 👤 Patient Features

* Patient registration and login
* Patient profile management
* Submission of personal and medical information
* Appointment booking
* Viewing appointment information
* Access to relevant hospital services

### 🩺 Hospital Staff Features

* Staff authentication
* Patient management
* Appointment management
* Viewing patient information
* Managing patient requests
* Dedicated staff dashboard

### 👨‍💼 Administration

* Administrative dashboard
* Overview of system activity
* Management of users and hospital information
* Centralized management of hospital operations

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **JavaScript**
* **SQLite** / database integration
* **Jinja2**

## 📂 Project Structure

```text
Hospital-management-system/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── ...
│
└── README.md
```

> The exact files and structure may vary as the system continues to be developed.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/fernandezmatseshe03-spec/Hospital-management-system-.git
```

### 2. Open the project directory

```bash
cd Hospital-management-system-
```

If the application files are inside a subdirectory, navigate into that directory before running the application.

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask application

```bash
python app.py
```

### 5. Open the application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 🔐 Authentication

The system includes separate access and functionality for different types of users.

Typical roles include:

* Patient
* Hospital Staff
* Administrator

Authentication and authorization are used to help ensure that users access the appropriate areas of the system.

## 📸 Screenshots

Screenshots of the system will be added here to demonstrate the user interface and major features.

 The screenshots include:

* Homepage
* Patient registration
* Patient login
* Patient dashboard
* Appointment booking
* Staff dashboard
* Admin dashboard

## 🎯 Project Goals

The main goals of this project are to:

* Digitize common hospital management processes
* Improve patient and appointment management
* Provide centralized access to hospital information
* Reduce reliance on manual record management
* Demonstrate practical full-stack development skills
* Build a scalable foundation for additional healthcare features

## 🔮 Future Improvements

Planned improvements may include:

* Online appointment notifications
* Doctor and department management
* Electronic medical records
* Prescription management
* Billing and payment integration
* Email/SMS notifications
* Advanced reporting and analytics
* Role-based access control improvements
* Cloud deployment
* Improved security and data protection

## ⚠️ Disclaimer

This project is intended for **educational, demonstration, and portfolio purposes**.

It should not be used to manage real patient information without appropriate security, privacy, authentication, authorization, regulatory compliance, data protection, and professional healthcare-system requirements.

## 👨‍💻 Developer

**Fernandez Matseshe**

Computer Science Graduate | Web Developer

Interested in building web applications, digital solutions, and SEO-focused websites.

---

⭐ If you find this project useful or interesting, feel free to explore the source code and follow the project's development.
>>>>>>> 573bdfbaf0505b0bf6f69d64f0d4c871d60f12d6
