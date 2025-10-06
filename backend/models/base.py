"""
Base model classes and database schemas
"""
from typing import Dict, Any, Optional
from datetime import datetime

class BaseModel:
    """Base model class with common functionality"""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

class User(BaseModel):
    """User model"""
    
    def __init__(self, user_id: str, name: str, email: str, 
                 password_hash: str = None, role_id: int = None, 
                 role_name: str = None, signature_path: str = None, 
                 signature_password: str = None, **kwargs):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.role_name = role_name
        self.signature_path = signature_path
        self.signature_password = signature_password
        super().__init__(**kwargs)

class Project(BaseModel):
    """Project model"""
    
    def __init__(self, project_id: int, project_name: str, 
                 project_date: str = None, created_by: str = None,
                 created_at: datetime = None, **kwargs):
        self.project_id = project_id
        self.project_name = project_name
        self.project_date = project_date
        self.created_by = created_by
        self.created_at = created_at
        super().__init__(**kwargs)

class LRU(BaseModel):
    """LRU model"""
    
    def __init__(self, lru_id: int, lru_name: str, project_id: int,
                 created_at: datetime = None, **kwargs):
        self.lru_id = lru_id
        self.lru_name = lru_name
        self.project_id = project_id
        self.created_at = created_at
        super().__init__(**kwargs)

class PlanDocument(BaseModel):
    """Plan Document model"""
    
    def __init__(self, document_id: int, lru_id: int, document_number: str,
                 version: str, revision: str = None, doc_ver: str = None,
                 uploaded_by: str = None, file_path: str = None,
                 status: str = 'not assigned', original_filename: str = None,
                 file_size: int = None, upload_date: datetime = None,
                 is_active: bool = True, **kwargs):
        self.document_id = document_id
        self.lru_id = lru_id
        self.document_number = document_number
        self.version = version
        self.revision = revision
        self.doc_ver = doc_ver
        self.uploaded_by = uploaded_by
        self.file_path = file_path
        self.status = status
        self.original_filename = original_filename
        self.file_size = file_size
        self.upload_date = upload_date
        self.is_active = is_active
        super().__init__(**kwargs)

class NewsUpdate(BaseModel):
    """News Update model"""
    
    def __init__(self, id: int, news_text: str, 
                 created_at: datetime = None, updated_at: datetime = None,
                 hidden: bool = False, **kwargs):
        self.id = id
        self.news_text = news_text
        self.created_at = created_at
        self.updated_at = updated_at
        self.hidden = hidden
        super().__init__(**kwargs)

class Test(BaseModel):
    """Test model"""
    
    def __init__(self, test_id: int, test_name: str,
                 created_at: datetime = None, **kwargs):
        self.test_id = test_id
        self.test_name = test_name
        self.created_at = created_at
        super().__init__(**kwargs)

class Stage(BaseModel):
    """Stage model"""
    
    def __init__(self, stage_id: int, stage_name: str,
                 created_at: datetime = None, **kwargs):
        self.stage_id = stage_id
        self.stage_name = stage_name
        self.created_at = created_at
        super().__init__(**kwargs)

class StageType(BaseModel):
    """Stage Type model"""
    
    def __init__(self, type_id: int, type_name: str, **kwargs):
        self.type_id = type_id
        self.type_name = type_name
        super().__init__(**kwargs)
