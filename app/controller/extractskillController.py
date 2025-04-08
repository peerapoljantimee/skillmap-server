# app/controller/extractskillController.py

import json
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.skill_extractors.skill_extractors import skill_extractors_utils

async def extractskills(request: dict):
    try:
        jobs_data = request.get("data")
        
        data = skill_extractors_utils(jobs_data)
        result = {
            "status": "success",
            "data": data
        }
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
  
async def insert_skills(request: dict, db: AsyncSession): 
    try:
        jobs_data = request.get("data")
        job_success = []
        job_error = []
        for job in jobs_data:
            try:
                job_id = job.get("job_id")
                if job_id is None:
                    job_error.append({"job_id": "unknown", "error": "Missing job_id in data"})
                    continue
                
                print(f"Processing job_id: {job_id}")
                
                # ตรวจสอบ extracted_skills
                extracted_skills = job.get("extracted_skills")
                if extracted_skills is None:
                    print(f"Warning: extracted_skills is None for job_id: {job_id}")
                    extracted_skills = {}
                hard_skills = extracted_skills.get("hard_skills", []) # type list
                soft_skills = extracted_skills.get("soft_skills", []) # type list
                
                # # ตรวจสอบว่าค่าเป็น None หรือไม่ หรือไม่ใช่ list และแปลงเป็น list ว่างในกรณีที่เป็น None หรือไม่ใช่ list
                if hard_skills is None or not isinstance(hard_skills, list):
                    hard_skills = []
                if soft_skills is None or not isinstance(soft_skills, list):
                    soft_skills = []
                
                # ต้องแยกการ insert เป็นรายการทักษะ เพราะเป็น list
                # 1. บันทึกข้อมูล hard_skills ทีละทักษะ
                for skill in hard_skills:
                    stmt = text("""
                        INSERT INTO jobs_skill (
                            job_id, skill_name, skill_type
                        )
                        VALUES (
                            :job_id, :skill_name, :skill_type
                        ) AS new_data
                        ON DUPLICATE KEY UPDATE
                            skill_name = new_data.skill_name,
                            skill_type = new_data.skill_type
                    """)

                    await db.execute(stmt, {
                        "job_id": job_id,
                        "skill_name": skill,
                        "skill_type": "hard_skill"
                    })
                
                # 2. บันทึกข้อมูล soft_skills ทีละทักษะ
                for skill in soft_skills:
                    stmt = text("""
                        INSERT INTO jobs_skill (
                            job_id, skill_name, skill_type
                        )
                        VALUES (
                            :job_id, :skill_name, :skill_type
                        ) AS new_data
                        ON DUPLICATE KEY UPDATE
                            skill_name = new_data.skill_name,
                            skill_type = new_data.skill_type
                    """)
                    await db.execute(stmt, {
                        "job_id": job_id,
                        "skill_name": skill,
                        "skill_type": "soft_skill"
                    })
                
                # 3. อัปเดตสถานะว่ามีการดึงทักษะแล้ว
                stmt = text("""
                    INSERT INTO jobs_skill_status (job_id, has_extracted_skill)
                    VALUES (:job_id, 1)
                    AS new_data
                    ON DUPLICATE KEY UPDATE
                        has_extracted_skill = new_data.has_extracted_skill
                """)
                await db.execute(stmt, {
                    "job_id": job_id,
                }) 
                
                # ถ้าทุกอย่างสำเร็จ commit transaction
                await db.commit()
                print(f"Successfully committed changes for job_id: {job_id}")
                
                job_success.append(job_id)  
            
            except Exception as err:
                await db.rollback()  # ทำ rollback เมื่อเกิดข้อผิดพลาด
                error_message = str(err)
                print(f"Error processing job_id {job_id}: {error_message}")
                job_error.append({"job_id": job_id, "error": error_message})
                continue
 
        return {
            "status": "success",
            "data": job_success,
            "error_job_ids": job_error,
        }
    except Exception as e:
        await db.rollback()  # ทำ rollback เมื่อเกิดข้อผิดพลาด
        error_message = str(e)
        print("### error", error_message)
        return {"status": "error", "message": error_message}