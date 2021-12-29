# Stackoverflow Telegram Bot

Stackoverflow Telegram Bot is a Telegram bot that allows you to send questions to other users and receive answers from them, similar to Stackoverflow.com.

Users can send question and receive answers, upvote/downvote, like, bookmark posts, and more.

## How to Run
1. Set your telegram bot token as environment variable `TELEGRAM_BOT_TOKEN`:
```
export TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
```

2. Add `src` to `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

3. Run:
```
python src/run.py
```
