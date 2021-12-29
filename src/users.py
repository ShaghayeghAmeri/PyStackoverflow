from src.db import db

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.db = db

    def get_user(self):
        return self.db.users.find_one({'chat.id': self.chat_id})

    def get_state(self):
        user = self.get_user()
        return user.get('state')
    
    def current_quastion(self):
        """
        Get current message
        """
        user = self.get_user()
        current_quastion = []
        if not user or not user.get('current_quastion'):
            return ''
        
        current_quastion = '\n\n'.join(user['current_quastion'])
        return f':right_arrow: Preview Quastion \n{current_quastion}'

    def reset(self):
        self.db.users.update_one({'chat.id': self.chat_id}, {'$set': {'current_quastion': []}})

    def update_state(self, chat_id, state):
        """
        Update user state.
        """
        self.db.users.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}}
        )

