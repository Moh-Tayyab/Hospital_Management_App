# Hospital Management System

A robust Hospital Management System built with Django REST Framework that streamlines operations and efficiently manages hospital data.

## Features

- CRUD operations for Doctors, Nurses, Staff, Patients, Appointments, and Medical Records
- Role-based access control
- RESTful API endpoints
- Admin interface for easy management
- Relationship management between different entities
- Detailed views and filtering capabilities

## Tech Stack

- Backend: Django 4.x, Django REST Framework
- Database: PostgreSQL / SQLite (for development)
- Authentication: Token-based (DRF TokenAuth)
- Validation: DRF Serializers and Custom Validators

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd hospital-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

The API is available at `http://localhost:8000/api/` with the following endpoints:

- `/departments/` - Department management
- `/doctors/` - Doctor management
- `/nurses/` - Nurse management
- `/staff/` - Staff management
- `/patients/` - Patient management
- `/appointments/` - Appointment management
- `/medical-records/` - Medical record management

## Admin Interface

Access the admin interface at `http://localhost:8000/admin/` using your superuser credentials.

## Authentication

The API uses token-based authentication. To obtain a token:

1. Send a POST request to `/api-token-auth/` with your credentials:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

2. Use the received token in subsequent requests by adding it to the Authorization header:
```
Authorization: Token <your_token>
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
