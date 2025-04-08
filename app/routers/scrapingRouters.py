# app\routers\scrapingRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.scrapingController import *

router = APIRouter()

# http://127.0.0.1:8000/scraping/fetch_jobs_card/?classification_id=6281&subcategory_id=6288
@router.get("/fetch_jobs_card")
async def get_jobs_card(classification_id : int, subcategory_id : int, db: AsyncSession = Depends(get_db)):
    jobs_card = await fetch_jobs_card_by_classification(classification_id, subcategory_id, db)
    return jobs_card


# app\routers\scrapingRouters.py
@router.post("/sreach_jobs_card")
async def post_jobscard(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    classification_id = request.get("classification_id")
    subcategory_id = request.get("subcategory_id")
    jobs_card = await fetch_jobs_card_by_classification(int(classification_id), int(subcategory_id), db)
    return jobs_card


@router.post("/sreach_jobs_details")
async def post_jobsdetails(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    jobs_card = request.get("data")
    jobs_details = await fetch_jobs_details(jobs_card)
    return jobs_details

@router.post("/sreach_jobsposting")
async def post_sreach_jobsposting(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    classification_id = request.get("classification_id")
    subcategory_id = request.get("subcategory_id")
    jobs_posting = await scraping_jobs_by_classification(int(classification_id), int(subcategory_id), db)
    return jobs_posting

@router.post("/jobpostings")
async def post_jobpostings(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
    # print("### request") 
    # print(request)
    result = await insert_jobpostings(request, db)
    print("### jobpostings result")
    print(result)
    return result

