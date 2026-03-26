from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
import model,schemas,utils
from auth_database import get_db
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

SECRET_KEY = "xS7yIeqMaoZmpSux9YzAk00ezzqv2Pag57TlqWKMHE0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#Helper function that takes user data
def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return encoded_jwt

app = FastAPI()
@app.post("/signup")
def register_user(user:schemas.UserCreate,db:Session = Depends(get_db)): 
  # check the user exit or not
  existing_user = db.query(model.User).filter(model.User.username == user.username).first()
  if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
  # Hash password
  hashed_pass = utils.hash_password(user.password)
  
  # create new user instance
  new_user = model.User(
      username=user.username,
      email=user.email,
      hashed_password=hashed_pass,
      role="user"   # ✅ set from backend only
  )
  
  # Save user to database
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
# return the value (except password)
  return {'id': new_user.id, "username": new_user.username,"email":new_user.email,"role": new_user.role}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
  user = db.query(model.User).filter(model.User.username == form_data.username).first()
  if not user:
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Username")
  
  if not utils.verify_password(form_data.password,user.hashed_password):
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "Invalid Password")
  
  token_data = {'sub':user.username, 'role':user.role}
  token = create_access_token(token_data)
  return {'access_token': token, "token_type": "bearer"}


                                                

