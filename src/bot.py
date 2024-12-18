import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from src.messages.motivational import MotivationalMessageManager
from src.messages.signals import SignalManager

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

def main():
    # Inicializa o bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adiciona handlers
    application.add_handler(CommandHandler("start", start))
    
    # Inicializa o scheduler
    scheduler = AsyncIOScheduler(timezone=TZ)
    
    # Inicializa os gerenciadores
    global motivational_manager, signal_manager
    motivational_manager = MotivationalMessageManager()
    signal_manager = SignalManager()
    
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

    # Comandos para teste
    application.add_handler(CommandHandler("test_signal", test_signal))
    application.add_handler(CommandHandler("test_signal", test_signal))
    
    # Inicia o scheduler
    scheduler.start()
    
    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()