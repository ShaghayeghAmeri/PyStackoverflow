import emoji

from src.constants import keys, states
from src.db import db


class User:
    def __init__(self, chat_id, mongodb, bot):
        self.chat_id = chat_id
        self.db = mongodb
        self.bot = bot

    @property
    def user(self):
        return self.db.users.find_one({'chat.id': self.chat_id})

    @property
    def state(self):
        return self.user.get('state')

    
    @property
    def current_quastion(self):
        """
        Get current message
        """
        user = self.user
        if not user or not user.get('current_quastion'):
            return ''
        
        current_quastion = ':pencil: Preview Quastion\n\n'
        current_quastion += '\n'.join(user['current_quastion'])
        current_quastion += f'\n{"-"*50}\nWhen done, click {keys.send_quastion}'
        return current_quastion


    def save_quastion(self):
        """
        save question to database
        """
        user = self.user
        if not user or not user.get('current_quastion'):
            return
        
        self.db.quastion.insert_one(
            'chat_id': self.chat_id,
            'current_quastion': user['current_quastion']
        )
        self.db.users.update_one(
            {'chat_id': self.chat_id},
            {'$set': {'current_quastion': []}}
        )

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

        self.bot.send_message(self.chat_id, text, reply_markup=reply_markup)

    def reset(self):
        self.db.users.update_one({'chat.id': self.chat_id}, {'$set': {'current_quastion': [], 'state': states.main}})


