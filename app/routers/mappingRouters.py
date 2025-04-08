# app\routers\mapping.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.mappingController import *



router = APIRouter()

@router.get("/hard_skills")
async def get_hard_skills(db: AsyncSession = Depends(get_db)):
    hard_skills = await fetch_hard_skills(db)
    return hard_skills
 
@router.get("/soft_skills")
async def get_soft_skills(db: AsyncSession = Depends(get_db)):
    soft_skills = await fetch_soft_skills(db)
    return soft_skills

@router.post("/retrieval")
async def posr_retrieval(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    jobs = await retrieval(request, db)
    # print(json.dumps(jobs, indent=4, ensure_ascii=False))
    return jobs