# utils.image_to_text.gemini.gemini_extract

import json
from google.generativeai import GenerativeModel, GenerationConfig, configure
import os
import base64
import io
from PIL import Image
import json
from utils.image_to_text.gemini.prompt import *
from dotenv import load_dotenv

async def process_with_gemini_util(image_content):
    print("###gemini_extract")
    try:
        # โหลด environment variables
        load_dotenv()
        
        # ตั้งค่า API key
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        configure(api_key=GEMINI_API_KEY)

        # เลือกโมเดล Gemini สำหรับงาน Vision
        model = GenerativeModel('gemini-1.5-flash')
        
        # แปลงข้อมูลไบนารีเป็นรูปภาพ PIL
        image = Image.open(io.BytesIO(image_content))
        
        # สร้างคำขอไปยัง Gemini
        response = model.generate_content([
                PROMPT_ENGINEERING,
                image
            ],
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                temperature=0
            )
        )
        
        response_str = response.text
        response_json = json.loads(response_str)
        # ส่งผลลัพธ์กลับ
        print(response_json)
        print(type(response_json))
        return response_json
        
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        raise Exception(f"ไม่สามารถประมวลผลรูปภาพด้วย Gemini: {str(e)}")