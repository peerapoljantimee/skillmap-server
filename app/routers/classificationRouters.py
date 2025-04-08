# app\routers\classificationRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from controller.classificationController import *


router = APIRouter()

@router.get("/subcategory/{subcategory_id}")  # ✅ แก้ path parameter ให้ถูกต้อง
async def get_classification_by_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    """API สำหรับดึง jobs ตาม subcategory_id"""
    classification_by_subcategory = await fetch_classification_by_subcategory(db, subcategory_id)
    return classification_by_subcategory


@router.get("/subcategory")
async def get_subCategory(db: AsyncSession = Depends(get_db)):

    subcategory_data = await fetch_subcategory(db)
    return subcategory_data

# @router.get("")
# async def get_maincategory(db: AsyncSession = Depends(get_db)):
   
#     maincategory_data = await fetch_maincategory(db)
#     return maincategory_data