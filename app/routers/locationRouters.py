# app\routers\locationRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.locationController import *

router = APIRouter()
@router.get("/country")
async def get_city(db: AsyncSession = Depends(get_db)):
   country_data = await fetch_country(db)
   return country_data

@router.get("/city")
async def get_city(db: AsyncSession = Depends(get_db)):
   city_data = await fetch_city(db)
   return city_data

@router.get("/area")
async def get_area(db: AsyncSession = Depends(get_db)):
   area_data = await fetch_area(db)
   return area_data