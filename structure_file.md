ตัวอย่างโครงสร้าง

```
.
├── app/  # โฟลเดอร์หลักของแอปพลิเคชัน 
│   ├── __init__.py   
│   ├── main.py       # เริ่มต้นแอปพลิเคชัน FastAPI
│   ├── dependencies.py # กำหนด dependencies ที่ใช้โดย routers
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tablesRouters.py  # API สำหรับตาราง  
│   │   ├── jobRouters.py  # API สำหรับงาน  
│   │   └── locationRouters.py  # API สำหรับที่ตั้งs
│   ├── controller/
│   │   ├── __init__.py  
│   │   ├── tablesController.py 
│   │   ├── jobController.py  
│   │   └── locationController.py  
│   ├── repository/
│   │   ├── __init__.py
│   │   └── database.py  # การเชื่อมต่อฐานข้อมูล
│   └── utils/
│       ├── __init__.py
│       ├── skill_mapping/
│       └── scraping/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_items.py  # การทดสอบสำหรับโมดูล items
│   └── test_users.py  # การทดสอบสำหรับโมดูล users
├── requirements.txt
├── .gitignore
└── README.md
```

