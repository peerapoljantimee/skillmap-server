# app\routers\salaryRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.salaryController import *

router = APIRouter()
@router.get("/currency")
async def get_currency(db: AsyncSession = Depends(get_db)):
   currency_data = await fetch_currency(db)
   return currency_data

@router.get("/period")
async def get_period(db: AsyncSession = Depends(get_db)):
   period_data = await fetch_period(db)
   return period_data

