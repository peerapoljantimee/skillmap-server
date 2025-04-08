# app\routers\jobsRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.jobsController import *

router = APIRouter()

@router.get("/jobsposting")
async def get_jobs(db: AsyncSession = Depends(get_db)):
    jobs = await fetch_jobs(db)
    return jobs

@router.get("/jobsposting/unextracted-skills")
async def get_jobs(db: AsyncSession = Depends(get_db)):
    jobs = await fetch_jobs_unextracted_skills(db)
    return jobs

@router.post("/jobpostings")
async def create_jobs(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    job_data = await insert_jobpostings(request, db)
    return job_data

# @router.post("/jobpostings")
# async def post_jobpostings(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     # print("### request") 
#     # print(request)
#     result = await insert_jobpostings(request, db)
#     print("### jobpostings result")
#     print(result)
#     return result