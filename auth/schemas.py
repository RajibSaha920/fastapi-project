from pydantic import BaseModel,EmailStr,Field,ConfigDict

# Schema for new user
class UserCreate(BaseModel):
  username: str = Field(min_length=3, max_length=50)
  email:EmailStr
  password: str = Field(min_length=6, max_length=100) 
  
# Schema for user login
class UserLogin(BaseModel):
  username:str
  password:str
  
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)
  
  
  