# library imports
import os
from dotenv import load_dotenv
import logging

# module imports
from gamelab_master.bot import GamelabMasterBot

load_dotenv()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    TOKEN = os.getenv('TOKEN')
    COMITEE_CHAT_ID = int(os.getenv('COMITEE_CHAT_ID'))
    OFFICIAL_CHAT_ID = int(os.getenv('OFFICIAL_CHAT_ID'))
    bot = GamelabMasterBot(TOKEN, COMITEE_CHAT_ID, OFFICIAL_CHAT_ID)
    bot.run()

if __name__ == '__main__':
    main()