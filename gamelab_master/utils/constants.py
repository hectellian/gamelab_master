import json

class Constants:
    def __init__(self):
        try:
            with open('data/schedule.json', 'r') as f:
                schedule = json.load(f)
                self.poll_day_of_week = schedule.get('poll_day_of_week', 'tue')
                self.poll_hour = schedule.get('poll_hour', 18)
                self.poll_minute = schedule.get('poll_minute', 0)
                self.announcement_day_of_week = schedule.get('announcement_day_of_week', 'tue')
                self.announcement_hour = schedule.get('announcement_hour', 23)
                self.announcement_minute = schedule.get('announcement_minute', 59)
        except FileNotFoundError:
            self.poll_day_of_week = 'tue'
            self.poll_hour = 18
            self.poll_minute = 0
            self.announcement_day_of_week = 'tue'
            self.announcement_hour = 23
            self.announcement_minute = 59

        try:
            with open('data/gamelab_schedule.json', 'r') as f:
                gamelab_schedule = json.load(f)
                self.gamelab_day_of_week = gamelab_schedule.get('gamelab_day_of_week', 'wed')
                self.gamelab_hour = gamelab_schedule.get('gamelab_hour', 18)
                self.gamelab_minute = gamelab_schedule.get('gamelab_minute', 0)
        except FileNotFoundError:
            self.gamelab_day_of_week = 'wed'
            self.gamelab_hour = 18
            self.gamelab_minute = 0

        self.welcome_message = (
            "Welcome to the Gamelab announcement group!"
            "\nYou will find all the information and rules about the Gamelab events here!"
            "\nRules:"
            "\n1. ..."
            "\n\nPlease verify your identity by sending a message with the following"
            "\n\n`/verify`"
            "Thank you!"
            "\n\n🎮🕹️🎲"
        )

    def save_schedule(self):
        """Save the schedule settings to a file."""
        schedule = {
            'poll_day_of_week': self.poll_day_of_week,
            'poll_hour': self.poll_hour,
            'poll_minute': self.poll_minute,
            'announcement_day_of_week': self.announcement_day_of_week,
            'announcement_hour': self.announcement_hour,
            'announcement_minute': self.announcement_minute,
        }
        with open('data/schedule.json', 'w') as f:
            json.dump(schedule, f)

    def save_gamelab_schedule(self):
        """Save the Gamelab schedule settings to a file."""
        gamelab_schedule = {
            'gamelab_day_of_week': self.gamelab_day_of_week,
            'gamelab_hour': self.gamelab_hour,
            'gamelab_minute': self.gamelab_minute,
        }
        with open('data/gamelab_schedule.json', 'w') as f:
            json.dump(gamelab_schedule, f)
