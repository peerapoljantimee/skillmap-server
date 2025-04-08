from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_currency(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT currency FROM salary WHERE currency IS NOT NULL;")
      result = await db.execute(stmt)

      currency_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': currency_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
async def fetch_period(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT period FROM salary WHERE period IS NOT NULL;")
      result = await db.execute(stmt)

      period_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': period_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
