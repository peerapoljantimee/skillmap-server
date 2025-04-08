# app\routers\subCategoryRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from controller.subcategoryController import *

router = APIRouter()
@router.get("")
async def get_subCategory(db: AsyncSession = Depends(get_db)):

    subcategory_data = await fetch_subcategory(db)
    return subcategory_data