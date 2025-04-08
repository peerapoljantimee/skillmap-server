# app\routers\maincategoryRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from controller.maincategoryController import *


router = APIRouter()

@router.get("")
async def get_maincategory(db: AsyncSession = Depends(get_db)):
   
    maincategory_data = await fetch_maincategory(db)
    return maincategory_data