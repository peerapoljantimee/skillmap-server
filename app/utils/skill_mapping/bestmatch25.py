import json
from rank_bm25 import BM25Okapi

def tokenize_skills(skills_list):
    # แยกคำและลบคำซ้ำ
    all_tokens = []
    for skill in skills_list:
        # แยกคำโดยใช้ช่องว่าง
        tokens = skill.split()
        all_tokens.extend(tokens)

    # ลบคำซ้ำและเรียงลำดับ
    unique_tokens = sorted(list(set(all_tokens)))
    return unique_tokens


def bm25_retrieval_utils(query , jobs_data_dict, top_n):
   jobs_data = jobs_data_dict

   for job in jobs_data:
      job['tokenized_skills'] = tokenize_skills(job['combine_skill_corpus'])
   
   bm25 = BM25Okapi([job['tokenized_skills'] for job in jobs_data])
    
   query_tokens = tokenize_skills(query)
   scores = bm25.get_scores(query_tokens)

   # เพิ่มคะแนน BM25 ลงใน jobs_data
   for i, score in enumerate(scores):
      jobs_data[i]['bm25_score'] = score

   # จัดอันดับตามคะแนน BM25 และเลือก 10 อันดับแรก
   sorted_jobs = sorted(jobs_data, key=lambda x: x['bm25_score'], reverse=True)[:top_n]


   # 🔹 ส่งผลลัพธ์เป็น JSON
   results = [
      {
         "bm25_score": round(job['bm25_score'], 2),
         "job_id": job.get("job_id"),
         "company_name": job.get("company_name"),
         "area": job.get("area"),
         "city": job.get("city"),
         "country": job.get("country"),
         "title": job.get("title"),
         "type": job.get("type"),
         "main_category_name": job.get("main_category_name"),
         "sub_category_name": job.get("sub_category_name"),
         "min_salary": job.get("min_salary"),
         "max_salary": job.get("max_salary"),
         "currency": job.get("currency"),
         "period": job.get("period"),
         "content": job.get("content"),
         "share_link": job.get("share_link"),
         "soft_skills": job.get("soft_skills"),
         "hard_skills": job.get("hard_skills"),
         "status": job.get("status"),
      }
      for job in sorted_jobs
   ]

   return results
