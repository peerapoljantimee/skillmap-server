# app\controller\tablesController.py

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import text


async def fetch_tables(db: AsyncSession):
    try:
        result = await db.execute(text("SHOW TABLES"))
        tables = result.fetchall()

        tables_list = []
        for table in tables:
            table_name = table[0]
            tables_list.append(f"- {table_name}")

            # ทดสอบดู structure ของแต่ละตาราง
            result = await db.execute(text(f"DESCRIBE {table_name}"))
            columns = result.fetchall()

            columns_list = []
            for col in columns:
                columns_list.append(f"  - {col[0]}: {col[1]}")

            tables_list.append({"table_name": table_name, "columns": columns_list})
            print(tables_list)
            return {"tables": tables_list}
    except Exception as e:
        print(f"\nError: {str(e)}")
        return {"status": "error", "message": str(e)}
