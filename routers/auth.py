from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   

import database,models,schemas,hashing,getsession,aouth

router = APIRouter(tags=['Authentication'])

@router.post('/login')
# def login(request:OAuth2PasswordRequestForm=Depends(),db:session=Depends(getsession.get_db)):   --when you use requestform then u have to add username in place of email because it doesnt have any thing like email 
def login(request:schemas.authentication,db:session=Depends(getsession.get_db)):
    test_user = db.query(models.User_Model).filter(models.User_Model.email == request.email).first()
    if not test_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No user found')
    
    final_user = hashing.verify_password(request.password,test_user.password)
    
    if not final_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid credentials')     

    token = aouth.create_token(data={"user_id":test_user.id})
    print('hello')                                                                      
    return {"access_token": token, "token_type": "bearer"}



