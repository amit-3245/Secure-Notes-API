#  Secure Notes API (FastAPI)

A secure backend API built with FastAPI that allows users to register using OTP verification, authenticate using JWT, and manage personal notes securely.
This project focuses on real-world authentication, security, and clean backend architecture.
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
