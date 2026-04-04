# Online Leave Management System

A professional, full-featured web application built with Django for managing employee leave requests — from applying for leave to tracking approvals, all through a modern, responsive UI with a dedicated admin panel.

## Table of Contents

- [Screenshots](#screenshots)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Email Configuration](#email-configuration)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## Screenshots

### Login
![Login](screenshots/login.png)

### User Dashboard
![User Dashboard](screenshots/user-dashboard.png)

### Apply for Leave
![Apply for Leave](screenshots/leave.png)

### Leave Balance
![Leave Balance](screenshots/balance.png)

### My Applications
![My Applications](screenshots/my-application.png)

### Profile
![Profile](screenshots/profile.png)

### Team Calendar
![Team Calendar](screenshots/calendar.png)

### Admin Dashboard
![Admin Dashboard](screenshots/admin-dashboard.png)

### Password Reset
![Password Reset](screenshots/password-reset.png)

## Features

### For Employees

- **User Authentication**: Secure login, logout, and password management with email-based password reset.
- **User Registration**: New employees can create accounts with role and department information.
- **Leave Application**: Apply for leave with type, date range, and reason. Includes duplicate/overlap prevention.
- **Leave Balance**: View your remaining annual, sick, and other leave days with auto-deduction on approval.
- **Leave Status Tracking**: Track all your leave applications with status badges (Pending, Approved, Rejected, Cancelled).
- **Leave Detail View**: Dedicated page with full details of each leave application.
- **Cancel Pending Requests**: Cancel your own pending leave applications before they are processed.
- **Profile Management**: Update your role, department, contact information, and password.
- **Sidebar Navigation**: Professional left sidebar for quick access to all pages.

### For Administrators

- **Admin Analytics Dashboard**: Overview with stat cards (total employees, applications, pending, approval rate), donut chart (by status), bar chart (by leave type), and recent applications table.
- **Professional Admin UI**: Custom sidebar-based layout matching the user portal design.
- **Leave Management**: View, approve, or reject all employee leave applications with audit trail tracking.
- **Bulk Actions**: Approve or reject multiple leave applications at once from the list view.
- **Rejection Reason**: Mandatory reason field when rejecting, with in-app notification to the employee.
- **Auto Balance Deduction**: Leave days automatically deducted from employee balances upon approval.
- **Email Notifications**: Employees receive email notifications when their leave is approved or rejected.
- **Team Calendar**: Visual monthly calendar showing who is on approved leave at a glance.
- **Leave Type Management**: Add, edit, or delete leave type categories.
- **User Management**: Full CRUD for users, profiles, and employee details via Django admin.
- **Audit Trail**: Tracks who approved/rejected each leave and when.
- **Search & Filter**: Search by employee name/username, filter by status and date range.
- **Pagination**: Manage large lists with built-in pagination.

### System Features

- **Professional UI**: Modern, responsive design with Inter font, Bootstrap 5, and Bootstrap Icons.
- **Consistent Design**: Matching dark sidebar layout for both user portal and admin panel.
- **Responsive Design**: Works on desktop and mobile devices with collapsible sidebar.
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

```bash
git clone https://github.com/ahmednule/Online_leave_Management_system.git
cd Online_leave_Management_system
```

#### Step 2: Set Up a Virtual Environment

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Apply Migrations

```bash
python manage.py migrate
```

#### Step 5: Create an Admin User

```bash
python manage.py createsuperuser
```

#### Step 6: Run the Development Server

```bash
python manage.py runserver
```

#### Step 7: Access the Application

Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

### URL Routes

| URL | Description |
|-----|-------------|
| `/` | Dashboard — overview, stats, recent leaves, notices |
| `/apply/` | Submit a new leave application |
| `/balance/` | View your leave balance |
| `/notifications/` | View all your leave applications with filters |
| `/profile/` | Manage your profile and change password |
| `/calendar/` | Team leave calendar (admin access) |
| `/accounts/login/` | Login page (redirects superusers to `/admin/`) |
| `/accounts/register/` | Employee registration |
| `/accounts/password-reset/` | Request password reset email |
| `/admin/` | Admin panel — analytics dashboard, leave management, user management |

### Authentication Flow

- **Regular users** log in and are redirected to the **Dashboard** (`/`).
- **Superusers** log in and are redirected to the **Admin Panel** (`/admin/`).
- After logout, all users are redirected to the login page.

### Admin Panel

The admin panel at `/admin/` features:

1. **Analytics Dashboard** — Stat cards, charts, and recent applications.
2. **Leave Management** — Applications, Balances, Leave Types (via sidebar).
3. **User Management** — Users, Profiles, Employee Details (via sidebar).
4. **Content** — Awards, Notices (via sidebar).
5. **Notifications** — System notifications (via sidebar).

### Creating Leave Types

As an admin, go to `/admin/` and navigate to **Leave Management > Leave Types** to add new categories (e.g., Annual Leave, Sick Leave, Maternity Leave, Paternity Leave).

### Setting Up Leave Balances

New users automatically get a default balance (20 annual, 10 sick, 5 other days). Admins can modify balances through the admin panel at `/admin/`.

## Email Configuration

The system uses a console email backend by default (emails print to the terminal). For production, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'Leave System <noreply@example.com>'
```

## Contributing

We welcome contributions! Fork this project and submit pull requests.

## Contact

For any inquiries or support, please reach out to **Ahmed Nule** at [itsahmednule@gmail.com](mailto:itsahmednule@gmail.com).

## License

This project is open source under the **MIT License**. See the [LICENSE](LICENSE) file for details.
