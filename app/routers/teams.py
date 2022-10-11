from fastapi import APIRouter, Depends, Query
from pydantic.types import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import TeamCreate, TeamRead, TeamUpdate
from app.services.teams_crud import create_team, delete_team, read_team, read_teams, update_team, update_team_put
from sqlmodel import Session

router = APIRouter(prefix="/teams")


@router.post("/", description="Creates a teams.", response_model=TeamRead)
async def create_a_team(team: TeamCreate, db: Session = Depends(get_session)):
    results = await create_team(team=team, db=db)
    return results


@router.get("/", description="Gets all the teams.", response_model=List[TeamRead])
async def get_teams(
    db: AsyncSession = Depends(get_session),
):
    results = await read_teams(db=db)
    return results


@router.get("/{name}", description="Gets a particular team.", response_model=TeamRead)
async def get_a_team(name: str, db: AsyncSession = Depends(get_session)):
    results = await read_team(name=name, db=db)
    return results


@router.put("/{name}", description="Updates a particular team.", response_model=TeamRead)
async def update_a_team(name: str, team: TeamUpdate, db: AsyncSession = Depends(get_session)):
    results = await update_team_put(name=name, team=team, db=db)
    return results


@router.delete(
    "/{id}",
    description="Deletes a particular team.",
)
async def delete_a_team(id: int, db: AsyncSession = Depends(get_session)):
    results = await delete_team(id=id, db=db)
    return results


@router.patch("/{id}", description="Updates a particular team.", response_model=TeamRead)
async def update_a_team(id: int, team: TeamUpdate, db: AsyncSession = Depends(get_session)):
    results = await update_team(id=id, team=team, db=db)
    return results
