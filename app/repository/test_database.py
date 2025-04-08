# app\repository\test_database.py
import asyncio
from app.repository.database import engine, async_session
from sqlalchemy import text

async def test_database_connection():
    print("Testing database connection...")
    
    try:
        # 1. ทดสอบ engine connection
        print("\n1. Testing engine connection:")
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"Basic query result: {row.test}")
        
        # 2. ทดสอบ session
        print("\n2. Testing session:")
        async with async_session() as session:
            # ทดสอบ query databases
            result = await session.execute(text("SHOW DATABASES"))
            databases = result.fetchall()
            print("\nAvailable databases:")
            for db in databases:
                print(f"- {db[0]}")
            
            # ทดสอบ query tables
            result = await session.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print("\nAvailable tables:")
            for table in tables:
                print(f"- {table[0]}")
                
                # ทดสอบดู structure ของแต่ละตาราง
                result = await session.execute(
                    text(f"DESCRIBE {table[0]}")
                )
                columns = result.fetchall()
                print(f"\nStructure of {table[0]}:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
                    
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise e
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_database_connection())