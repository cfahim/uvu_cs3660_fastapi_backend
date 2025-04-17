from pydantic import BaseModel

class UserRoleSchema(BaseModel):
    id: int
    name: str

class UserSchema(BaseModel):
    id: int
    username: str
    name: str
    roles: list[UserRoleSchema] = []

class PutUserRolesSchemaRequest(BaseModel):
    set_roles: list[str]