from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, filters
from pytz import timezone
import logging

class CommandHandlers:
    def __init__(self, bot, application):
        self.bot = bot
        self.application = application
        self.logger = logging.getLogger(__name__)
        self.bot_stopped_message = "Bot is currently stopped. Please start the bot to use this command."

        self.start_handler = CommandHandler("start", self.start, filters=filters.Chat(chat_id=self.bot.comitee_chat_id))
        self.help_handler = CommandHandler("help", self.help_command, filters=filters.Chat(chat_id=self.bot.comitee_chat_id))
        self.info_handler = CommandHandler("info", self.info_command)
        self.poll_handler = CommandHandler("poll", self.poll, filters=filters.Chat(chat_id=self.bot.comitee_chat_id))
        self.set_poll_time_handler = CommandHandler("set_poll_time", self.set_poll_time, filters=filters.Chat(chat_id=self.bot.comitee_chat_id))
        self.set_gamelab_time_handler = CommandHandler("set_gamelab_time", self.set_gamelab_time, filters=filters.Chat(chat_id=self.bot.comitee_chat_id))
        self.verify_handler = CommandHandler("verify", self.verify_user)
        self.stop_handler = CommandHandler("stop", self.stop_bot, filters=filters.Chat(chat_id=self.bot.comitee_chat_id))

    async def start(self, update: Update, context: CallbackContext) -> None:
        if not self.bot.is_running:
            self.bot.scheduler.resume()
            self.bot.is_running = True
            self.logger.info("Bot is back online!")
        await update.message.reply_text('Hello! I will help manage your Gamelab events.')

    async def help_command(self, update: Update, context: CallbackContext) -> None:
        help_text = (
            "Available commands:\n"
            "/start - Start the bot or get a welcome message\n"
            "/help - Show this help message\n"
            "/info - Display bot status and schedule information\n"
            "/poll - Send the attendance poll\n"
            "/set_poll_time <day_of_week> <hour> <minute> - Set the poll schedule\n"
            "/set_gamelab_time <day_of_week> <hour> <minute> - Set the Gamelab event day and time\n"
            "/stop - Stop the bot\n"
        )
        await update.message.reply_text(help_text)

    async def info_command(self, update: Update, context: CallbackContext) -> None:
        """Display information about the bot's schedule and status."""
        status = "🟢 Running" if self.bot.is_running else "🔴 Stopped"

        last_poll_time = self.bot.poll_handlers.last_poll_time

        next_poll_time = self.bot.scheduler.get_next_run_time('send_poll_job')

        # Gamelab event time
        gamelab_day = self.bot.constants.gamelab_day_of_week
        gamelab_hour = self.bot.constants.gamelab_hour
        gamelab_minute = self.bot.constants.gamelab_minute

        # Convert day_of_week to French day name
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

        # Format time as "18h" or "18h30"
        if gamelab_minute == 0:
            gamelab_time_str = f"{gamelab_hour}h"
        else:
            gamelab_time_str = f"{gamelab_hour}h{gamelab_minute:02d}"

        # Format times
        def format_time(dt):
            if dt is None:
                return "N/A"
            else:
                # Convert to local timezone (Paris)
                paris_tz = timezone('Europe/Paris')
                return dt.astimezone(paris_tz).strftime('%Y-%m-%d %H:%M:%S %Z')

        info_message = (
            f"**Bot Status:** {status}\n\n"
            f"**Last Poll Sent:** {format_time(last_poll_time)}\n"
            f"**Next Poll Scheduled:** {format_time(next_poll_time)}\n"
            f"--\n"
            f"**Gamelab Event:** Tout les {gamelab_day_name} at {gamelab_time_str}\n"
        )

        await update.message.reply_text(info_message, parse_mode='Markdown')

    async def poll(self, update: Update, context: CallbackContext) -> None:
        if not self.bot.is_running:
            await update.message.reply_text(self.bot_stopped_message)
            return
        await self.bot.poll_handlers.send_poll()
        
    async def set_gamelab_time(self, update: Update, context: CallbackContext) -> None:
        if update.effective_chat.id != self.bot.comitee_chat_id:
            return
        if not self.bot.is_running:
            await update.message.reply_text("Bot is currently stopped. Please start the bot to use this command.")
            return
        try:
            # Expecting arguments: day_of_week hour minute
            day_of_week = context.args[0].lower()
            hour = int(context.args[1])
            minute = int(context.args[2])

            # Validate day_of_week
            valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            if day_of_week not in valid_days:
                await update.message.reply_text(f"Invalid day of week. Choose from: {', '.join(valid_days)}")
                return

            # Update Gamelab schedule variables
            self.bot.constants.gamelab_day_of_week = day_of_week
            self.bot.constants.gamelab_hour = hour
            self.bot.constants.gamelab_minute = minute

            # Save the schedule
            self.bot.constants.save_gamelab_schedule()

            await update.message.reply_text(f"Gamelab time updated to {day_of_week} at {hour}:{minute:02d}")

        except (IndexError, ValueError):
            await update.message.reply_text("Usage: /set_gamelab_time <day_of_week> <hour> <minute>")

    async def set_poll_time(self, update: Update, context: CallbackContext) -> None:
        if not self.bot.is_running:
            await update.message.reply_text(self.bot_stopped_message)
            return
        await self.bot.poll_handlers.set_poll_time(update, context)

    async def verify_user(self, update: Update, context: CallbackContext) -> None:
        if not self.bot.is_running:
            await update.message.reply_text("Bot is currently stopped. Please wait until the bot is started again.")
            return
        await self.bot.member_handlers.verify_user(update, context)

    async def stop_bot(self, update: Update, context: CallbackContext) -> None:
        self.bot.is_running = False
        self.bot.scheduler.pause()
        await update.message.reply_text("Bot has been stopped. Use /start to start it again.")
        self.logger.info("Bot stopped.")

    async def error_handler(self, update: object, context: CallbackContext) -> None:
        self.logger.error('Update "%s" caused error "%s"', update, context.error)
        if isinstance(update, Update) and update.effective_chat:
            try:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f"An error occurred: {context.error}")
            except Exception as e:
                self.logger.error(f"Failed to send error message: {e}")
