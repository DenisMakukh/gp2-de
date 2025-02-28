"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 27.02.2025
"""
import os

from dotenv import load_dotenv

load_dotenv()

RABOTA_RU_CODE_TOKEN = os.getenv("RABOTA_RU_CODE_TOKEN")
RABOTA_RU_APP_ID = os.getenv("RABOTA_RU_APP_ID")
RABOTA_RU_APP_SECRET = os.getenv("RABOTA_RU_APP_SECRET")

SUPERJOB_SECRET = os.getenv("SUPERJOB_SECRET")
