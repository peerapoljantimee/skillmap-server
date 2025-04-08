# app\routers\tablesRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from controller.tablesController import *

router = APIRouter()

@router.get("/")
async def get_tables(db: AsyncSession = Depends(get_db)):
    """API สำหรับดึงตารางทั้งหมดจากฐานข้อมูล"""
    tables = await fetch_tables(db)
    return tables
