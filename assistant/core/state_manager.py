class StateManager:
    def __init__(self):
        self.states = {}

    def set_state(self, user_id, state):
        """Устанавливает состояние пользователя"""
        self.states[user_id] = state

    def get_state(self, user_id):
        """Возвращает текущее состояние пользователя"""
        return self.states.get(user_id, None)

    def clear_state(self, user_id):
        """Удаляет состояние пользователя"""
        if user_id in self.states:
            del self.states[user_id]