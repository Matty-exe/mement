from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) ->None:
    await update.message.reply_text("Ciao")

async def ciao(update: Update, context: ContextTypes.DEFAULT_TYPE) ->None:
    await update.message.reply_photo('7318.jpg')

async def nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE) ->None:
    await update.message.reply_photo('6899.jpg')
def main() -> None:
    application = Application.builder().token('5297548426:AAF2fClwo2JHe4NoPNxQe8b7TIXy8rJ44rM').build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ciao", ciao))
    application.add_handler(CommandHandler("nsfw", nsfw))
    application.run_polling()
if __name__  == "__main__":
    main()