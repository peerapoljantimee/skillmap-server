# app\routers\companyRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.companyController import *

router = APIRouter()
@router.get("/company_size")
async def get_company_size(db: AsyncSession = Depends(get_db)):
   subcategory_data = await fetch_company_size(db)
   return subcategory_data
 
@router.get("/industry")
async def get_industry(db: AsyncSession = Depends(get_db)):
   industry_data = await fetch_industry(db)
   return industry_data


@router.get("")
async def get_company(db: AsyncSession = Depends(get_db)):
   company_data = await fetch_company(db)
   return company_data


@router.post("")
async def create_company(request: dict = Body(...), db: AsyncSession = Depends(get_db)):
   company_data = await insert_company(request, db)
   return company_data
