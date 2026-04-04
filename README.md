---
# Online Leave Management System

Welcome to the **Online Leave Management System**! A professional, user-friendly web application built with Django, designed to help manage employee leave requests efficiently. From applying for leave to tracking approvals — this system has you covered.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## Features

### For Employees
- **User Authentication**: Secure login, logout, and password management with email-based password reset.
- **Leave Application**: Apply for leave with type, date range, and reason. Includes duplicate/overlap prevention.
- **Leave Balance**: View your remaining annual, sick, and other leave days with a visual doughnut chart.
- **Leave Status Tracking**: Track all your leave applications with status badges (Pending, Approved, Rejected, Cancelled).
- **Leave Detail View**: Dedicated page with full details of each leave application.
- **Cancel Pending Requests**: Cancel your own pending leave applications before they are processed.
- **Profile Management**: Update your role, department, contact information, and password.

### For Administrators
- **Admin Dashboard**: View and manage all employee leave applications.
- **Search & Filter**: Search by employee name/username, filter by status, and filter by date range.
- **Pagination**: Manage large lists of leave applications with built-in pagination.
- **Approve / Reject**: Approve or reject leave requests with a mandatory reason for rejections.
- **Balance Auto-Deduction**: Automatically deduct leave days from employee balances upon approval.
- **Email Notifications**: Employees receive email notifications when their leave is approved or rejected.
- **Team Calendar**: Visual monthly calendar showing who is on approved leave at a glance.
- **Django Admin**: Full admin panel for managing users, leave types, notices, and awards.

### System Features
- **Professional UI**: Modern, responsive Bootstrap-based design with a clean color palette.
- **Bootstrap Icons**: Consistent iconography throughout the application.
- **Responsive Design**: Works on desktop and mobile devices.
- **Real-time Feedback**: Success and error messages for all actions.
- **MIT Licensed**: Open source and free to use.

## Getting Started

Follow these steps to set up the application on your local machine.

### Prerequisites

- **Python 3.x**
- **Django 5.x**
- **SQLite** (default, included)

### Installation

#### Step 1: Clone the Repository

`ash
git clone https://github.com/ahmednule/Online_leave_Management_system.git
cd Online-leave-management-system
`

#### Step 2: Set Up a Virtual Environment

**For Windows:**
`ash
python -m venv venv
venv\Scripts\activate
`

**For Linux/Mac:**
`ash
python3 -m venv venv
source venv/bin/activate
`

#### Step 3: Install Dependencies

`ash
pip install -r requirements.txt
`

#### Step 4: Apply Migrations

`ash
python manage.py migrate
`

#### Step 5: Create an Admin User

`ash
python manage.py createsuperuser
`

#### Step 6: Run the Development Server

`ash
python manage.py runserver
`

#### Step 7: Access the Application

Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

### URL Routes

| URL | Description |
|-----|-------------|
| / | Dashboard — overview, stats, recent leaves, notices |
| /apply/ | Submit a new leave application |
| /balance/ | View your leave balance and chart |
| /notifications/ | View all your leave applications with filters |
| /profile/ | Manage your profile and change password |
| /accounts/login/ | Login page |
| /accounts/password-reset/ | Request password reset email |
| /leaves/admin/ | Admin: manage all leave applications |
| /leaves/admin/?status=Pending | Admin: filter by status |
| /calendar/ | Admin: team leave calendar |

### Creating Leave Types

As an admin, go to the Django admin panel at /admin/ and add leave types (e.g., Annual Leave, Sick Leave, Maternity Leave, Paternity Leave).

### Setting Up Leave Balances

New users automatically get a default balance (20 annual, 10 sick, 5 other days). Admins can modify balances through the admin panel.

### Email Configuration

The system uses a console email backend by default (emails print to the terminal). For production, update settings.py:

`python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'Leave System <noreply@example.com>'
`

## Contributing

We welcome contributions! Fork this project and submit pull requests.

## Contact

For any inquiries or support, please reach out to **Ahmed Nule** at [itsahmednule@gmail.com](mailto:itsahmednule@gmail.com).

## License

This project is open source under the **MIT License**. See the [LICENSE](LICENSE) file for details.
