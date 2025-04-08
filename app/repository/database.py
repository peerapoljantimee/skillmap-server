# app\repository\database.py

from sqlalchemy.ext.asyncio import create_async_engine 
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = (
    f"mysql+asyncmy://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# สร้าง Engine
engine = create_async_engine(DATABASE_URL)
