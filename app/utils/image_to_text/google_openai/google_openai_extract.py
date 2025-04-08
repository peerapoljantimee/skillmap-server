# utils.image_to_text.google_openai.google_openai_extract.py

import json
import os
import io
from PIL import Image
import tempfile
from google.cloud import vision
from openai import OpenAI
from dotenv import load_dotenv
from utils.image_to_text.google_openai.prompt import PROMPT_ENGINEERING

async def process_with_google_openai_util(image_content):
    print("###google_openai_extract")
    try:
        # โหลด environment variables
        load_dotenv()
        
        # ตั้งค่า credentials สำหรับ Google Vision API
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # ตั้งค่า OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=openai_api_key)
        
        # สร้างไฟล์ชั่วคราวเพื่อเก็บรูปภาพ
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(image_content)
            temp_file_path = temp_file.name
        
        # OCR ด้วย Google Vision API
        vision_client = vision.ImageAnnotatorClient()
        with open(temp_file_path, "rb") as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        response = vision_client.document_text_detection(image=image)
        
        # ตรวจสอบข้อผิดพลาดจาก Google Vision API
        if response.error.message:
            raise Exception(f"Google Vision API Error: {response.error.message}")
        
        # ดึงข้อความที่ได้จาก OCR
        google_vision_ocr_text = response.full_text_annotation.text.strip()
        print("### OCR Result:")
        print(google_vision_ocr_text)
        
        print('### PROMPT')
        fomatted_prompt = PROMPT_ENGINEERING.format(ocr_text=google_vision_ocr_text)
        print(fomatted_prompt)
    
        # ใช้ OpenAI เพื่อแปลงข้อความเป็นโครงสร้าง JSON
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": fomatted_prompt}],
            max_tokens=2000,
            # response_format="json",
            response_format={"type": "json_object"},
            temperature=0,
            timeout=60,
        )
        
        result_json = response.choices[0].message.content
        print("### OpenAI Result (raw):")
        print(result_json)

        parsed = json.loads(result_json)
        print("### Parsed JSON:")
        print(parsed)
        return parsed
        
    except Exception as e:
        print(f"Google Vision + OpenAI API error: {str(e)}")
        raise Exception(f"ไม่สามารถประมวลผลรูปภาพด้วย Google Vision + OpenAI: {str(e)}")