# Online Leave Management System

The Online Leave Management System is a Django-based web application designed to manage employee leave requests, track leave balances, and handle notifications. It allows users to apply for different types of leave, view their leave balances, and receive notifications related to their leave status.

## Features

- **User Authentication**: Login, logout, and password management.
- **Leave Management**: Users can apply for leave, view the status of their applications, and check their leave balances.
- **Notifications**: Users receive notifications about the status of their leave applications.
- **Admin Interface**: Admin users can manage users, leave types, and leave applications through Django's admin interface.

## Author

**Judy Auma**

## License

This project is licensed under the Nairobi Technical Training Institute.

## Prerequisites

- Python 3.x
- Django
- SQLite (default database)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ahmednule/Online_leave_Management_system.git
cd online-leave-management-system
2. Set Up a Virtual Environment
For Windows:

bash
Copy code
python -m venv venv
venv\Scripts\activate
For Linux/Mac:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
in windows --> pip install Django
in bash apt-get install django
4. Apply Migrations
bash
Copy code
python manage.py migrate
5. Load Initial Data
If you want to prepopulate the database with existing user data:

bash
Copy code
python manage.py loaddata users_all_fixture.json
6. Create a Superuser (Optional)
If you need to create a superuser for admin access:

bash
Copy code
python manage.py createsuperuser
7. Run the Development Server
bash
Copy code
python manage.py runserver
8. Access the Application
Open your web browser and go to http://127.0.0.1:8000/ to access the application.

Using Fixture Files
This project includes a fixture file users_all_fixture.json that can be used to prepopulate the database with existing users, profiles, and other data.

To load the fixture data into your local database:

bash
Copy code
python manage.py loaddata users_all_fixture.json
This ensures you have a similar starting point to the original project setup.

Contributing
Feel free to fork this project and submit pull requests. Any contributions are welcome.

Contact
For any inquiries or support, please contact Judy Auma at judyauma@gmail.com.