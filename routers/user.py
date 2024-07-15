from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import session

import database,models,schemas,hashing,getsession

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('',status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.Userss,db:session = Depends(getsession.get_db)):
    hashed_password = hashing.hash_password(request.password)
    userdata = models.User_Model(email= request.email,username = request.username,password = hashed_password)
    db.add(userdata)
    db.commit()
    db.refresh(userdata)
    return userdata

@router.get('',response_model = list[schemas.showUser])
def show_users(db:session = Depends(getsession.get_db)):
    users = db.query(models.User_Model).all()
    return users

@router.get('/{id}',response_model = list[schemas.showUser])
def show_users(id,db:session = Depends(getsession.get_db)):
    user = db.query(models.User_Model).filter(models.User_Model.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no record found")
    return user

@router.put('/update/{id}')
def edit_post(id,request:schemas.showUser,db:session = Depends(getsession.get_db)):
    temp_user = db.query(models.User_Model).filter(models.User_Model.id == id).first()
    if not temp_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No record found")
    temp_user.email = request.email
    temp_user.username = request.username
    db.commit()
    db.refresh(temp_user)
    return temp_user

@router.delete('/delete/{id}')
def delete_post(id,db:session = Depends(getsession.get_db)):
    temp_user = db.query(models.User_Model).filter(models.User_Model.id == id).first()
    if not temp_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No record found")
    db.delete(temp_user)
    db.commit()
    return {"message":"Post deleted successfully"}