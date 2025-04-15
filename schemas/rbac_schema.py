# schemas/rbac_schema.py
from pydantic import BaseModel
from typing import List

class PermissionSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RolePermissionSchema(BaseModel):
    permission: PermissionSchema

    class Config:
        from_attributes = True

class RoleSchema(BaseModel):
    id: int
    name: str
    role_permissions: List[RolePermissionSchema]

    class Config:
        from_attributes = True



class PutRoleSchemaRequest(BaseModel):    
    role_permissions: List[str]

