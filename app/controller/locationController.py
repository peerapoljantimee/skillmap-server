from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_country(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT country FROM location WHERE country IS NOT NULL ORDER BY country ;")
      result = await db.execute(stmt)

      country_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': country_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
async def fetch_city(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT city FROM location WHERE city IS NOT NULL ORDER BY city;")
      result = await db.execute(stmt)

      city_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': city_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
async def fetch_area(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT area FROM location WHERE area IS NOT NULL ORDER BY area;")
      result = await db.execute(stmt)

      area_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': area_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 