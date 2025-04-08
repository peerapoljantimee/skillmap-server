# app\utils\scraping\scraping.py  run  python -m app.utils.scraping.scraping

from dependencies import get_db 
from controller.classificationController import fetch_classification_by_subcategory
import asyncio

async def get_classification_from_utils(sub_category_id: int):
    """ฟังก์ชันเรียกใช้ fetch_classification_by_subcategory() จาก utils"""
    async for db in get_db():  # ใช้ async generator ดึง session
        result = await fetch_classification_by_subcategory(db, sub_category_id)
        return result  # คืนค่าข้อมูล


if __name__ == '__main__':
    sub_category_id = 6290  # กำหนดค่า sub_category_id ที่ต้องการ
    result = asyncio.run(get_classification_from_utils(sub_category_id))  # ส่ง sub_category_id
    
    # ตรวจสอบว่า result เป็น dictionary และแสดงผลลัพธ์บางส่วน
    print(result['data'][0:10]) 

