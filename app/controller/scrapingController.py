# app\controller\scrapingController.py

import json
import re
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.scraping.fetch_jobs_card import fetch_jobs_card_utils
from utils.scraping.fetch_jobs_details import fetch_job_details_utils
from utils.simplified.transform import transform_job_data_utils

# async def fetch_jobs_card_by_classification(
#     classification_id: int, subcategory_id: int, db: AsyncSession
# ):
#     # async def fetch_jobs_card(request: dict, db: AsyncSession):
#     try:
#         # ค้นหา job_id ที่ตรงกับ sub_category_id
#         stmt = text(
#             "SELECT job_id FROM classification WHERE sub_category_id = :sub_category_id"  
#         )
#         stmt = stmt.bindparams(sub_category_id=subcategory_id)
#         result = await db.execute(stmt)

#         classification_data = result.mappings().all()

#         # ดึง job_id จาก classification_data
#         classified_job_ids = {job["job_id"] for job in classification_data}

#         _, fetch_jobs_card = fetch_jobs_card_utils(classification_id, subcategory_id)

#         # กรองข้อมูลที่ไม่ซ้ำ
#         filtered_jobs_card = [
#             job
#             for job in fetch_jobs_card["data"]
#             if int(job["id"]) not in classified_job_ids
#         ]
#         print(f"จำนวนงานที่ไม่ซ้ำ: {len(filtered_jobs_card)}")
#         return {"data": filtered_jobs_card}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}


async def fetch_jobs_card_by_classification(
    classification_id: int, subcategory_id: int, db: AsyncSession
):
    # async def fetch_jobs_card(request: dict, db: AsyncSession):
    try:
        # คำสั่ง SQL ที่ใช้ INNER JOIN และกรองตามเงื่อนไขที่กำหนด
        stmt = text("""
            SELECT 
                js.job_id, 
                js.source_type, 
                js.scraped_from, 
                c.main_category_id, 
                c.sub_category_id
            FROM employment_analytics_db.jobs_source js
            INNER JOIN employment_analytics_db.classification c 
            ON js.job_id = c.job_id
            WHERE js.source_type = 'scraping' 
              AND js.scraped_from = 'jobsdb' 
              AND c.main_category_id = 6281 
              AND c.sub_category_id = :sub_category_id;
        """)
        stmt = stmt.bindparams(sub_category_id=subcategory_id)
        result = await db.execute(stmt)

        classification_data = result.mappings().all()

        # ดึง job_id จาก classification_data
        classified_job_ids = {job["job_id"] for job in classification_data}

        _, fetch_jobs_card = fetch_jobs_card_utils(classification_id, subcategory_id)

        # กรองข้อมูลที่ไม่ซ้ำ
        filtered_jobs_card = [
            job
            for job in fetch_jobs_card["data"]
            if int(job["id"]) not in classified_job_ids
        ]
        print(f"จำนวนงานที่ไม่ซ้ำ: {len(filtered_jobs_card)}")
        return {"data": filtered_jobs_card}

    except Exception as e:
        return {"status": "error", "message": str(e)}

async def fetch_jobs_details(jobs_card: list):
    try:
        jobs_details = []
        for job in jobs_card:

            job_id = job["id"]
            job_details = fetch_job_details_utils(job_id)
            if job_details:
                jobs_details.append(job_details["data"])

        # with open("jobDetails_data.json", "w") as file:
        #     json.dump({"data": jobs_details}, file, indent=4)

        return {'data': jobs_details}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    

async def scraping_jobs_by_classification(classification_id: int, subcategory_id: int, db: AsyncSession):
    try:
        filtered_jobs_card = await fetch_jobs_card_by_classification(classification_id, subcategory_id, db)
        filtered_jobs_card = filtered_jobs_card['data']
 
        jobs_details = await fetch_jobs_details(filtered_jobs_card)
        
        return {"data": jobs_details['data']}

   
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

