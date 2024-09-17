from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
import logging

class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

        paris_tz = timezone('Europe/Paris')
        self.scheduler = AsyncIOScheduler(timezone=paris_tz)
        self.scheduler.add_job(
            self.bot.poll_handlers.send_poll,
            trigger='cron',
            day_of_week=self.bot.constants.poll_day_of_week,
            hour=self.bot.constants.poll_hour,
            minute=self.bot.constants.poll_minute,
            id='send_poll_job',
            name='send_poll_job'
        )

    def start(self):
        self.scheduler.start()

    def pause(self):
        self.scheduler.pause()
        self.logger.info("Scheduler paused.")

    def resume(self):
        self.scheduler.resume()
        self.logger.info("Scheduler resumed.")

    def get_next_run_time(self, job_id):
        """Get the next run time of a scheduled job."""
        job = self.scheduler.get_job(job_id)
        if job:
            return job.next_run_time
        else:
            return None
