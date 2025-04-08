# app\controller\mappingController.py

import json
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.skill_mapping.bestmatch25 import bm25_retrieval_utils


async def fetch_hard_skills(db: AsyncSession):
    try:
        stmt = text("""
            SELECT DISTINCT skill_name
            FROM jobs_skill_status js_status
            INNER JOIN jobs_skill js ON js_status.job_id = js.job_id
            WHERE has_extracted_skill = 1 
            AND skill_type = 'hard_skill';
            """)
        
        result = await db.execute(stmt)

        hard_skills_list = result.mappings().all()

        return {
            "status": "success",
            "skills_type": "hard_skills",   
            "skills": hard_skills_list
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}


async def fetch_soft_skills(db: AsyncSession):
    try:
        stmt = text("""
            SELECT DISTINCT skill_name
            FROM jobs_skill_status js_status
            INNER JOIN jobs_skill js ON js_status.job_id = js.job_id
            WHERE has_extracted_skill = 1 
            AND skill_type = 'soft_skill';
            """)
        
        result = await db.execute(stmt)

        soft_skills_list = result.mappings().all()

        return {
            "status": "success",
            "skills_type": "soft_skills",   
            "skills": soft_skills_list
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    
async def retrieval(request : dict, db: AsyncSession):
    try:        
        stmt = text("""
            SELECT
            j.job_id,
            comp.name AS company_name,
            loc.area,
            loc.city,
            loc.country,
            job_info.title,
            job_info.type,
            main_cat.name AS main_category_name,
            sub_cat.name AS sub_category_name,
            sal.min_salary,
            sal.max_salary,
            sal.currency,
            sal.period,
            j.content,
            j.share_link,
            skills.combine_skill_corpus,
            skills.soft_skills,
            skills.hard_skills,
            job_info.status

            FROM jobs j
            INNER JOIN company comp ON j.company_id = comp.company_id
            INNER JOIN location loc ON j.job_id = loc.job_id
            INNER JOIN basicinfo job_info ON j.job_id = job_info.job_id
            INNER JOIN salary sal ON j.job_id = sal.job_id
            INNER JOIN classification class ON j.job_id = class.job_id
            INNER JOIN main_category main_cat ON class.main_category_id = main_cat.main_category_id
            INNER JOIN sub_category sub_cat ON class.sub_category_id = sub_cat.sub_category_id
            INNER JOIN job_skills_view skills ON j.job_id = skills.job_id
            INNER JOIN jobs_skill_status js_status ON j.job_id = js_status.job_id
            WHERE job_info.status = "Active"
            AND js_status.has_extracted_skill = 1 
            AND sub_cat.sub_category_id = :sub_category_id

            GROUP BY
            j.job_id,
            comp.name,
            loc.area,
            loc.city,
            loc.country,
            job_info.title,
            job_info.type,
            main_cat.name,
            sub_cat.name,
            sal.min_salary,
            sal.max_salary,
            sal.currency,
            sal.period,
            j.content,
            j.share_link,
            skills.combine_skill_corpus,
            skills.soft_skills,
            skills.hard_skills,
            job_info.status
            """)
        
        # request = {'sub_category_id': '6283', 'hard_skills': ['business administration', 'business performance analysis'], 'soft_skills': []}
        subcategory_id = request.get("sub_category_id")
        
        hard_skills = request.get("hard_skills")
        soft_skills = request.get("soft_skills")
        query = hard_skills + soft_skills
     
        
        # jobs = await db.execute(stmt)
        stmt = stmt.bindparams(sub_category_id=subcategory_id)
        result = await db.execute(stmt)
        jobs_data = result.mappings().all()
         
        # แปลง RowMapping เป็น dictionaries
        jobs_data_dict = [
            {
                "job_id": row.get("job_id"),
                "company_name": row.get("company_name"),
                "area": row.get("area"),
                "city": row.get("city"),
                "country": row.get("country"),
                "title": row.get("title"),
                "type": row.get("type"),
                "main_category_name": row.get("main_category_name"),
                "sub_category_name": row.get("sub_category_name"),
                "min_salary": row.get("min_salary"),
                "max_salary": row.get("max_salary"),
                "currency": row.get("currency"),
                "period": row.get("period"),
                "content": row.get("content"),
                "share_link": row.get("share_link"),
                "combine_skill_corpus": json.loads(row.get("combine_skill_corpus")) if row.get("combine_skill_corpus") else [],
                "soft_skills": json.loads(row.get("soft_skills")) if row.get("soft_skills") else [],
                "hard_skills": json.loads(row.get("hard_skills")) if row.get("hard_skills") else [],
                "status": row.get("status"),
            }
            for row in jobs_data
        ]     
        
        top_n = 10
        jobs_retrieval = bm25_retrieval_utils(query, jobs_data_dict, top_n)
  
         
        return {
            "status": "success",
            "top_n": top_n,
            "jobs": jobs_retrieval,   
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}