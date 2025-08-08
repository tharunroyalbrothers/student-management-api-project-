# Student Management API (Django + DRF)

A Django REST Framework project for managing student details with **user authentication** (register, login, logout, update, delete).  
User must be logged in before they can add, view, update, or delete student details.

## Features

- User authentication system (`loginadmin` app)
  - Register (Required details username, strong password, unique email,unique phone number)
  - Login (should enter the username and password which was created while regestering)
  - Logout (Some user should be logged in before logout)
  - Update profile (username,email and phone number can be updated by logging in)
  - Delete account (Some user should be logged in before delete)
- Student management (`api` app)
  - (IMPORTANT NOTE:- Some user must be logged in before performing any actions below)
  - Add student details (Required details unique usn, name, unique phone number, age, unique email, course)
  - View student details (Usn must be entered of desired student to view his/her details)
  - Update student details (Name, age, course, email, phone number can be updated of desired student)
  - Delete student details (Usn must be entered of desired student whose details need to delete)
- PostgreSQL database integration
- Custom permission messages for unauthenticated users
- Swagger API Documentation (via `drf-yasg`)

---

## USN format

- Here it must contain 10characters
- Format example: 1SJ21CS001
- Validations
  1. It should start with '1SJ' only if it error is raised.
  2. It has 2 letters at position 5 and 6 which represents the course.
  3. Integers are specified to 7,8 and 9 position only.

## Name format

- Name cant be empty or can not contain special characters.
- Accepts alphabetics and periods(.)
- Before and after every period(.) there must be an alphabetic.

## Age format

- Age must be positive interger always.
- Age is constrained from 1 to 99 only here.

## Course format

- Accepts full names and common abbrivations(e.g cse,ec,mech,etc.)
- Internally maps to standard course name.

## Email format

- Perfect email with all validations of email.

## Phone number format

- Accepts all the Indian phone numbers whose length is 10

---

## How to Run

- Ensure you have **Python 3.x** installed on your system.
- Ensure you have **Django 5.2.4** installed on your system.
- Ensure you have some app for PostgreSQL like PGAdmin.
- Download or clone this repository.
- Navigate to the project directory in the terminal.
- Run the local server.

---
## Install required dependencies:

- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

## API Documentation:
- Swagger UI is available at
    - http://127.0.0.1:8000/swagger/
    
- Redoc is available at
    - http://127.0.0.1:8000/redoc/
    