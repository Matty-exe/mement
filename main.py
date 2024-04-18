import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Variabile globale per memorizzare lo stato del timer
is_sending_enabled = False

# Funzione per ottenere il prezzo attuale di Bitcoin in euro
def get_btc_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur'
    response = requests.get(url)
    data = response.json()
    btc_price_eur = data['bitcoin']['eur']
    return btc_price_eur

# Funzione per inviare il prezzo di Bitcoin in euro
async def send_btc_price(context):
    chat_id = context['chat_id']
    btc_price = get_btc_price()
    await context['bot'].send_message(chat_id=chat_id, text=f"Prezzo attuale di Bitcoin in euro: {btc_price}")

# Gestore del comando /start per avviare l'invio periodico del prezzo di Bitcoin
async def start_sendbtc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_sending_enabled
    chat_id = update.message.chat_id
    if not is_sending_enabled:
        is_sending_enabled = True
        await update.message.reply_text("Invio periodico del prezzo di Bitcoin avviato.")
        # Avvia il timer per inviare il prezzo ogni 5 minuti
        while is_sending_enabled:
            await send_btc_price({'bot': context.bot, 'chat_id': chat_id})
            await asyncio.sleep(300)  # Attendi 5 minuti prima di inviare il prossimo messaggio
    else:
        await update.message.reply_text("L'invio periodico del prezzo di Bitcoin è già attivo.")

# Gestore del comando /stop per interrompere l'invio periodico del prezzo di Bitcoin
async def stop_sendbtc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_sending_enabled
    if is_sending_enabled:
        is_sending_enabled = False
        await update.message.reply_text("Invio periodico del prezzo di Bitcoin interrotto.")
    else:
        await update.message.reply_text("L'invio periodico del prezzo di Bitcoin non è attivo.")

# Crea l'applicazione Telegram
app = ApplicationBuilder().token("5297548426:AAF2fClwo2JHe4NoPNxQe8b7TIXy8rJ44rM").build()  # Assicurati di inserire il tuo token Telegram

# Aggiungi i gestori di comandi per /start e /stop
app.add_handler(CommandHandler("start", start_sendbtc))
app.add_handler(CommandHandler("stop", stop_sendbtc))

# Avvia l'applicazione
app.run_polling()