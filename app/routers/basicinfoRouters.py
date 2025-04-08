# app\routers\basicinfoRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi import Body
from controller.basicinfoController import *

router = APIRouter()
@router.get("/type")
async def get_type(db: AsyncSession = Depends(get_db)):
   type_data = await fetch_type(db)
   return type_data