async def insert_jobpostings(request: dict, db: AsyncSession):
    try:
        
        with open("request_jobpostings.json", "w", encoding="utf-8") as file:
            json.dump(request, file, ensure_ascii=False, indent=4)
        
        # ดูผลลัพธ์ที่ได้  
        jobs = request.get('jobs')
        print("insert_jobpostings len", len(jobs))
        print("insert_jobpostings type", type(jobs))
        
        transform_job = transform_job_data_utils(jobs)
        print("transformed_data len", len(transform_job))
        print("transformed_data type", type(transform_job))
        
        # ดูผลลัพธ์ที่ได้หลังจากแปลงข้อมูล
        with open("transform_job_data.json", "w", encoding="utf-8") as file:
            json.dump(transform_job, file, ensure_ascii=False, indent=4)
        
        # เริ่มกระบวนการบันทึกข้อมูลลงฐานข้อมูล
        successful_jobs = []
        failed_jobs = []
        
        for job in transform_job:
            try:
                job_id = int(job["jobId"])
                company_id = int(job["company"]["id"])
                
                # 1. บันทึกข้อมูลบริษัท (company) หากยังไม่มีในฐานข้อมูล
                company_stmt = text("""
                    INSERT INTO company (
                        company_id, name, short_name, industry, verified,
                        company_search_url, registration_date, company_size
                    )
                    VALUES (
                        :company_id, :name, :short_name, :industry, :verified,
                        :company_search_url, 
                        STR_TO_DATE(:registration_date, '%Y-%m-%dT%H:%i:%s.%fZ'),
                        :company_size
                    ) AS new_data
                    ON DUPLICATE KEY UPDATE
                        name = new_data.name,
                        short_name = new_data.short_name,
                        industry = new_data.industry,
                        verified = new_data.verified,
                        company_search_url = new_data.company_search_url,
                        registration_date = STR_TO_DATE(:registration_date, '%Y-%m-%dT%H:%i:%s.%fZ'),
                        company_size = new_data.company_size
                """)

                
                await db.execute(company_stmt, {
                    "company_id": company_id,
                    "name": job["company"]["name"],
                    "short_name": job["company"]["shortName"],
                    "industry": job["company"]["industry"],
                    "verified": job["company"]["isVerified"],
                    "company_search_url": job["companySearchUrl"] if "companySearchUrl" in job else None,
                    "registration_date": job["company"]["registrationDate"],
                    "company_size": job["company"]["max_size"]
                })
                
                # 2. บันทึกข้อมูลงาน (jobs)
                jobs_stmt = text("""
                    INSERT INTO jobs (
                        job_id, company_id, content, share_link
                    )
                    VALUES (
                        :job_id, :company_id, :content, :share_link
                    ) AS new_data
                    ON DUPLICATE KEY UPDATE
                        company_id = new_data.company_id,
                        content = new_data.content,
                        share_link = new_data.share_link
                """)
                
                await db.execute(jobs_stmt, {
                    "job_id": job_id,
                    "company_id": company_id,
                    "content": job["content"],
                    "share_link": job["shareLink"]
                })
                
                # 3. บันทึกข้อมูลพื้นฐาน (basicinfo)
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
                    "title": job["basicInfo"]["title"],
                    "type": job["basicInfo"]["type"],
                    "status": job["basicInfo"]["status"],
                    "posted_date": job["basicInfo"]["postedDate"],
                    "expiry_date": job["basicInfo"]["expiryDate"]
                })
                
                # 4. บันทึกข้อมูลหมวดหมู่ (classification)
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
                    "main_category_id": int(job["classification"]["mainCategory"]["id"]),
                    "sub_category_id": int(job["classification"]["subCategory"]["id"])
                })
                
                # 5. บันทึกข้อมูลสถานะทักษะ (jobs_skill_status)
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
                
                # 6. บันทึกข้อมูลแหล่งที่มา (jobs_source)
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
                    "source_type": "scraping",
                    "scraped_from": "jobsdb"
                })
                
                # 7. บันทึกข้อมูลสถานที่ (location)
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
                    "area": job["location"]["area"],
                    "city": job["location"]["city"],
                    "country": job["location"]["country"]
                })
                
                # 8. บันทึกข้อมูลเงินเดือน (salary)
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
                    "min_salary": job["salary"]["min_salary"],
                    "max_salary": job["salary"]["max_salary"],
                    "currency": job["salary"]["currency"],
                    "period": job["salary"]["period"],
                    "has_salary_info": job["salary"]["has_salary_info"]
                })
                
                # Commit transaction for this job
                await db.commit()
                
                successful_jobs.append(job_id)
                
            except Exception as e:
                # Roll back in case of error
                await db.rollback()
                print(f"Error processing job {job['jobId']}: {str(e)}")
                failed_jobs.append({
                    "job_id": job["jobId"],
                    "error": str(e)
                })
        
        return {
            "status": "success",
            "total_jobs": len(transform_job),
            "successful_jobs": len(successful_jobs),
            "failed_jobs": len(failed_jobs),
            "failed_jobs_details": failed_jobs if failed_jobs else None
        }
        
    except Exception as e:
        await db.rollback()
        print(f"Error in insert_jobpostings: {str(e)}")
        return {"status": "error", "message": str(e)}






