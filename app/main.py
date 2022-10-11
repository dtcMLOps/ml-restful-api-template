import secrets
import os

from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_simple_security import api_key_router, api_key_security
from fastapi_versioning import VersionedFastAPI, version

from app.core import constants
from app.core.addition import addition
from app.core.config import settings
from app.database import init_db
from app.routers import sample_bg, teams
from app.schemas.addition_schema import AdditionInput, AdditionResults
from app.schemas.heartbeat_schema import ResponseCommon
from app.settings import description, tags_metadata


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        version="0.0.1",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Addition API developer",
            "url": "https://ab-inbev.com/contact/",
            "email": "xyz@ab-inbev.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        openapi_tags=tags_metadata,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app

# Basic auth
security = HTTPBasic()

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "root")
    correct_password = secrets.compare_digest(credentials.password, "root")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



app = get_application()
app.include_router(api_key_router, prefix="/auth", tags=["_auth"])
app.include_router(teams.router, tags=["Team"], dependencies=[Depends(basic_auth)])
app.include_router(sample_bg.router, tags=["BackgroundTask"], dependencies=[Depends(basic_auth)])


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/ping", tags=["health check"])
def pong():
    return {"ping": "pong!"}


@app.post(
    "/addition/",
    description="Addition of all the numbers in a list.",
    response_model=AdditionResults,
    tags=["addition"],
)
async def update_item(input_list: AdditionInput):
    results = addition(input_list.input_list)
    return {"results": results}


@app.get(
    "/heartbeat", description="HeartBeat API to test the application", response_model=ResponseCommon, tags=["Heartbeat"]
)
def heartbeat():
    common_msg = ResponseCommon(status=status.HTTP_200_OK, message=constants.STATUS)
    return common_msg


# Admin panel registration

from sqladmin import Admin, ModelAdmin
from .database import engine
from .models import Team
admin = Admin(app, engine)

class TeamAdmin(ModelAdmin, model=Team):
    column_list = [Team.id, Team.name]


admin.register_model(TeamAdmin)

