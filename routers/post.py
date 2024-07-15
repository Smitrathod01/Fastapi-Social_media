from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import session

import database,models,schemas,getsession,aouth

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post('/',status_code=status.HTTP_201_CREATED) 
def create_post(request:schemas.Post,db:session = Depends(getsession.get_db),current_user:int=Depends(aouth.get_current_user)):
    createdPost = models.Post_Model(title = request.title,content = request.content,published = request.published,creater_id = current_user)
    db.add(createdPost)
    db.commit()
    db.refresh(createdPost)
    return createdPost

@router.get('/',response_model=list[schemas.showPost])#if you write class config in show post then there is no need to add list u can directly write schemas.showPost
def get_posts(db:session = Depends(getsession.get_db),limit:int = 10,skip:int = 0,search:str = ""):
    posts = db.query(models.Post_Model).filter(models.Post_Model.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get('/myposts',response_model=list[schemas.showPost])#if you write class config in show post then there is no need to add list u can directly write schemas.showPost
def get_posts(db:session = Depends(getsession.get_db),current_user:int=Depends(aouth.get_current_user)):
    posts = db.query(models.Post_Model).filter(models.Post_Model.creater_id == current_user)
    return posts

@router.get('/{id}')
def get_posts(id,db:session = Depends(getsession.get_db)):
    posts = db.query(models.Post_Model).filter(models.Post_Model.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No record found")
    return posts

@router.put('/update/{id}')
def edit_post(id,request:schemas.Post,db:session = Depends(getsession.get_db),current_user:int=Depends(aouth.get_current_user)):
    temp_post = db.query(models.Post_Model).filter(models.Post_Model.id == id).first()

    if not temp_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No record found")
    
    if temp_post.creater_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the owner of this post")
    
    temp_post.title = request.title
    temp_post.content = request.content
    db.commit()
    db.refresh(temp_post)
    return temp_post

@router.delete('/delete/{id}',)
def delete_post(id,db:session = Depends(getsession.get_db),current_user:int=Depends(aouth.get_current_user)):
    temp_post = db.query(models.Post_Model).filter(models.Post_Model.id == id).first()

    if not temp_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No record found")
    
    if temp_post.creater_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not the owner of this post") 
    
    db.delete(temp_post)
    db.commit()
    return {"message":"Post deleted successfully"}









