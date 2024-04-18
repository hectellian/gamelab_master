# gamelab_master

## Description

Simple bot to manage presence and open times of the Game Lab at the University of Geneva.

## Manual Use and Development

### Requirements

- Python 3.10+
- Poetry

### Installation

1. Clone the repository
```bash
git clone
```

1. Install the dependencies
```bash
poetry install
```

1. Create a `.env` file with the following content
```env
TOKEN = 'TELEGRAM_BOT_TOKEN'
COMITEE_CHAT_ID = 'COMITEE_CHAT_ID' 
OFFICIAL_CHAT_ID = 'OFFICIAL_CHAT_ID'
```

1. Run the bot
```bash
poetry run python run.py
```