from pydantic.types import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint

class TeamBase(SQLModel):

    name: str = Field(index=True, min_length=3, max_length=50, sa_column_kwargs={"unique": True})
    headquarters: str = Field(..., min_length=3, max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "name": "MLteam",
                "headquarters": "Brazil",
            }
        }


class Team(TeamBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(TeamBase):
    name: Optional[str] = None
    headquarters: Optional[str] = None

