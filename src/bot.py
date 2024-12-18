import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from src.messages.motivacional import MotivationalMessageManager
from src.messages.signals import SignalManager
from src.messages.raffle import RaffleMessageManager
from datetime import time

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='logs/bot.log'
)
logger = logging.getLogger(__name__)

# Configurações
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
TZ = timezone(os.getenv('TIMEZONE'))

async def start(update, context):
    await update.message.reply_text('Bot Indica Bet iniciado!')

async def send_message_to_channel(context, message):
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode='HTML'
    )

async def send_morning_motivation(context):
    message = motivational_manager.get_morning_message()
    await send_message_to_channel(context, message)

async def send_night_motivation(context):
    message = motivational_manager.get_night_message()
    await send_message_to_channel(context, message)

async def send_signal(context):
    # Obtém o horário agendado do job
    scheduled_time = context.job.next_run_time
    
    # Gera e envia o sinal
    signal = signal_manager.generate_signal(scheduled_time)
    await send_message_to_channel(context, signal)

# Comandos para teste
async def test_motivation(update, context):
    await send_morning_motivation(context)
    await send_night_motivation(context)

async def test_signal(update, context):
    await send_signal(context)
    
async def test_raffle(update, context):
    await send_raffle_message(context)

def schedule_signal_sessions(application, scheduler):
    """Agenda as duas sessões diárias de sinais"""
    
    # Sessão da manhã (8:00-9:00)
    morning_times = signal_manager.generate_session_times(8, 0)
    for time in morning_times:
        scheduler.add_job(
            send_signal,
            trigger='cron',
            hour=time.hour,
            minute=time.minute,
            kwargs={'context': application}
        )
    
    # Sessão da noite (18:30-19:30)
    evening_times = signal_manager.generate_session_times(18, 30)
    for time in evening_times:
        scheduler.add_job(
            send_signal,
            trigger='cron',
            hour=time.hour,
            minute=time.minute,
            kwargs={'context': application}
        )

async def send_raffle_message(context):
    message = raffle_manager.get_raffle_message()
    await send_message_to_channel(context, message)

def schedule_raffle_message(application, scheduler):
    """Agenda a mensagem de sorteio para um horário aleatório entre 13:00 e 17:00"""
    random_time = raffle_manager.get_random_time()
    
    scheduler.add_job(
        send_raffle_message,
        trigger='cron',
        hour=random_time.hour,
        minute=random_time.minute,
        kwargs={'context': application}
    )
    
    # Agenda para gerar novo horário aleatório todos os dias à meia-noite
    scheduler.add_job(
        schedule_raffle_message,
        trigger='cron',
        hour=0,
        minute=0,
        kwargs={'application': application, 'scheduler': scheduler}
    )

# Comando de status
async def status(update, context):
    now = datetime.now(TZ)
    status_message = f"""
🤖 Status do Bot Indica Bet

⏰ Hora atual: {now.strftime('%H:%M:%S')}

📅 Próximas mensagens:
- Motivacional manhã: 07:00
- Sinais manhã: 08:00-09:00
- Sorteio: {raffle_manager.get_random_time().strftime('%H:%M')}
- Sinais noite: 18:30-19:30
- Motivacional noite: 22:00

✅ Bot funcionando normalmente
"""
    await update.message.reply_text(status_message)

def main():
    # Inicializa o bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adiciona handlers
    application.add_handler(CommandHandler("start", start))
    
    # Inicializa o scheduler
    scheduler = AsyncIOScheduler(timezone=TZ)
    
    # Inicializa os gerenciadores
    global motivational_manager, signal_manager, raffle_manager
    motivational_manager = MotivationalMessageManager()
    signal_manager = SignalManager()
    raffle_manager = RaffleMessageManager()
    
    # Agenda as mensagens motivacionais
    scheduler.add_job(
        send_morning_motivation,
        trigger='cron',
        hour=7,
        minute=0,
        kwargs={'context': application}
    )
    
    scheduler.add_job(
        send_night_motivation,
        trigger='cron',
        hour=22,
        minute=0,
        kwargs={'context': application}
    )

    schedule_signal_sessions(application, scheduler)

    schedule_raffle_message(application, scheduler)

    # Comandos para teste
    application.add_handler(CommandHandler("test_signal", test_signal))
    application.add_handler(CommandHandler("test_raffle", test_raffle))
    application.add_handler(CommandHandler("test_motivation", test_motivation))

    # Comando de status
    application.add_handler(CommandHandler("status", status))

    # Inicia o scheduler
    scheduler.start()
    
    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()