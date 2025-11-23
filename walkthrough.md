# Hospital Management App Walkthrough

## Overview
I have successfully set up and run the Hospital Management App. The application is now running locally.

## Steps Taken

### 1. Environment Setup
- Verified Python version (3.12.8).
- Created a virtual environment `.venv`.
- Installed dependencies: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `django-cors-headers`.

### 2. Configuration Fixes
- **Issue**: `migrate` failed because `AUTH_USER_MODEL` was missing in `settings.py`.
- **Fix**: Added `AUTH_USER_MODEL = 'hospital.CustomUser'` to `hospital_management/settings.py`.
- **Issue**: `makemigrations` failed to detect changes because the `hospital/migrations` folder was empty/corrupt.
- **Fix**: Renamed the old `migrations` folder and ran `makemigrations hospital` to regenerate the initial migration.

### 3. Database Setup
- Deleted the existing `db.sqlite3` to ensure a clean state.
- Ran `python manage.py migrate` to apply all migrations.
- Created a superuser with credentials:
  - **Username**: `admin`
  - **Password**: `admin`

### 4. Verification
- Started the development server at `http://127.0.0.1:8000/`.
- Verified that the server accepts requests (checked logs).
- The Admin interface is accessible at `http://127.0.0.1:8000/admin/`.

## How to Access
- **App URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (Note: Root path returns 404 as expected, check API endpoints or Admin)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Login**: Use `admin` / `admin`

## Next Steps
- Explore the API endpoints listed in `README.md`.
- Use Postman or the browser to interact with the API.

### 5. Frontend Setup
- **Issue**: The root URL `/` was returning a 404 because no view was configured for it, although a `home.html` template existed.
- **Fix**: 
    - Created a `home` view in `hospital/views.py` to render `hospital/home.html`.
    - Mapped the root URL `''` to this view in `hospital_management/urls.py`.
- **Verification**: Verified that `http://127.0.0.1:8000/` now loads the "Hospital Management System" landing page.
