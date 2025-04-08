# app\routers\extractskillsRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.extractskillController import *

router = APIRouter()

@router.post("")
async def post_extractskills(request: dict = Body(...)):
    result = await extractskills(request)
    return result

@router.post("/jobs/insert_skills")
async def post_insert_skills(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    result = await insert_skills(request, db)
    return result