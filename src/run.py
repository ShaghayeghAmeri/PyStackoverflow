import emoji
from loguru import logger
from telebot import custom_filters

from src.bot import bot
from src.constants import keyboards, keys, states
from src.data import DATA_DIR
from src.db import db
from src.filters import IsAdmin
from src.utils.io import read_file, read_json
from src.utils.keyboard import create_keyboard
from src.users import User


class Bot:
    """
    Template for telegram bot.
    """
    def __init__(self, telebot, mongodb):
        self.bot = telebot
        self.db = mongodb

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())
        self.bot.add_custom_filter(custom_filters.TextMatchFilter())
        self.bot.add_custom_filter(custom_filters.TextStartsFilter())

        # register handlers
        self.handlers()

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, 
            f"Hey, <strong>{message.chat.first_name}</strong>",
            reply_markup=keyboards.main
            )
           
            self.db.users.update_one(
                {'chat.id': message.chat.id}, 
                {'$set': message.json}, 
                upsert=True
            )
            self.update_state(message.chat.id, states.main)

        @self.bot.message_handler(text=[emoji.emojize(keys.ask_question)])
        def ask_quastion(message):
            self.update_state(message.chat.id, states.ask_question)
            self.bot.send_message(
                message.chat.id,
                read_file(DATA_DIR / 'guide.html'),
                reply_markup=create_keyboard(keys.cancel)
            )

        @self.bot.message_handler(text=[emoji.emojize(keys.cancel)])
        def cancel(message):
            user = User(chat_id=message.chat.id)
            user.reset()
            self.update_state(message.chat.id, states.main)
            self.bot.send_message(
                message.chat.id,
                emoji.emojize(':cross_mark: Canceled.'),
                reply_markup=keyboards.main
            )

        @self.bot.message_handler(text=[keys.settings])
        def settings(message):
            pass

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, '<strong>You are admin of this group!</strong>')

        @self.bot.message_handler(func=lambda ـ: True)
        def echo(message):
            user = User(chat_id=message.chat.id)
            if user.get_state() == states.ask_question:
                self.db.users.update_one(
                    {'chat.id': message.chat.id},
                    {'$push': {'current_quastion': message.text}}
                )
                self.send_message(
                    message.chat.id, 
                    user.current_quastion(),
                    reply_markup=keyboards.ask_quastion
                )

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        Send message to telegram bot having a chat_id and text_content.
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_state(self, chat_id, state):
        """
        Update user state.
        """
        self.db.users.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}}
        )


if __name__ == '__main__':
    logger.info('Bot started')
    nashenas_bot = Bot(telebot=bot, mongodb=db)
    nashenas_bot.run()
