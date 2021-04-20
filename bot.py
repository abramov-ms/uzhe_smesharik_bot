import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import handlers


PORT = int(os.environ.get("PORT", 8443))
TOKEN = "1725080540:AAEOekc4Wf7xGn1-Nza2CoBHJ6Rwn8GUbcQ"


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handlers.start))
    dispatcher.add_handler(CommandHandler("help", handlers.get_help))
    dispatcher.add_handler(CommandHandler("flat", handlers.get_flat_info))
    dispatcher.add_handler(CommandHandler("3d", handlers.get_3d_info))
    dispatcher.add_handler(CommandHandler("random", handlers.random_ep_info))
    dispatcher.add_handler(MessageHandler(Filters.text, handlers.echo))
    dispatcher.add_error_handler(handlers.error)

    updater.start_webhook(
        listen="0.0.0.0", port=PORT, url_path=TOKEN,
        webhook_url="https://uzhe-smesharik-bot.herokuapp.com/{}"
            .format(TOKEN))

    updater.idle()


if __name__ == "__main__":
    main()
