from pydantic import BaseModel, EmailStr,field_validator
import re


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str

    

    @field_validator('first_name')
    def first_name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('First name cannot be empty')
        return v
    
    @field_validator('phone_number')
    def phone_number_valid(cls, v):
        
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(v):
            raise ValueError('Invalid phone number')
        return v

class UserCreate(UserBase):
    password: str
    confirmpassword:str

    @field_validator('confirmpassword')
    def password_conf(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes=True



 
class UserBlog(BaseModel):
    title:str
    content:str
    class Config:
        form_attributes=True
    
