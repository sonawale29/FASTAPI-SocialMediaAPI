from fastapi import FastAPI,Depends
from db.database import Base, engine
from dependencies import get_current_user
from routes import user_routes,post_routes

from fastapi.security import OAuth2PasswordBearer

# Initialize FastAPI app
app = FastAPI()
# Define the OAuth2 scheme for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(user_routes.router)
app.include_router(post_routes.post_router)


# Event to start database connection
@app.on_event("startup")
async def startup():
    print("Starting the application...")


@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You have access!", "user": current_user}


# Event to stop database connection
@app.on_event("shutdown")
async def shutdown():
    print("Shutting down the application...")
