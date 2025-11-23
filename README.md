# 🏥 Hospital Management System

A comprehensive, full-stack hospital management application designed to streamline healthcare operations. This system provides role-based access control for administrators, doctors, nurses, receptionists, and patients, enabling efficient management of appointments, medical records, billing, and patient care.

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.0-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Docker Setup](#docker-setup)
- [API Documentation](#api-documentation)
- [User Roles & Permissions](#user-roles--permissions)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 About the Project

The **Hospital Management System** is a modern, scalable solution built to digitize and optimize hospital operations. It addresses critical challenges in healthcare management including:

- **Appointment Scheduling**: Real-time slot availability with conflict prevention
- **Electronic Health Records (EHR)**: Secure, centralized patient medical history
- **Billing & Invoicing**: Automated invoice generation with multiple payment methods
- **Role-Based Access**: Granular permissions for different user types
- **Patient Management**: Comprehensive tracking of in-patients and out-patients

### Why This Project?

Traditional hospital management systems are often fragmented, difficult to use, and lack modern features. This project aims to provide:

- 🚀 **Modern Tech Stack**: Built with cutting-edge technologies
- 🔒 **Security First**: JWT authentication, role-based access control
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ⚡ **Performance**: Optimized database queries and efficient API design
- 🎨 **User Experience**: Intuitive, beautiful interface with smooth animations

---

## ✨ Key Features

### For Patients
- 📅 **Book Appointments**: Schedule appointments with available doctors
- 📋 **View Medical Records**: Access complete medical history
- 💰 **Billing Dashboard**: View invoices and payment history
- 👤 **Profile Management**: Update personal and contact information

### For Doctors
- 🗓️ **Manage Schedule**: Set availability and view appointments
- 📝 **Create Medical Records**: Document patient visits and diagnoses
- 💊 **Prescriptions**: Generate and manage prescriptions
- 📊 **Patient Overview**: Access patient medical history

### For Administrators
- 👥 **User Management**: Create and manage staff accounts
- 🏢 **Department Management**: Organize hospital departments
- 📈 **Analytics Dashboard**: View system statistics and reports
- ⚙️ **System Configuration**: Manage hospital settings

### For Receptionists
- 📞 **Patient Registration**: Register new patients
- 📅 **Appointment Management**: Schedule and manage appointments
- 💳 **Billing Operations**: Process payments and generate invoices

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **Django** | Web Framework | 5.1+ |
| **Django REST Framework** | API Development | 3.15+ |
| **PostgreSQL** | Database | 15 |
| **JWT** | Authentication | 5.3+ |
| **Python** | Programming Language | 3.10+ |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **Next.js** | React Framework | 16.0 |
| **React** | UI Library | 19.2 |
| **TypeScript** | Type Safety | 5.0+ |
| **Tailwind CSS** | Styling | 4.0 |
| **Axios** | HTTP Client | 1.13+ |
| **React Icons** | Icon Library | 5.5+ |

### DevOps & Tools
- **Docker** & **Docker Compose**: Containerization
- **Git**: Version Control
- **ESLint**: Code Linting

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Dashboard  │  │  Appointments│  │   Patients   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Doctors    │  │    Records   │  │    Login     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                    REST API (JWT Auth)
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Django REST API)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     Auth     │  │ Appointments │  │   Patients   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Doctors    │  │    Records   │  │   Billing    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                      PostgreSQL Database
                            │
┌─────────────────────────────────────────────────────────────┐
│                         Database Layer                       │
│  Users | Patients | Doctors | Appointments | Records        │
│  Invoices | Payments | Departments | Staff                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.10 or higher
- **Node.js** 18.0 or higher
- **PostgreSQL** 15 or higher
- **Docker** (optional, for containerized setup)
- **Git**

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Moh-Tayyab/Hospital_Management_App.git
   cd Hospital_Management_App
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure database**
   
   Create a PostgreSQL database:
   ```sql
   CREATE DATABASE hospital_db;
   CREATE USER hospital_user WITH PASSWORD 'securepassword';
   GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
   ```

   Update `backend/hospital_management/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'hospital_db',
           'USER': 'hospital_user',
           'PASSWORD': 'securepassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Load test data (optional)**
   ```bash
   python create_test_data.py
   ```

9. **Start development server**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   
   Create `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

### Docker Setup

For a quick setup using Docker:

1. **Start services**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Database: `localhost:5432`

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET | `/api/auth/profile/` | Get user profile |

### Patient Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients/` | List all patients |
| POST | `/api/patients/` | Create new patient |
| GET | `/api/patients/{id}/` | Get patient details |
| PUT | `/api/patients/{id}/` | Update patient |
| DELETE | `/api/patients/{id}/` | Delete patient |

### Appointment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments/` | List appointments |
| POST | `/api/appointments/` | Create appointment |
| GET | `/api/appointments/{id}/` | Get appointment details |
| PUT | `/api/appointments/{id}/` | Update appointment |
| DELETE | `/api/appointments/{id}/` | Cancel appointment |
| GET | `/api/appointments/available-slots/` | Get available time slots |

### Medical Records Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/medical-records/` | List medical records |
| POST | `/api/medical-records/` | Create medical record |
| GET | `/api/medical-records/{id}/` | Get record details |
| PUT | `/api/medical-records/{id}/` | Update record |

### Billing Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/invoices/` | List invoices |
| POST | `/api/invoices/` | Create invoice |
| GET | `/api/invoices/{id}/` | Get invoice details |
| POST | `/api/payments/` | Record payment |

For detailed API documentation, visit `/api/docs/` when the backend server is running.

---

## 👥 User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Admin** | Full system access, user management, system configuration |
| **Doctor** | View/create medical records, manage appointments, view patients |
| **Nurse** | View medical records, assist with patient care |
| **Receptionist** | Patient registration, appointment scheduling, billing |
| **Patient** | View own records, book appointments, view invoices |

---

## 🗄️ Database Schema

### Core Models

- **CustomUser**: Extended Django user with role-based authentication
- **Patient**: Patient profiles with medical history
- **Doctor**: Doctor profiles with specialization and schedule
- **Nurse**: Nurse profiles with department assignment
- **Department**: Hospital departments
- **Appointment**: Appointment scheduling with conflict prevention
- **MedicalRecord**: Electronic health records
- **Invoice**: Billing and invoicing
- **InvoiceItem**: Line items for invoices
- **Payment**: Payment tracking

---

## 📁 Project Structure

```
Hospital_Management_App/
├── backend/
│   ├── hospital/                 # Main Django app
│   │   ├── models.py            # Database models
│   │   ├── serializers.py       # DRF serializers
│   │   ├── views.py             # API views
│   │   ├── urls.py              # URL routing
│   │   └── permissions.py       # Custom permissions
│   ├── hospital_management/     # Project settings
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Root URL config
│   │   └── wsgi.py              # WSGI config
│   ├── manage.py                # Django management
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js app directory
│   │   │   ├── dashboard/       # Dashboard pages
│   │   │   ├── appointments/    # Appointment pages
│   │   │   ├── patients/        # Patient pages
│   │   │   ├── doctors/         # Doctor pages
│   │   │   ├── records/         # Medical records
│   │   │   └── login/           # Authentication
│   │   ├── components/          # Reusable components
│   │   └── lib/                 # Utility functions
│   ├── public/                  # Static assets
│   └── package.json             # Node dependencies
│
├── docker-compose.yml           # Docker configuration
└── README.md                    # This file
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Test Scripts

```bash
# Test patient API
python verify_patient.py

# Test appointments
python test_appointments.py

# Test all APIs
python verify_api.py
```

### Frontend Tests

```bash
cd frontend
npm run test
```

---

## 🚢 Deployment

### Backend Deployment (Production)

1. **Set environment variables**
   ```bash
   export DEBUG=False
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='postgresql://user:pass@host:5432/db'
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Use production server (Gunicorn)**
   ```bash
   pip install gunicorn
   gunicorn hospital_management.wsgi:application
   ```

### Frontend Deployment

1. **Build production bundle**
   ```bash
   npm run build
   ```

2. **Start production server**
   ```bash
   npm start
   ```

### Recommended Platforms
- **Backend**: Heroku, Railway, DigitalOcean, AWS
- **Frontend**: Vercel, Netlify, AWS Amplify
- **Database**: AWS RDS, DigitalOcean Managed PostgreSQL

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

**Muhammad Tayyab**

- GitHub: [@Moh-Tayyab](https://github.com/Moh-Tayyab)
- Project Link: [https://github.com/Moh-Tayyab/Hospital_Management_App](https://github.com/Moh-Tayyab/Hospital_Management_App)

---

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Icons](https://react-icons.github.io/react-icons/)

---

<div align="center">
  <p>Made with ❤️ by Muhammad Tayyab</p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>
