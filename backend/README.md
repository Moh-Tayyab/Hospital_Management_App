# 🏥 Hospital Management System

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#) [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern and comprehensive Hospital Management System built with cutting-edge technologies to streamline healthcare operations and enhance patient care.

---

## 📋 Table of Contents

- [🏥 Hospital Management System](#-hospital-management-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [💻 Tech Stack](#-tech-stack)
  - [🚀 Getting Started](#-getting-started)
  - [🗂️ API Endpoints](#️-api-endpoints)
  - [🔐 Authentication](#-authentication)
  - [🔌 Postman API Testing](#-postman-api-testing)
    - [Environment Setup](#environment-setup)
    - [Automatic Authentication Script](#automatic-authentication-script)
    - [Token Refresh](#token-refresh)
  - [⚙️ Admin Interface](#️-admin-interface)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [👥 Authors](#-authors)
  - [🙏 Acknowledgments](#-acknowledgments)
  - [📞 Support](#-support)
  - [🔄 Updates](#-updates)

---

## ✨ Features

- **Patient Management**
  - Patient registration and profile management
  - Medical history tracking
  - Appointment scheduling
  - Digital health records

- **Staff Management**
  - Doctor and staff profiles
  - Shift scheduling
  - Performance tracking
  - Specialization management

- **Administrative Tools**
  - Billing and invoicing
  - Inventory management
  - Report generation
  - Analytics dashboard

- **Appointment System**
  - Online booking
  - Automated reminders
  - Calendar integration
  - Wait-list management

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

JWT (JSON Web Token) authentication is enforced on all endpoints.

1. **Obtain Token**:
   ```http
   POST /gettoken/
   Content-Type: application/json

   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **Refresh Token**:
   ```http
   POST /refreshtoken/
   Content-Type: application/json

   {
     "refresh": "your_refresh_token"
   }
   ```

3. **Verify Token**:
   ```http
   POST /verifytoken/
   Content-Type: application/json

   {
     "token": "your_access_token"
   }
   ```

4. **Use Token**:
   Include the token in the `Authorization` header for subsequent requests:
   ```http
   Authorization: Bearer <your_access_token>
   ```

## 🔌 Postman API Testing

### Environment Setup

1. **Create Environment**:
   - Open Postman and click on "Environments" in the sidebar
   - Click "Create New" or "+" button
   - Name your environment (e.g., "Hospital Management API")

2. **Add Environment Variables**:
   - `base_url`: Your API base URL (e.g., `http://localhost:8000`)
   - `access_token`: Leave empty (will be filled automatically)
   - `refresh_token`: Leave empty (will be filled automatically)

3. **Set Up Token Generation**:
   - Create a POST request to `{{base_url}}/gettoken/`
   - In the Body tab, select "raw" and "JSON"
   - Add your credentials:
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```
   - In the "Tests" tab, add this script to automatically save tokens:
     ```javascript
     if (pm.response.code === 200) {
         var response = pm.response.json();
         pm.environment.set("access_token", response.access);
         pm.environment.set("refresh_token", response.refresh);
     }
     ```

### Automatic Authentication Script

Add this script to your Postman Collection in the "Pre-request Script" tab to automatically add authentication headers to all requests (except auth endpoints):

```javascript
// Define endpoints you want to exclude from authentication
const excludedEndpoints = [
    '/api/auth/login',
    '/api/auth/signup',
    '/gettoken/',
    '/refreshtoken/',
    '/verifytoken/'
];

// Extract request path (excluding domain)
const requestUrl = pm.request.url.getPath();

// Check if current endpoint should be excluded from authentication
if (!excludedEndpoints.includes(requestUrl)) {
    // Get the access token from environment variables
    const accessToken = pm.environment.get("access_token");
    
    // Only add the Authorization header if a token exists
    if (accessToken) {
        pm.request.headers.add({
            key: "Authorization",
            value: `Bearer ${accessToken}`
        });
        
        // Get and add the refresh token if it exists
        const refreshToken = pm.environment.get("refresh_token");
        if (refreshToken) {
            pm.request.headers.add({
                key: "X-Refresh-Token",
                value: refreshToken
            });
        }
    } else {
        console.warn("Warning: No access token found in environment variables");
    }
}
```

### Token Refresh

To handle token expiration, create a POST request to `{{base_url}}/refreshtoken/` with this body:

```json
{
  "refresh": "{{refresh_token}}"
}
```

Add this script to the "Tests" tab to automatically update the access token:

```javascript
if (pm.response.code === 200) {
    var response = pm.response.json();
    pm.environment.set("access_token", response.access);
}
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

## 👥 Authors

- Muhammad Tayyab - *Initial work* - [My LinkedIn Profile](https://www.linkedin.com/in/ch-muhammad-tayyab/)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped this project grow
- Special thanks to the open-source community for their valuable tools and libraries

## 📞 Support

For support, please email support@hospitalmanagementsystem.com or create an issue in the GitHub repository.

## 🔄 Updates

Stay tuned for regular updates and new features. Follow our GitHub repository for the latest changes.

---


