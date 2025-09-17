# Role-Based Login System

This document describes the implementation of the role-based login system for the AVIATRAX application.

## Overview

The system now implements proper role-based authentication where:
1. Users are authenticated via email and password
2. User roles are fetched from the `user_roles` and `roles` tables
3. Frontend navigation is automatically determined based on the user's role
4. Passwords are properly hashed using SHA-256

## Database Schema

The system uses three main tables:

### `users` table
- `user_id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `password_hash`: SHA-256 hashed password

### `roles` table
- `role_id`: Primary key
- `role_name`: Role name (Admin, QA Head, QA Reviewer, Design Head, Designer)

### `user_roles` table
- `user_role_id`: Primary key
- `user_id`: Foreign key to users table
- `role_id`: Foreign key to roles table
- `assigned_at`: Timestamp when role was assigned

## Setup Instructions

### 1. Database Setup
Run the SQL queries from `queries.sql` to create the necessary tables and sample data.

### 2. Update Existing Passwords
If you have existing users with plain text passwords, run:
```bash
cd backend
python update_passwords.py
```

This will hash all existing passwords using SHA-256.

### 3. Start the Backend
```bash
cd backend
python app.py
```

The Flask server will start on `http://127.0.0.1:5000`

### 4. Test the System
Run the test script to verify database connectivity:
```bash
cd backend
python test_login.py
```

## API Endpoints

### POST /api/login
Authenticates a user and returns role information.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1001,
    "name": "User Name",
    "email": "user@example.com",
    "role": "QA Reviewer"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Invalid password"
}
```

## Role-Based Navigation

After successful login, users are automatically redirected based on their role:

| Role | Route | Component |
|------|-------|-----------|
| Admin | `/admin` | `HomePageAdmin` |
| QA Head | `/qahead/home` | `HomePageQAHead` |
| QA Reviewer | `/reviewer/home` | `HomePageReviewer` |
| Design Head | `/designhead/home` | `HomePageDesignHead` |
| Designer | `/designer/home` | `HomePageDesigner` |

## Security Features

1. **Password Hashing**: All passwords are hashed using SHA-256
2. **Input Validation**: Email and password are validated before processing
3. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
4. **SQL Injection Protection**: Uses parameterized queries
5. **CORS Support**: Configured for frontend integration

## Testing

### Sample Users
The system comes with sample users for testing:

| Email | Password | Role |
|-------|----------|------|
| avanthikapg22@gmail.com | reviewer | QA Reviewer |
| sudhikshamk06@gmail.com | admin | Admin |
| mahadevmanohar07@gmail.com | designhead | Design Head |
| mohan@gmail.com | qahead | QA Head |
| mahaashri@gmail.com | designer | Designer |

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials in `app.py`
   - Ensure database "ERP" exists

2. **Login Fails**
   - Check if passwords were updated using `update_passwords.py`
   - Verify user exists in database
   - Check user has assigned role

3. **Role Navigation Issues**
   - Verify route names match exactly in router configuration
   - Check role names in database match expected values

### Debug Mode
Enable debug logging by setting `debug=True` in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

## Future Enhancements

1. **JWT Tokens**: Implement JWT-based authentication
2. **Password Reset**: Add password reset functionality
3. **Session Management**: Implement proper session handling
4. **Rate Limiting**: Add login attempt rate limiting
5. **Audit Logging**: Log login attempts and user actions
