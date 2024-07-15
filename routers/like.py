from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import session

import database,models,schemas,getsession,aouth

router = APIRouter(
    prefix="/like",
    tags=['Likes']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def like_post(request:schemas.likes,db:session = Depends(getsession.get_db),current_user:int=Depends(aouth.get_current_user)):
    post = db.query(models.Post_Model).filter(models.Post_Model.id == request.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not available")
    
    if request.like_dir not in [0,1] :
        print(request.post_id)
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="pls make sure you have entered the like dir 0 or 1")
    else:
        found_like = db.query(models.Like_Model).filter(models.Like_Model.post_id==request.post_id,models.Like_Model.user_id == current_user).first()
        if request.like_dir ==1:
            if found_like:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="You have already liked this post")
            
            create_like = models.Like_Model(post_id = request.post_id ,user_id = current_user)
            db.add(create_like)
            db.commit()
            db.refresh(create_like)
            return {"message":"Successfully liked"}
        
        elif request.like_dir==0:
            if not found_like:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Like not found")
            
            db.delete(found_like)
            db.commit()
            return {"message":"Successfully unliked"}

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Its a bad request")
        
@router.get('/',response_model=list[schemas.showlikes])
def show_like(db:session = Depends(getsession.get_db)):
    likes = db.query(models.Like_Model).all()
    return likes
        
#remember one thing is still left that total number of likes is remaining to show on posts


