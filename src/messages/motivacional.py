import random
from datetime import datetime
from src.data.motivational_messages import MOTIVATIONAL_MESSAGES

class MotivationalMessageManager:
    def __init__(self):
        self.morning_messages = [msg for msg in MOTIVATIONAL_MESSAGES if msg["morning"]]
        self.night_messages = [msg for msg in MOTIVATIONAL_MESSAGES if not msg["morning"]]
        self.last_morning_index = -1
        self.last_night_index = -1

    def get_morning_message(self):
        if not self.morning_messages:
            return "Mensagem motivacional da manhã não disponível."
        
        self.last_morning_index = (self.last_morning_index + 1) % len(self.morning_messages)
        return self.morning_messages[self.last_morning_index]["message"]

    def get_night_message(self):
        if not self.night_messages:
            return "Mensagem motivacional da noite não disponível."
        
        self.last_night_index = (self.last_night_index + 1) % len(self.night_messages)
        return self.night_messages[self.last_night_index]["message"]