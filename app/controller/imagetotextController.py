# app\controller\imagetotextController.py

from utils.image_to_text.gemini.gemini_extract import process_with_gemini_util
from utils.image_to_text.google_openai.google_openai_extract import process_with_google_openai_util
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, GenerationConfig, configure

load_dotenv()

async def process_imagetotext(model, files):
   print("###imagetotextController")
   
   try:
      # อ่านเนื้อหาของไฟล์ทั้งหมดที่ได้รับ
      file_contents = []
      file_info = []
      
      for file in files:
         content = await file.read()
         file_info.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
         })
         file_contents.append(content)
         # ต้อง seek กลับไปที่ต้นไฟล์หลังจากอ่าน
         await file.seek(0)
      
      # เรียกใช้งาน API ที่เหมาะสมตามโมเดลที่เลือก
      if model == "gemini":
         # ส่งรูปภาพไปยัง Gemini API
         data = await process_with_gemini_util(file_contents[0])
      elif model == "google_openai":
         # ส่งรูปภาพไปยัง Google Vision และ OpenAI
         data = await process_with_google_openai_util(file_contents[0])
      
      
      result = {
         "status": "success",
         "model": model,
         "file": file_info,
         "data": data
      }
      print(result)
      return result
   
   except Exception as e:
      result = {
         "status": "error",
         "message": str(e)
      }
   return result
     
