"""Main Settings File"""

import os
from dotenv import load_dotenv

load_dotenv()

# ----------- Database
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# ----------- Authentication
ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecretkey")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 10080))  # 7 days * 24 * 60

# ----------- Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "noreply@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-email-password")

# ----------- Celery Settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# ----------- Frontend (for email verify link etc.)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")
