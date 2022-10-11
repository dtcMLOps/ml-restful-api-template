from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import Team, TeamCreate, TeamUpdate


async def create_team(team: TeamCreate, db: AsyncSession = Depends(get_session)):
    team_to_db = Team.from_orm(team)
    db.add(team_to_db)
    await db.commit()
    await db.refresh(team_to_db)
    return team_to_db


async def read_teams(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Team))
    teams = result.scalars().all()
    # teams = result.fetchall()
    return teams



async def read_team(name: str, db: AsyncSession = Depends(get_session)):
    statement = select(Team).where(Team.name == name)
    result = await db.execute(statement)
    team = result.scalar_one_or_none()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team not found with name: {name}",
        )
    return team

async def update_team_put(name: str, team: TeamUpdate, db: AsyncSession = Depends(get_session)):
    statement = (
        update(Team)
        .where(Team.name==name)
        .values(headquarters=team.headquarters, name=team.name)
        .execution_options(synchronize_session='fetch')
    )
    await db.execute(statement)
    await db.commit()

    statement = select(Team).where(Team.name == team.name)
    result = await db.execute(statement)
    team_to_update = result.scalar_one_or_none()
    return team_to_update


async def update_team(id: int, team: TeamUpdate, db: AsyncSession = Depends(get_session)):
    # team_to_update = db.get(Team, team_id)
    statement = select(Team).where(Team.id == id)
    result = await db.execute(statement)
    team_to_update = result.scalar_one_or_none()
    if not team_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team not found with id: {id}",
        )

    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team_to_update, key, value)

    db.add(team_to_update)
    await db.commit()
    await db.refresh(team_to_update)
    return team_to_update


async def delete_team(id: int, db: AsyncSession = Depends(get_session)):
    # team = await db.get(Team, id)
    statement = select(Team).where(Team.id == id)
    result = await db.execute(statement)
    team = result.scalar_one_or_none()
    print(team)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team not found with id: {id}",
        )

    await db.delete(team)
    await db.commit()
    return {"ok": True}


