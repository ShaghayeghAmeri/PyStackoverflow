import emoji

from src.constants import keys, states
from src.db import db
import concurrent.futures
from loguru import logger


class User:
    def __init__(self, chat_id, mongodb, stackbot, message):
        self.chat_id = chat_id
        self.db = mongodb
        self.stackbot = stackbot
        self.message = message

    @property
    def user(self):
        return self.db.users.find_one({'chat.id': self.chat_id})

    @property
    def state(self):
        return self.user.get('state')

    @property
    def question(self):
        """
        Get current question raw message text.
        """
        return '\n'.join(self.user.get('current_question', []))

    @property
    def current_question(self):
        """
        Get current question full message.
        """
        question_text = ':pencil: <strong>Question Preview</strong>\n\n'
        question_text += self.question
        question_text += f'\n{"_" * 40}\nWhen done, click <strong>{keys.send_question}</strong>.'
        return question_text


    def save_question(self):
        """
        save question to database
        """
        user = self.user
        if not user or not user.get('current_question'):
            self.send_message(text='Question is empty!')
            return False
        logger.info('message saved!')
        self.db.questions.insert_one({
            'chat_id': self.chat_id,
            'question': self.user.get('current_question', []),
            'date': self.message.date,
        })
        return True

    def send_to_all(self):
        user = self.user
        user_name = f"@{user['chat'].get('username')}"
        first_name = user['chat']['first_name']
        msg_txt = f':bus_in_silhouette:{user_name or first_name} asked:\n'
        msg_txt += ':red_question_mark:<strong>New Question</strong>\n'
        msg_txt += self.question
        logger.info('send 1')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for chat_id in self.db.users.distinct('chat.id'):
                executor.submit(
                    self.stackbot.send_message,
                    chat_id,
                    msg_txt
                )
        logger.info('send 2')
        self.send_message(text='Your message sent succesfully to all users')

    def update_state(self, state):
        """
        Update user state.
        """
        self.db.users.update_one(
            {'chat.id': self.chat_id},
            {'$set': {'state': state}}
        )

    def send_message(self, text, reply_markup=None, emojize=True):
        """
        Send message to telegram bot having a chat_id and text_content.
        """
        if emojize:
            text = emoji.emojize(text)

        self.stackbot.send_message(self.chat_id, text, reply_markup=reply_markup)

    def reset(self):
        self.db.users.update_one({'chat.id': self.chat_id}, {'$set': {'current_question': [], 'state': states.main}})


