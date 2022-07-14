from fastapi import FastAPI
from database.config import engine, Base
from modules.authentication.routers import authentication_routes
from modules.users.routers import user_routes
from modules.permissions.routers import permession_routes


from tests.email_sender import email_sender_path_operations


app = FastAPI()


# registering the modules routers
app.include_router(authentication_routes.router)
app.include_router(user_routes.router)
app.include_router(permession_routes.router)

# Test endpoints
app.include_router(email_sender_path_operations.router)

Base.metadata.create_all(engine)