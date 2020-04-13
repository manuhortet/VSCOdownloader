import telegram
import logging
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import run_async

from bot.downloader import download_picture
from credentials.credentials import token

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telegram.Bot(token=token)


@run_async
def start(bot, update):
    username = update.effective_user.name
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Hey {}. Use /help if you need instructions.".format(username))
    logging.info(f'Listening to {username}.')


@run_async
def download(bot, update):

    if len(update.message.entities) != 1:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Invalid format. Try /help.")
        logging.warning(
            f'{update.effective_user.name} tried to download without providing an URL.')
        return

    link = update.message.parse_entity(update.message.entities[0])
    picture, author = download_picture(link)

    if picture:
        bot.sendPhoto(chat_id=update.message.chat_id, photo=picture,
                      caption=f"via @{author.replace(' ', '-')}")
        logging.info(f'Sending {link} to {update.effective_user.name}.')
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="I couldn't find any picture following that link.")
        logging.warning(f'Failed to send {link} to {update.effective_user.name}.')


@run_async
def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="To download a picture from VSCO, just share the public URL of the picture with me.")


def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(Filters.text, download))

    logging.info("Bot running at @VSCOdownloader_bot")
    updater.start_polling()
    updater.idle()
