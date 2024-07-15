from fastapi import FastAPI,Depends,status,HTTPException,APIRouter

from routers import post,user,auth,like

app = FastAPI()

#related to posts
app.include_router(post.router)

#related to users
app.include_router(user.router)

#related to authentication
app.include_router(auth.router)                                                             

#related to likes
app.include_router(like.router)








    











    
    



















    




