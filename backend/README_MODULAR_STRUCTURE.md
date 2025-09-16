# AVIATRAX Backend - Modular Structure

## Overview

The backend has been refactored from a single monolithic `app.py` file (2659 lines) into a clean, modular structure using Flask blueprints and organized components.

## New Structure

```
backend/
├── app_new.py              # New modular application entry point
├── app.py                  # Legacy version (kept as backup)
├── config.py               # Configuration and database connection
├── requirements.txt        # Dependencies
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── helpers.py          # Common helper functions
│   └── database_init.py    # Database initialization
├── routes/                 # Modular route blueprints
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── projects.py        # Project and LRU management
│   ├── users.py           # User management
│   ├── documents.py       # Plan document management
│   ├── tests.py           # Test configuration management
│   ├── news.py            # News updates management
│   └── files.py           # File upload and serving
└── models/                 # Data models and schemas
    ├── __init__.py
    └── base.py            # Base model classes
```

## Key Improvements

### 1. **Separation of Concerns**
- Each module handles a specific domain (auth, projects, users, etc.)
- Clear separation between configuration, business logic, and data models
- Utility functions organized in dedicated modules

### 2. **Maintainability**
- Code is split into manageable files (100-400 lines each)
- Easy to locate and modify specific functionality
- Clear module boundaries and dependencies

### 3. **Scalability**
- New features can be added as separate blueprints
- Easy to add new routes without modifying existing code
- Modular structure supports team development

### 4. **Configuration Management**
- Centralized configuration in `config.py`
- Database connection handling abstracted
- Environment-specific settings support

## Module Breakdown

### config.py
- Application configuration settings
- Database connection management
- File upload configurations

### utils/helpers.py
- Password hashing and verification
- File validation functions
- Upload directory creation
- Database error handling

### utils/database_init.py
- Database table initialization
- Schema setup and migrations

### routes/auth.py
- User login endpoint
- Authentication logic
- Session management

### routes/projects.py
- Project CRUD operations
- LRU management
- Project-LRU relationships
- Serial number management

### routes/users.py
- User management (create, read, update)
- Role management
- User-role assignments
- Reviewer management

### routes/documents.py
- Plan document upload and management
- Document status updates
- Reviewer assignments
- Document versioning

### routes/tests.py
- Test configuration management
- Stage and stage type management
- Test-stage-type configurations
- Debug endpoints

### routes/news.py
- News updates management
- Soft delete functionality
- Repost functionality
- Bulk operations

### routes/files.py
- File serving endpoints
- Background image management
- File upload handling
- Security checks

### models/base.py
- Base model classes
- Data transfer objects
- Type definitions
- Common model functionality

## Running the Application

### Option 1: Use the new modular structure (Recommended)
```bash
cd backend
python app_new.py
```

### Option 2: Use the legacy version (Backup)
```bash
cd backend
python app.py
```

## Benefits of the New Structure

1. **Easier Debugging**: Issues can be isolated to specific modules
2. **Better Testing**: Each module can be tested independently
3. **Code Reusability**: Utility functions can be reused across modules
4. **Team Collaboration**: Multiple developers can work on different modules
5. **Performance**: Easier to optimize specific components
6. **Documentation**: Each module has clear responsibilities

## Migration Notes

- All existing endpoints remain functional
- No breaking changes to the API
- Database connections and configurations are preserved
- File upload functionality maintained
- All business logic preserved

## Future Enhancements

With this modular structure, you can easily:
- Add new API endpoints as separate blueprints
- Implement caching layers for specific modules
- Add middleware for authentication and authorization
- Implement API versioning
- Add comprehensive logging per module
- Create unit tests for each component
- Add API documentation with Swagger/OpenAPI

## Dependencies

The modular structure uses the same dependencies as the original:
- Flask
- Flask-CORS
- psycopg2
- Standard Python libraries

No additional dependencies were introduced during the refactoring.
