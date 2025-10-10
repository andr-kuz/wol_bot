import os
from dotenv import load_dotenv

load_dotenv()


TARGET_MAC = os.getenv('TARGET_MAC', '')
TARGET_IP = os.getenv('TARGET_IP', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
USER_ID = int(os.getenv('USER_ID', None))
