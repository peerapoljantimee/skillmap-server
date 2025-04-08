# app/dependencies.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from repository.database import engine

# สร้าง sessionmaker ที่ใช้ asynchronous
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# ฟังก์ชันสำหรับการใช้งานฐานข้อมูล
async def get_db():
    async with async_session() as session: # เปิด session
        yield session   # ส่ง session ออกไปให้ router/controller ใช้งาน
        # หลังจาก yield ออกจากฟังก์ชันแล้ว session จะถูกปิดอัตโนมัติ
