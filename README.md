# SkillMap Server: ระบบวิเคราะห์แนวโน้มอาชีพและจับคู่ทักษะ

![Python](https://img.shields.io/badge/Python-3.10.7-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0.41-4479A1?style=flat&logo=mysql&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic_Claude-0B0D12?style=flat&logo=anthropic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E44AD?style=flat&logo=google&logoColor=white)
![Google Vision](https://img.shields.io/badge/Google_Vision-4285F4?style=flat&logo=google&logoColor=white)
![Looker Studio](https://img.shields.io/badge/Looker_Studio-0078D4?style=flat&logo=google&logoColor=white)
![JobsDB](https://img.shields.io/badge/JobsDB-db0473?style=flat&logo=job&logoColor=white)![Web Scraping](https://img.shields.io/badge/Web_Scraping-47A248?style=flat)
![Image to Text](https://img.shields.io/badge/Image_to_Text-FF6F00?style=flat&logo=image&logoColor=white)


## เกี่ยวกับโปรเจค

SkillMap Server เป็นส่วน Backend ของระบบ [SkillMap Client](https://github.com/peerapoljantimee/skillmap-client) ที่พัฒนาขึ้นเพื่อสร้างแพลตฟอร์มอัจฉริยะสำหรับการวิเคราะห์ตลาดแรงงาน พร้อมระบบจับคู่ทักษะที่เชื่อมโยงความสามารถของผู้ใช้กับตำแหน่งงานที่เหมาะสม เพื่อเพิ่มโอกาสในการพัฒนาอาชีพด้านเทคโนโลยีสารสนเทศและการสื่อสารอย่างตรงจุด

## คุณสมบัติหลัก

- แสดงแนวโน้มตลาดงานในปัจจุบัน
- จับคู่ทักษะกับหมวดหมู่และตำแหน่งงานที่เหมาะสม
- รวบรวมข้อมูล
- ดึงข้อมูลตำแหน่งงานจากเว็บไซต์หางานโดยอัตโนมัติ
- วิเคราะห์และสกัดทักษะจากประกาศรับสมัครงานด้วย AI
- แปลงภาพโปสเตอร์ประกาศรับสมัครงานเป็นข้อความเพื่อช่วยในการรวบรวมข้อมูลตำแหน่งงานด้วย AI

## ความต้องการของระบบ

- Python 3.10.7 หรือสูงกว่า
- MySQL Server 8.0.41
- pip (Package Installer for Python)
- เชื่อมต่ออินเทอร์เน็ตสำหรับการใช้งาน API ภายนอก

## การติดตั้ง

### ขั้นตอนที่ 1: โคลนโปรเจค

```bash
git clone https://github.com/peerapoljantimee/skillmap-server.git
cd skillmap-server
```

### ขั้นตอนที่ 2: สร้างและเปิดใช้งาน Virtual Environment

```bash
python -m venv env
# สำหรับ Windows
env\Scripts\activate
# สำหรับ Linux/Mac
# source env/bin/activate
```

### ขั้นตอนที่ 3: ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### ขั้นตอนที่ 4: ติดตั้ง MySQL Server

1. ดาวน์โหลดและติดตั้ง [MySQL Community Server 8.0.41](https://dev.mysql.com/downloads/mysql/)
2. ติดตั้ง [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) (แนะนำสำหรับการจัดการฐานข้อมูล)

### ขั้นตอนที่ 5: สร้างฐานข้อมูลโดยใช้ MySQL Workbench

1. เปิด MySQL Workbench และเชื่อมต่อกับ MySQL Server ของคุณ
2. เลือกแท็บ "Administration" ที่ด้านซ้าย
3. ในส่วน "Management" เลือก "Data Import/Restore"
4. เลือก "Import frorm Dump Project Folder" และเรียกดูไปที่โฟลเดอร์ `...\employment_analytics_db_dump\Structure_Only` ในโปรเจค
5. ที่ "Default Schema to be Imported To" เลือก "New" และตั้งชื่อเป็น `employment_analytics_db`
6. คลิก "Start Import" เพื่อสร้างโครงสร้างฐานข้อมูล

## การตั้งค่าสภาพแวดล้อม

สร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจคและเพิ่มข้อมูลต่อไปนี้:

```
# การตั้งค่า MySQL
DB_USER={ชื่อผู้ใช้}
DB_PASS={รหัสผ่าน}
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=employment_analytics_db

# API Keys
ANTHROPIC_API_KEY="เเทน ANTHROPIC API KEY ของคุณ"
GEMINI_API_KEY="เเทน GEMINI API KEY ของคุณ"
OPENAI_API_KEY="เเทน OPENAI API KEY ของคุณ"
GOOGLE_APPLICATION_CREDENTIALS="app\utils\image_to_text\google_openai\{เเทน GOOGLE VISION API KEY ของคุณ}.json"
```

> **หมายเหตุ:** อย่าเผยแพร่ไฟล์ `.env` ที่มีข้อมูลจริงลงใน GitHub หรือระบบควบคุมเวอร์ชันอื่นๆ

## การเริ่มต้นใช้งาน

```bash
# เปิดใช้งาน environment (ถ้ายังไม่ได้เปิดใช้งาน)
env\Scripts\activate

# เริ่มต้นเซิร์ฟเวอร์
python -m app.main
```

เซิร์ฟเวอร์จะทำงานที่ `http://localhost:8000` และคุณสามารถเข้าถึง API Documentation ได้ที่ `http://localhost:8000/docs`

## โครงสร้างโปรเจค

โปรเจคนี้ใช้โครงสร้างแบบ Routes and Controllers เพื่อจัดการ API endpoints และ business logic

```
skillmap-server/
└── app/
    ├── controller/           # จัดการ business logic และคำสั่ง SQL
    ├── repository/           # จัดการการเชื่อมต่อฐานข้อมูล
    ├── routers/              # กำหนด API endpoints
    ├── utils/                # เครื่องมือและฟังก์ชันเสริม
    │   ├── image_to_text/    # แปลงภาพเป็นข้อความด้วยเทคโนโลยี AI
    │   ├── scraping/         # ดึงข้อมูลจากเว็บไซต์หางาน
    │   ├── simplified/       # ประมวลผลและลดความซับซ้อนของข้อมูล
    │   ├── skill_extractors/ # สกัดทักษะจากข้อความด้วยเทคโนโลยี AI
    │   └── skill_mapping/    # จับคู่ทักษะกับหมวดหมู่ที่เกี่ยวข้อง
    ├── dependencies.py       # dependency injection
    └── main.py               # entry point ของแอปพลิเคชัน
```

### การทำงานของส่วนหลัก:

- **Controllers**: จัดการ business logic, ประมวลผลข้อมูล และทำงานกับฐานข้อมูลผ่าน SQL queries
- **Routers**: กำหนด API endpoints และเส้นทางไปยัง controller ที่เหมาะสม
- **Repository**: จัดการการเชื่อมต่อกับฐานข้อมูล
- **Utils**: 
  - `image_to_text`: แปลงภาพโปสเตอร์ประกาศรับสมัครงานเป็นข้อความด้วยเทคโนโลยี AI จาก Gemini และ Google OCR + GPT สำหรับรวบรวมข้อมูลตำแหน่งงาน
  - `scraping`: ดึงข้อมูลตำแหน่งงานจากเว็บไซต์หางาน JobsDB
  - `simplified`: ทำหน้าที่ประมวลผลและลดความซับซ้อนของข้อมูล
  - `skill_extractors`: สกัดทักษะจากรายละเอียดงานด้วยเทคโนโลยี AI จาก Anthropic AI 
  - `skill_mapping`: จับคู่ทักษะกับหมวดหมู่และทำการวิเคราะห์ความเกี่ยวข้อง
