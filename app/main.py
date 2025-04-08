# app\main.py

import asyncio
from fastapi import FastAPI
from routers import tablesRouters, jobsRouters, classificationRouters, scrapingRouters, subcategoryRouters ,maincategoryRouters, mappingRouters, companyRouters, basicinfoRouters, locationRouters, salaryRouters, imagetotextRouters, extractskillsRouters
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Employment Analytics API",
    description="API for importing and managing job data",
)

# กำหนดการตั้งค่า CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # กำหนดที่อยู่ที่อนุญาตให้ร้องขอจากที่นี่
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # อนุญาตเฉพาะบางเมธอด ถ้าต้องการ
    allow_headers=["*"],  # อนุญาตให้มีเฮดเดอร์ทุกประเภท
)

app.include_router(tablesRouters.router, prefix="/tables", tags=["test"]) # test
app.include_router(jobsRouters.router, prefix="/jobs", tags=["jobs"])
app.include_router(classificationRouters.router, prefix="/classification", tags=["classification"])
app.include_router(scrapingRouters.router, prefix="/scraping", tags=["scraping"])
app.include_router(companyRouters.router, prefix="/company", tags=["company"])
app.include_router(basicinfoRouters.router, prefix="/basicinfo", tags=["basicinfo"])
app.include_router(locationRouters.router, prefix="/location", tags=["location"])
app.include_router(salaryRouters.router, prefix="/salary", tags=["salary"])
app.include_router(imagetotextRouters.router, prefix="/imagetotext", tags=["imagetotext"])
app.include_router(extractskillsRouters.router, prefix="/extractskills", tags=["extractskills"])

app.include_router(subcategoryRouters.router, prefix="/subcategory", tags=["subcategory"])
app.include_router(maincategoryRouters.router, prefix="/maincategory", tags=["maincategoryRouters"])

app.include_router(mappingRouters.router, prefix="/mapping", tags=["mappingRouters"])
