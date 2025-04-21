# 🏥 Hospital Management System

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#) [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust **Hospital Management System** built with **Django REST Framework** that streamlines operations and efficiently manages hospital data.

---

## 📋 Table of Contents

- [🏥 Hospital Management System](#-hospital-management-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [💻 Tech Stack](#-tech-stack)
  - [🚀 Getting Started](#-getting-started)
  - [🗂️ API Endpoints](#️-api-endpoints)
  - [🔐 Authentication](#-authentication)
  - [⚙️ Admin Interface](#️-admin-interface)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)

---

## ✨ Features

- ✅ **CRUD Operations** for Doctors, Nurses, Staff, Patients, Appointments, and Medical Records
- 🔒 **Role-Based Access Control** to secure sensitive data
- 🌐 **RESTful API Endpoints** following best practices
- 🛠 **Admin Interface** for easy data management
- 🔗 **Relationship Management** between entities (e.g., Patients ↔️ Appointments)
- 🔍 **Filtering & Detailed Views** for quick data retrieval

---

## 💻 Tech Stack

| Layer           | Technology                        |
|-----------------|------------------------------------|
| Backend         | Django 4.x, Django REST Framework |
| Database        | PostgreSQL / SQLite               |
| Authentication  | DRF Token Authentication          |
| Validation      | DRF Serializers & Custom Validators |

---

## 🚀 Getting Started

Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Moh-Tayyab/Hospital_Management_App.git
   cd hospital-management
   ```

2. **Create & activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

Your API is now running at `http://localhost:8000/api/`!

---

## 🗂️ API Endpoints

| Endpoint               | Description                     |
|------------------------|---------------------------------|
| `/departments/`        | Department management           |
| `/doctors/`            | Doctor management               |
| `/nurses/`             | Nurse management                |
| `/staff/`              | Staff management                |
| `/patients/`           | Patient management              |
| `/appointments/`       | Appointment management          |
| `/medical-records/`    | Medical record management       |

---

## 🔐 Authentication

Token-based authentication is enforced on all endpoints.

1. **Obtain Token**:
   ```http
   POST /api-token-auth/
   Content-Type: application/json

   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **Use Token**:
   Include the token in the `Authorization` header for subsequent requests:
   ```http
   Authorization: Token <your_token>
   ```

---

## ⚙️ Admin Interface

Access the Django admin panel to manage all entities:

- URL: `http://localhost:8000/admin/`
- Login with your superuser credentials

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. 🎯 **Fork** the repository<br>
2. 🛠 **Create a new branch** (`git checkout -b feature/YourFeature`)<br>
3. 📝 **Make your changes** and ensure tests pass<br>
4. 📬 **Submit a Pull Request** detailing your improvements

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---


