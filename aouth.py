from jwt.exceptions import InvalidTokenError
import jwt
from datetime import datetime,timedelta,timezone
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_token(data:dict):
    temp_data = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    temp_data.update({"exp":expire})

    final_data = jwt.encode(temp_data,SECRET_KEY,algorithm=ALGORITHM)
    return final_data

def verify_access_token(token:str,credentials_exception):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        userId = payload.get("user_id")
        print(userId)
        if userId is None:
            
            raise credentials_exception
        
     
    except PyJWTError:
                                            
        raise credentials_exception
    
    return userId
    

def get_current_user(token:str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Oops You are not authorized",headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token,credentials_exception)
    
                        

