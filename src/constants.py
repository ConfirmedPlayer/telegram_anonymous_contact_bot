import os

from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('TOKEN')

BOT_OWNER_NICKNAME = os.getenv('BOT_OWNER_NICKNAME')
BOT_OWNER_ID = int(os.getenv('BOT_OWNER_ID'))
