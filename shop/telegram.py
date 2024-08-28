from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from male_fashion import settings

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Assalomu alaykum {user.first_name}!")

def send_order_info(update: Update, context: CallbackContext) -> None:
    order_info = context.args[0]
    update.message.reply_text(f"Yangi zakaz:\n{order_info}")

def main() -> None:
    updater = Updater(settings.TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("send_order_info", send_order_info))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
