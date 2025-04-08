# app\routers\imagetotextRouters.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, Form, UploadFile
from typing import List
from controller.imagetotextController import *

router = APIRouter()

@router.post("")
async def post_imagetotext(
    model: str = Form(...),
    files: List[UploadFile] = File(...)
):
   print("###post_imagetotext")
   result =  await process_imagetotext(model, files)
   return result