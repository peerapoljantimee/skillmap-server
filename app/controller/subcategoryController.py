# app/controller/subCategoryController.py

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_subcategory(db: AsyncSession):
    try:
        # เขียนคำสั่ง SQL แบบ raw
        stmt = text("SELECT * FROM sub_category")
        result = await db.execute(stmt)

        subcategory_list = result.mappings().all()

        # คืนค่าผลลัพธ์
        return {
            "status": "success",
            'data': subcategory_list 
        }
         
    except Exception as e:
        return {"status": "error", "message": str(e)} 