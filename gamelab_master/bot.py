import logging
from telegram.ext import Application
from gamelab_master.handlers.command_handlers import CommandHandlers
from gamelab_master.handlers.poll_handlers import PollHandlers
from gamelab_master.utils.scheduler import Scheduler
from gamelab_master.utils.constants import Constants

class GamelabMasterBot:
    def __init__(self, token, comitee_chat_id, official_chat_id):
        self.token = token
        self.comitee_chat_id = comitee_chat_id
        self.official_chat_id = official_chat_id

        self.application = Application.builder().token(self.token).build()
        self.logger = logging.getLogger(__name__)
        self.constants = Constants()
        self.is_running = True 

        self.command_handlers = CommandHandlers(
            bot=self,
            application=self.application
        )
        self.poll_handlers = PollHandlers(
            bot=self,
            application=self.application
        )

        self.add_handlers()

        self.scheduler = Scheduler(
            bot=self
        )

    def add_handlers(self):
        dp = self.application
        dp.add_handler(self.command_handlers.start_handler)
        dp.add_handler(self.command_handlers.help_handler)
        dp.add_handler(self.command_handlers.info_handler)
        dp.add_handler(self.command_handlers.poll_handler)
        dp.add_handler(self.command_handlers.set_gamelab_time_handler)
        dp.add_handler(self.command_handlers.set_poll_time_handler)
        dp.add_handler(self.command_handlers.verify_handler)
        dp.add_handler(self.command_handlers.stop_handler)

        dp.add_error_handler(self.command_handlers.error_handler)

    def run(self):
        self.scheduler.start()
        self.application.run_polling()
