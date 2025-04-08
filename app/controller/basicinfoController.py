import json
import re
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
import random

async def fetch_type(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT type FROM basicinfo;")
      result = await db.execute(stmt)

      type_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': type_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    