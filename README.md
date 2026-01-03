#  Secure Notes API (FastAPI)

A real-world backend API built with FastAPI that provides secure user authentication using OTP verification, JWT-based login, and user-specific notes management.

This project is designed with production-style architecture, proper security practices, and clean code structure.

---

# Features

# Authentication & Security
- OTP-based user registration (email verification)
- Secure password hashing using bcrypt
- JWT-based authentication (Bearer token)
- Protected routes using dependency injection
- Forgot password (OTP based)
- Reset password
- Change password (authenticated user)

# Notes Management
- Create notes
- Read user-specific notes
- Update notes
- Delete notes
- One user cannot access another user’s data

# Email Integration
- OTP sent via email using SMTP (Gmail)
- Centralized email service

---

# Tech Stack Used

- Python
- FastAPI
- SQLAlchemy ORM
- MySQL
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- SMTP (Gmail)
- Uvicorn
