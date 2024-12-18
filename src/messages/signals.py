import random
from datetime import datetime, timedelta
from src.data.bets import BETS
from src.data.games import GAMES

class SignalManager:
    def __init__(self):
        self.bets = BETS
        self.games = GAMES

    def generate_signal(self, scheduled_time):
        # Seleciona aleatoriamente uma bet e um jogo
        bet = random.choice(self.bets)
        game = random.choice(self.games)
        
        # Calcula o horário de entrada (2 minutos após o envio)
        entry_time = scheduled_time + timedelta(minutes=2)
        
        signal_message = f"""
⚠️ SINAL IDENTIFICADO ⚠️

Meta (Até 5min)-> 5 MINUTOS

🕐 {bet['name']} no jogo {game['name']} em {entry_time.strftime('%H:%M')} 🔽

{game['instructions']}

🕯 Clique para abrir o aplicativo: {bet['app_deep_link']}

🆘 Não sabe operar ainda? Clique aqui: https://t.me/c/{CHANNEL_ID}/tutorial
"""
        return signal_message.strip()

    def generate_session_times(self, base_hour, base_minute):
        """Gera os horários para uma sessão de sinais"""
        times = []
        base = datetime.now().replace(
            hour=base_hour,
            minute=base_minute,
            second=0,
            microsecond=0
        )
        
        # Gera 4 horários com 15 minutos de intervalo
        for i in range(4):
            signal_time = base + timedelta(minutes=15*i)
            # Subtrai 2 minutos para enviar o sinal antes
            send_time = signal_time - timedelta(minutes=2)
            times.append(send_time)
            
        return times