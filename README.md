# 🏥 Hospital Management System

A full-stack **Hospital Management System** built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**. The system provides separate functionality for patients and hospital staff, including authentication, appointments, medical requests, medical records, and profile management.

## 🌐 Live Demo

**[Open the Hospital Management System](https://hospital-management-system-1-osle.onrender.com)**

The application is publicly deployed on **Render**, allowing users to access and interact with the system directly through a web browser.

## 📂 Source Code

**[View the GitHub Repository](https://github.com/fernandezmatseshe03-spec/Hospital-management-system-)**

---

## ✨ Features

### 👤 Patient Features

* Patient account registration
* Secure login and logout
* Personal patient dashboard
* Profile management
* Appointment booking
* Medical assistance/request submission
* View appointment status
* View medical records
* Secure password hashing

### 👨‍⚕️ Hospital Staff Features

The system supports different staff roles, including:

* Administrator
* Doctor
* Nurse
* Receptionist

Staff can:

* View patient information
* Manage appointments
* Update appointment status
* Respond to medical requests
* Create and manage medical records
* Access role-specific functionality

### 🔐 Authentication & Security

* User authentication
* Password hashing using Werkzeug
* Session-based authentication
* Role-based access control
* Protected patient and staff routes
* Environment-based configuration for production deployment

---

## 🛠️ Technologies Used

| Technology   | Purpose                                    |
| ------------ | ------------------------------------------ |
| Python       | Backend programming                        |
| Flask        | Web application framework                  |
| SQLite       | Database                                   |
| HTML5        | Page structure                             |
| CSS3         | Styling and responsive interface           |
| JavaScript   | Client-side functionality                  |
| Jinja2       | Dynamic HTML templates                     |
| Werkzeug     | Password hashing and security              |
| Gunicorn     | Production WSGI server                     |
| Render       | Cloud deployment                           |
| Git & GitHub | Version control and source-code management |

---

## 🗄️ Database Structure

The system uses SQLite with several interconnected tables:

* `users`
* `appointments`
* `medical_requests`
* `medical_records`

The database stores patient accounts, staff accounts, appointments, medical requests, and medical records.

---

## 🔑 User Roles

### Patient

Patients can register for an account and access their personal dashboard.

### Doctor

Doctors can manage appointments, respond to medical requests, and create medical records.

### Nurse

Nurses can access relevant patient and appointment functionality and manage medical records.

### Receptionist

Receptionists can manage appointments and assist with patient administration.

### Administrator

The administrator has elevated system-management privileges, including staff account creation and management.

---

## 📸 Screenshots

Screenshots of the application can be found in the `screenshots` folder.

### Homepage

![Homepage](screenshots/homepage.png)

### Patient Registration

![Patient Registration](screenshots/register.png)

### Login

![Login](screenshots/login.png)

### Patient Dashboard

![Patient Dashboard](screenshots/patient-dashboard.png)

### Staff Dashboard

![Staff Dashboard](screenshots/staff-dashboard.png)

### Appointments

![Appointments](screenshots/appointments.png)

> **Note:** Rename the screenshot files in the `screenshots` folder to match the filenames above, or update the paths in this section to match your actual screenshot filenames.

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/fernandezmatseshe03-spec/Hospital-management-system-.git
```

### 2. Enter the project directory

```bash
cd Hospital-management-system-
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

The application is deployed using **Render**.

Production deployment uses:

```text
Build Command:
pip install -r requirements.txt
```

```text
Start Command:
gunicorn app:app
```

Production configuration uses environment variables for sensitive settings such as the Flask secret key and administrator credentials.

---

## 📁 Project Structure

```text
Hospital-management-system/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── patient_dashboard.html
│   ├── staff_dashboard.html
│   └── profile.html
│
├── app.py
├── hospital.db
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🎯 Project Objective

The goal of this project was to develop a web-based hospital management system that demonstrates how different hospital users can interact with a centralized system.

The project focuses on:

* User authentication
* Role-based access control
* Patient management
* Appointment management
* Medical request handling
* Medical record management
* Database integration
* Production deployment

---

## 💡 What I Learned

Through this project, I gained practical experience with:

* Building full-stack applications with Flask
* Designing relational database structures
* Implementing authentication and authorization
* Working with SQLite
* Creating dynamic interfaces with Jinja2
* Managing application sessions
* Deploying Python applications to the cloud
* Using Git and GitHub for version control
* Debugging production deployment issues
* Adapting applications for Linux-based hosting environments

---

## 👨‍💻 Developer

**Fernandez Matseshe**

BSc Computer Science

### Portfolio Links

* **Live Application:** https://hospital-management-system-1-osle.onrender.com
* **GitHub:** https://github.com/fernandezmatseshe03-spec

---

## 📄 License

This project was developed for educational, portfolio, and demonstration purposes.
