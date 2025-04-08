# app/controller/maincategoryController.py

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_maincategory(db: AsyncSession):
    try:
        # เขียนคำสั่ง SQL แบบ raw
        stmt = text("SELECT * FROM main_category")
        result = await db.execute(stmt)

        maincategory_list = result.mappings().all()

        # คืนค่าผลลัพธ์
        return {
            "status": "success",
            'data': maincategory_list 
        }
         
    except Exception as e:
        return {"status": "error", "message": str(e)} 