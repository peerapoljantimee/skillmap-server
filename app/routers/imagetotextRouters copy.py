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
    try:
        # อ่านเนื้อหาของไฟล์ทั้งหมดที่ได้รับ
        file_contents = []
        file_info = []
        
        for file in files:
            content = await file.read()
            file_info.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content)
            })
            file_contents.append(content)
            # ต้อง seek กลับไปที่ต้นไฟล์หลังจากอ่าน
            # await file.seek(0)
        
        # เรียกใช้งาน API ที่เหมาะสมตามโมเดลที่เลือก
        if model == "gemini":
            # ส่งรูปภาพไปยัง Gemini API
            extracted_text = await process_with_gemini(file_contents[0])
      #   elif model == "google_openai":
      #       # ส่งรูปภาพไปยัง Google Vision และ OpenAI
      #       extracted_text = await process_with_google_and_openai(file_contents[0])
        else:
            return {"status": "error", "message": "โมเดลไม่ถูกต้อง"}
        
        # ส่งผลลัพธ์กลับไปยัง frontend
        result = {
            "status": "success",
            "model": model,
            "file": file_info,
            "extracted_text": extracted_text
        }
        print(result)
        return result
    
    except Exception as e:
        result = {
            "status": "error",
            "message": str(e)
        }
        return result