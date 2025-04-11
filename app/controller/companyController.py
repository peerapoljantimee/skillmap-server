import json
import re
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
import random

async def fetch_company_size(db: AsyncSession):
   try:
      stmt = text("""
      SELECT DISTINCT company_size
      FROM company
      WHERE company_size IS NOT NULL
      ORDER BY 
      CASE 
         WHEN company_size = '11-50 employees' THEN 1
         WHEN company_size = '51-100 employees' THEN 2
         WHEN company_size = '101-1,000 employees' THEN 3
         WHEN company_size = '1,001-5,000 employees' THEN 4
         WHEN company_size = '5,001-10,000 employees' THEN 5
         WHEN company_size = 'More than 10,000 employees' THEN 6
         ELSE 7
      END;         
      """)
      result = await db.execute(stmt)

      company_size_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': company_size_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
async def fetch_industry(db: AsyncSession):
   try:
      stmt = text("SELECT DISTINCT industry FROM company WHERE industry IS NOT NULL ORDER BY industry;")
      result = await db.execute(stmt)

      industry_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': industry_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
    
async def fetch_company(db: AsyncSession):
   try:
      stmt = text("""
      SELECT 
         comp.company_id, 
         comp.name, 
         comp.short_name, 
         comp.industry, 
         comp.verified, 
         comp.company_search_url,
         comp.registration_date, 
         comp.company_size, 
         COUNT(j.job_id) AS count_jobs
      FROM company comp
      LEFT JOIN jobs j ON comp.company_id = j.company_id
      GROUP BY 
         comp.company_id, 
         comp.name, 
         comp.short_name, 
         comp.industry, 
         comp.verified, 
         comp.company_search_url,
         comp.registration_date,  
         comp.company_size;         
      """)
      result = await db.execute(stmt)

      company_list = result.mappings().all()

      # คืนค่าผลลัพธ์
      return {
         "status": "success",
         'data': company_list 
         }
   
   except Exception as e:
       return {"status": "error", "message": str(e)} 
    
async def insert_company(request: dict, db: AsyncSession): 
   try:
      print("request")
      print(request)
      
      # ตรวจสอบว่ามี company_id มาในคำขอหรือไม่
      company_id = request.get("company_id")
      
      # ใช้ AS new_data เป็น alias และใช้ new_data.column แทน VALUES(column)
      company_stmt = text("""
      INSERT INTO company (
          name, short_name, industry, verified,
          company_search_url, company_size
      )
      VALUES (
          :name, :short_name, :industry, :verified,
          :company_search_url, :company_size
      ) AS new_data
      ON DUPLICATE KEY UPDATE
          name = new_data.name,
          short_name = new_data.short_name,
          industry = new_data.industry,
          verified = new_data.verified,
          company_search_url = new_data.company_search_url,
          company_size = new_data.company_size
      """)
      
      await db.execute(company_stmt, {
         # "company_id": company_id,
         "name": request.get("name"),
         "short_name": request.get("short_name"),
         "industry": request.get("industry"),
         "verified": request.get("verified", 0),
         "company_search_url": request.get("company_search_url"),
         "company_size": request.get("company_size")
      })
      
      # ดึง company_id ที่เพิ่งสร้าง
      last_id_stmt = text("SELECT LAST_INSERT_ID() AS company_id")
      result = await db.execute(last_id_stmt)
      company_id_row = result.fetchone()  # ไม่ต้องใช้ await เพราะ fetchone() ไม่ใช่ coroutine
      company_id = company_id_row[0] if company_id_row else None
      print("company_id", company_id)
      
      # เพิ่ม company_id เข้าไปใน response
      response_data = request.copy()
      response_data["company_id"] = company_id
      
      await db.commit()
      
      return {
          "status": "success",
          "data": response_data
      }

   except Exception as e:
      await db.rollback()
      print(f"Error: {str(e)}")
      return {"status": "error", "message": str(e)}
    
    
    
    