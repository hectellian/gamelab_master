# library imports
import json
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, PollAnswerHandler
from apscheduler.schedulers.asyncio  import AsyncIOScheduler

# Your custom error types
from gamelab_master.error_types import PollError, CommunicationError

class GamelabMasterBot:
    def __init__(self, token, comitee_chat_id, official_chat_id):
        self.token = token
        self.comitee_chat_id = comitee_chat_id
        self.official_chat_id = official_chat_id
        self.poll_message_id = None
        
        with open('announcements.json', 'r') as file:
            self.announcements = json.load(file)['announcements']
        
        with open('closed.json', 'r') as file:
            self.closed = json.load(file)['announcements']

        # Set up the bot with Application (replaces Updater)
        self.application = Application.builder().token(token).build()

        # Configure logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Set up handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(PollAnswerHandler(self.handle_poll_answer))
        self.application.add_error_handler(self.error_callback)

        # Initialize and start the scheduler
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.send_poll, trigger='cron', day_of_week='tue', hour=18, minute=0)
        self.scheduler.add_job(self.check_poll_results, trigger='cron', day_of_week='tue', hour=23, minute=59)

    async def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        await update.message.reply_text('Hello! I will help manage your Gamelab events.')

    async def send_poll(self):
        """Send a poll to the comitee chat to ask if they will attend the Gamelab."""
        question = "Présence au Gamelab demain ?"
        options = ["J'y serai", "Pas cette fois"]
        try:
            msg = await self.application.bot.send_poll(chat_id=self.comitee_chat_id, question=question, options=options,
                                           is_anonymous=False, allows_multiple_answers=False)
            self.logger.info("Poll sent")
            self.poll_message_id = msg.message_id
        except Exception as e:
            self.logger.error("Failed to send poll: {}".format(e))
            raise PollError("Failed to send poll") from e

    async def handle_poll_answer(self, update: Update, context: CallbackContext) -> None:
        """Handle the poll answer and send a message to the official chat if enough people will attend."""
        options_counts = [0, 0]
        for answer in update.poll_answer.option_ids:
            options_counts[answer] += 1
            
        if options_counts[0] >= 2:
            try:
                await self.application.bot.send_message(chat_id=self.official_chat_id,
                                                  text=random.choice(self.announcements))
                self.logger.info("Announcement sent")
            except Exception as e:
                self.logger.error("Failed to send announcement: {}".format(e))
                raise CommunicationError("Failed to send announcement") from e
            
    async def check_poll_results(self):
        """Check if the required number of affirmative responses has been reached by midnight."""
        try:
            if self.poll_message_id is not None:
                poll_info = await self.application.bot.stop_poll(chat_id=self.comitee_chat_id, message_id=self.poll_message_id)
                count_yes = poll_info.options[0].voter_count
                if count_yes < 2:
                    await self.application.bot.send_message(chat_id=self.official_chat_id,
                                                            text=random.choice(self.closed))
        except Exception as e:
            self.logger.error(f"Failed to conclude poll: {e}")
            await self.application.bot.send_message(chat_id=self.official_chat_id,
                                                    text="Error concluding the attendance poll for Gamelab.")

    async def error_callback(self, update: Update, context: CallbackContext) -> None:
        """Log errors and send a message to the user about the encountered error."""
        self.logger.error('Update "{}" caused error "{}"'.format(update, context.error))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='An error occurred: {}'.format(context.error))

    def run(self):
        """Start the bot."""
        self.scheduler.start()
        self.application.run_polling()