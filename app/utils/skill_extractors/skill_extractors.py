import os
import json
import time
import datetime
from dotenv import load_dotenv
from utils.skill_extractors.anthropic_client import client
from utils.skill_extractors.create_requests import create_requests

def skill_extractors_utils(jobs_data: list):
   # แสดงผลลัพธ์
   print(f"📌 Number of job postings: {len(jobs_data)}")

   # กำหนดโฟลเดอร์สำหรับเก็บผลลัพธ์
   timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
   results_dir = os.path.join("results", timestamp)
   requests_dir = os.path.join(results_dir, "requests")
   processed_jobs_dir = os.path.join(results_dir, "processed_jobs")

   os.makedirs(requests_dir, exist_ok=True)
   os.makedirs(processed_jobs_dir, exist_ok=True)

   # สร้าง Requests และบันทึกลงไฟล์
   requests_config = create_requests(jobs_data)
   requests_filepath = os.path.join(requests_dir, "requests.json")

   with open(requests_filepath, 'w', encoding='utf-8') as f:
      json.dump(requests_config, f, ensure_ascii=False, indent=2)

   print(f"📄 Requests saved to: {requests_filepath}")
   
   # return requests_config

   # 📡 ส่ง requests ไปยัง API
   message_batch = client.messages.batches.create(requests=requests_config)
   message_batch_id = message_batch.id
   print(f"📤 Sent requests to API with Batch ID: {message_batch_id}")

   # ตรวจสอบสถานะของ Message Batch
   while True:
      message_batch = client.messages.batches.retrieve(message_batch_id)
      if message_batch.processing_status == "ended":
         break
      print(f"⏳ Batch {message_batch_id} is still processing...")
      time.sleep(5)  # รอ 5 วินาทีก่อนตรวจสอบสถานะอีกครั้ง

   print("✅ Processing completed!")

   # ดึงผลลัพธ์ของ Batch
   retriever_results = list(client.messages.batches.results(message_batch_id))

   # แปลงผลลัพธ์เป็น JSON และบันทึกลงไฟล์
   processed_jobs = []
   for result in retriever_results:
      job_id = int(result.custom_id)
      try:
         extracted_skills = json.loads(result.result.message.content[0].text.lower())
      except json.JSONDecodeError:
         extracted_skills = {"error": "Invalid JSON format"}

      # ดึงข้อมูลโทเค็นที่ใช้ไป
      input_tokens = result.result.message.usage.input_tokens
      output_tokens = result.result.message.usage.output_tokens

      processed_jobs.append({
         "job_id": job_id,
         "extracted_skills": extracted_skills,
         "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens}
      })

   # บันทึกผลลัพธ์ลงไฟล์
   processed_jobs_filepath = os.path.join(processed_jobs_dir, "processed_jobs.json")
   with open(processed_jobs_filepath, 'w', encoding='utf-8') as f:
      json.dump(processed_jobs, f, ensure_ascii=False, indent=2)

   print(f"✅ Processed jobs saved to: {processed_jobs_filepath}")
   
   return processed_jobs
  