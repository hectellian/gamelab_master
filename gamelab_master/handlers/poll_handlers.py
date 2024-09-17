from telegram.ext import PollAnswerHandler
from telegram import Update
import logging
import random
import datetime

class PollHandlers:
    def __init__(self, bot, application):
        self.bot = bot
        self.application = application
        self.logger = logging.getLogger(__name__)

        self.poll_message_id = None
        self.announcement_sent = False
        self.votes = [0, 0]
        self.last_poll_time = None
        self.last_announcement_time = None

    async def send_poll(self):
        if not self.bot.is_running:
            self.logger.info("Bot is stopped. Poll not sent.")
            return
        
        gamelab_day = self.bot.constants.gamelab_day_of_week
        gamelab_hour = self.bot.constants.gamelab_hour
        gamelab_minute = self.bot.constants.gamelab_minute
        
        day_names = {
            'mon': 'Lundi',
            'tue': 'Mardi',
            'wed': 'Mercredi',
            'thu': 'Jeudi',
            'fri': 'Vendredi',
            'sat': 'Samedi',
            'sun': 'Dimanche'
        }
        gamelab_day_name = day_names.get(gamelab_day, gamelab_day)
        
        question = f"Présence au Gamelab le {gamelab_day_name} à {gamelab_hour}:{gamelab_minute:02d}"
        options = ["Present", "Absent"]
        try:
            msg = await self.application.bot.send_poll(
                chat_id=self.bot.comitee_chat_id,
                question=question,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=False
            )
            self.logger.info("Poll sent")
            self.poll_message_id = msg.message_id
            self.announcement_sent = False
            self.votes = [0, 0]
            self.last_poll_time = datetime.datetime.now(datetime.timezone.utc)
        except Exception as e:
            self.logger.error(f"Failed to send poll: {e}")

    async def set_poll_time(self, update, context):
        try:
            day_of_week = context.args[0].lower()
            hour = int(context.args[1])
            minute = int(context.args[2])

            valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            if day_of_week not in valid_days:
                await update.message.reply_text(f"Invalid day of week. Choose from: {', '.join(valid_days)}")
                return

            self.bot.constants.poll_day_of_week = day_of_week
            self.bot.constants.poll_hour = hour
            self.bot.constants.poll_minute = minute

            self.bot.scheduler.scheduler.reschedule_job('send_poll_job', trigger='cron', day_of_week=day_of_week, hour=hour, minute=minute)

            self.bot.constants.save_schedule()

            await update.message.reply_text(f"Poll time updated to {day_of_week} at {hour}:{minute:02d}")

        except (IndexError, ValueError):
            await update.message.reply_text("Usage: /set_poll_time <day_of_week> <hour> <minute>")