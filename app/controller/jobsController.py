# app/controller/jobsController.py

import json
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

async def fetch_jobs(db: AsyncSession):
    try:
        # เขียนคำสั่ง SQL แบบ raw
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
            skills.soft_skills,
            skills.hard_skills,
            js_source.source_type,
            js_source.scraped_from,
            js_status.has_extracted_skill,
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
            INNER JOIN jobs_source js_source ON j.job_id = js_source.job_id

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
        skills.soft_skills,
        skills.hard_skills,
        js_source.source_type,
        js_source.scraped_from,
        js_status.has_extracted_skill,
        job_info.status           
        """)
        result = await db.execute(stmt)

        jobs_list = result.mappings().all()
        # print(jobs_list)

        # คืนค่าผลลัพธ์
        return {
            "status": "success",
            'data': jobs_list 
        }
         
    except Exception as e:
        return {"status": "error", "message": str(e)} 
    
async def fetch_jobs_unextracted_skills(db: AsyncSession):
    try:
        # เขียนคำสั่ง SQL แบบ raw
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
            skills.soft_skills,
            skills.hard_skills,
            js_source.source_type,
            js_source.scraped_from,
            js_status.has_extracted_skill,
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
            INNER JOIN jobs_source js_source ON j.job_id = js_source.job_id
        WHERE has_extracted_skill = 0

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
        skills.soft_skills,
        skills.hard_skills,
        js_source.source_type,
        js_source.scraped_from,
        js_status.has_extracted_skill,
        job_info.status           
        """)
        result = await db.execute(stmt)

        jobs_list = result.mappings().all()
        # print(jobs_list)

        # คืนค่าผลลัพธ์
        return {
            "status": "success",
            'data': jobs_list 
        }
         
    except Exception as e:
        return {"status": "error", "message": str(e)} 
    
    


async def insert_jobpostings(request: dict, db: AsyncSession):
    try:
        print("request")
        print(request)
        company_id = int(request["company"]["id"])

        # 1. บันทึกข้อมูลงาน (jobs)
        jobs_stmt = text("""
            INSERT INTO jobs (
                company_id, content, share_link
            )
            VALUES (
                :company_id, :content, :share_link
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                company_id = new_data.company_id,
                content = new_data.content,
                share_link = new_data.share_link
        """)

        await db.execute(jobs_stmt, {
            "company_id": company_id,
            "content": request["content"],
            "share_link": request["shareLink"]
        })

        # ดึง job_id ที่เพิ่งสร้าง
        last_id_stmt = text("SELECT LAST_INSERT_ID() AS job_id")
        result = await db.execute(last_id_stmt)
        job_id_row = result.fetchone()  # ไม่ต้องใช้ await เพราะ fetchone() ไม่ใช่ coroutine
        job_id = job_id_row[0] if job_id_row else None
        print("job_id", job_id)
        
        # 2. บันทึกข้อมูลพื้นฐาน (basicinfo)
        basicinfo_stmt = text("""
            INSERT INTO basicinfo (
                job_id, title, type, status, posted_date, expiry_date
            )
            VALUES (
                :job_id, :title, :type, :status, 
                STR_TO_DATE(:posted_date, '%Y-%m-%dT%H:%i:%s.%fZ'),
                STR_TO_DATE(:expiry_date, '%Y-%m-%dT%H:%i:%s.%fZ')
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                title = new_data.title,
                type = new_data.type,
                status = new_data.status,
                posted_date = STR_TO_DATE(:posted_date, '%Y-%m-%dT%H:%i:%s.%fZ'),
                expiry_date = STR_TO_DATE(:expiry_date, '%Y-%m-%dT%H:%i:%s.%fZ')
        """)
                
        await db.execute(basicinfo_stmt, {
            "job_id": job_id,
            "title": request["basicInfo"]["title"],
            "type": request["basicInfo"]["type"],
            "status": request["basicInfo"]["status"],
            "posted_date": request["basicInfo"]["postedDate"],
            "expiry_date": request["basicInfo"]["expiryDate"]
        })
        
        # 3. บันทึกข้อมูลหมวดหมู่ (classification)
        classification_stmt = text("""
            INSERT INTO classification (
                job_id, main_category_id, sub_category_id
            )
            VALUES (
                :job_id, :main_category_id, :sub_category_id
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                main_category_id = new_data.main_category_id,
                sub_category_id = new_data.sub_category_id
        """)


        await db.execute(classification_stmt, {
            "job_id": job_id,
            "main_category_id": int(request["classification"]["mainCategories"]["id"]),
            "sub_category_id": int(request["classification"]["subCategories"]["id"])
        })
        
        # 4. บันทึกข้อมูลสถานะทักษะ (jobs_skill_status)
        skill_status_stmt = text("""
            INSERT INTO jobs_skill_status (
                job_id, has_extracted_skill
            )
            VALUES (
                :job_id, :has_extracted_skill
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                has_extracted_skill = new_data.has_extracted_skill
        """)

        await db.execute(skill_status_stmt, {
            "job_id": job_id,
            "has_extracted_skill": 0  # เริ่มต้น false (0)
        })
        
        # 5. บันทึกข้อมูลแหล่งที่มา (jobs_source)
        source_stmt = text("""
            INSERT INTO jobs_source (
                job_id, source_type, scraped_from
            )
            VALUES (
                :job_id, :source_type, :scraped_from
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                source_type = new_data.source_type,
                scraped_from = new_data.scraped_from
        """)

        await db.execute(source_stmt, {
            "job_id": job_id,
            "source_type": "manual",
            "scraped_from": None
        })
        
        # 6. บันทึกข้อมูลสถานที่ (location)
        location_stmt = text("""
            INSERT INTO location (
                job_id, area, city, country
            )
            VALUES (
                :job_id, :area, :city, :country
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                area = new_data.area,
                city = new_data.city,
                country = new_data.country
        """)

        await db.execute(location_stmt, {
            "job_id": job_id,
            "area": request["location"]["area"],
            "city": request["location"]["city"],
            "country": request["location"]["country"]
        })
        
        # 7. บันทึกข้อมูลเงินเดือน (salary)
        salary_stmt = text("""
            INSERT INTO salary (
                job_id, min_salary, max_salary, currency, period, has_salary_info
            )
            VALUES (
                :job_id, :min_salary, :max_salary, :currency, :period, :has_salary_info
            ) AS new_data
            ON DUPLICATE KEY UPDATE
                min_salary = new_data.min_salary,
                max_salary = new_data.max_salary,
                currency = new_data.currency,
                period = new_data.period,
                has_salary_info = new_data.has_salary_info
        """)

        await db.execute(salary_stmt, {
            "job_id": job_id,
            "min_salary": request["salary"]["min_salary"],
            "max_salary": request["salary"]["max_salary"],
            "currency": request["salary"]["currency"],
            "period": request["salary"]["period"],
            "has_salary_info": request["salary"]["has_salary_info"]
        })
                
        # เพิ่ม job_id เข้าไปใน response
        response_data = request.copy()
        response_data["job_id"] = job_id
        
        print("### response_data")
        print(response_data)
        
        await db.commit()
        
        return {
                "status": "success",
                "data": response_data
        }
    except Exception as e:
        await db.rollback() 
        return {"status": "error", "message": str(e)}
        
