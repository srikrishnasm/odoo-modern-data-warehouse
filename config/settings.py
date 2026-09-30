import os

from dotenv import load_dotenv


load_dotenv()


# Odoo
ODOO_URL = os.getenv("ODOO_URL")
ODOO_API_KEY = os.getenv("ODOO_API_KEY")


# Cloudflare R2
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")


# Validation
if not ODOO_URL:
    raise ValueError("ODOO_URL is not set in .env")

if not ODOO_API_KEY:
    raise ValueError("ODOO_API_KEY is not set in .env")

if not R2_ACCOUNT_ID:
    raise ValueError("R2_ACCOUNT_ID is not set in .env")

if not R2_ACCESS_KEY_ID:
    raise ValueError("R2_ACCESS_KEY_ID is not set in .env")

if not R2_SECRET_ACCESS_KEY:
    raise ValueError("R2_SECRET_ACCESS_KEY is not set in .env")

if not R2_BUCKET_NAME:
    raise ValueError("R2_BUCKET_NAME is not set in .env")


ODOO_URL = ODOO_URL.rstrip("/")