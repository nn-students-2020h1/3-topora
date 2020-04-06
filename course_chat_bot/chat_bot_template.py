
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
from calculation_class import  calculatons
from log_class import logger as func_logger
from operator import itemgetter

from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

log=func_logger()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
@log.log_func
def corona_stats_dynamics(update: Update, context: CallbackContext):
    update.message.reply_text(calculatons.corona_stats_dynamics())

@log.log_func
def corono_stats(update: Update, context: CallbackContext):
    update.message.reply_text(calculatons.get_corona_dictlist_yesterday())


@log.log_func
def weather(update: Update, context: CallbackContext):
    update.message.reply_text(calculatons.get_weather())

@log.log_func
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


@log.log_func
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')

@log.log_func
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

@log.log_func
def chat_history(update: Update, context: CallbackContext):
    update.message.reply_text(log.last_5_history(update))

@log.log_func
def fact(update: Update, context: CallbackContext):
    update.message.reply_text(calculatons.get_cat_fact())


@log.log_func
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    bot = Bot(
        token=TOKEN,
        base_url=PROXY,  # delete it if connection via VPN
    )
    updater = Updater(bot=bot, use_context=True)
    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('history', chat_history))
    updater.dispatcher.add_handler(CommandHandler('fact', fact))
    updater.dispatcher.add_handler(CommandHandler('corono_stats',corono_stats))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.dispatcher.add_handler(CommandHandler('dynamics', corona_stats_dynamics))
    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    calculatons.get_corona_dictlist_yesterday()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()