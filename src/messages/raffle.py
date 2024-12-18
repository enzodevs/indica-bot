import random
from datetime import datetime, time

class RaffleMessageManager:
    def __init__(self):
        self.raffle_message = """
🎉 SORTEIO DIÁRIO INDICA BET 🎉

💰 Quer participar dos nossos sorteios diários?
É muito simples:

1️⃣ Abra o app Indica Bet
2️⃣ Faça pelo menos 3 operações hoje
3️⃣ Pronto! Você já está participando! 

🏆 Prêmios:
- 1º Lugar: R$ 1.000,00
- 2º Lugar: R$ 500,00
- 3º Lugar: R$ 250,00

⚡️ Quanto mais você operar, mais chances tem de ganhar!

📱 Não perca tempo, abra seu app agora:
{app_link}

❓ Ainda não tem o app? Adquira agora:
{purchase_link}
"""

    def get_raffle_message(self):
        return self.raffle_message.format(
            app_link="https://playstore.indicabet.site",
            purchase_link="https://playstore.indicabet.site"
        )

    def get_random_time(self):
        """Gera um horário aleatório entre 13:00 e 17:00"""
        hour = random.randint(13, 16)
        minute = random.randint(0, 59)
        return time(hour=hour, minute=minute)