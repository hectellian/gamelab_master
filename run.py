# library imports
import os
from dotenv import load_dotenv

# module imports
from gamelab_master.bot import GamelabMasterBot

load_dotenv()

TOKEN = os.getenv('TOKEN')
COMITEE_CHAT_ID = os.getenv('COMITEE_CHAT_ID')
OFFICIAL_CHAT_ID = os.getenv('OFFICIAL_CHAT_ID')

if __name__ == '__main__':
    bot = GamelabMasterBot(TOKEN, COMITEE_CHAT_ID, OFFICIAL_CHAT_ID)
    bot.run()