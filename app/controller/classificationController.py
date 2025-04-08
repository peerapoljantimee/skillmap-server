# app\controller\classificationController.py app.controller.classificationController

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_classification_by_subcategory(db: AsyncSession, sub_category_id):
    try:
        stmt = text(
            "SELECT * FROM classification WHERE sub_category_id = :sub_category_id"
        )
        stmt = stmt.bindparams(sub_category_id=sub_category_id)
        result = await db.execute(stmt)

        classification_list = result.mappings().all()

        return {"data": classification_list}

    except Exception as e:
        return {"status": "error", "message": str(e)}


async def fetch_subcategory(db: AsyncSession):
    try:
        stmt = text("SELECT * FROM sub_category")
        result = await db.execute(stmt)

        subcategory_list = result.mappings().all()

        return {"data": subcategory_list}

    except Exception as e:
        return {"status": "error", "message": str(e)}
