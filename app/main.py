from fastapi import FastAPI

from app import user
from app.routes import auth, event, registration
from app.database import engine, Base
from app.models import User, Event, Registration

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(event.router)
app.include_router(registration.router)
app.include_router(user.router )

@app.get("/")
def read_root():
    return {"Hello": "event_management_system"}