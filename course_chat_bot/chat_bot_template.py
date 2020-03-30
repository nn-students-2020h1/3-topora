
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

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import datetime
import requests
import csv
from operator import itemgetter

from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def yesterday_date():
    #здесь сегодняшяя дата должна превращаться во вчерашнюю
    pass

def get_confirmed(item):
    return int(itemgetter('Confirmed')(item))-int(itemgetter('Recovered')(item))-int(itemgetter('Deaths')(item))

def get_corona_dictlist_yesterday():
    data=datetime.date.today()
    mainurl_corona='https://raw.github.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
   # req=requests.get(f'{mainurl_corona}{}')
    if data.day>10:
        if data.month>=10:
            req=requests.get(f'{mainurl_corona}{str(data.month)}-{str(data.day-1)}-2020.csv')
        else:
            req = requests.get(f'{mainurl_corona}0{str(data.month)}-{str(data.day-1)}-2020.csv')
    else:
        if data.month>10:
            req = requests.get(f'{mainurl_corona}{str(data.month)}-0{str(data.day-1)}-2020.csv')
        else:
            req = requests.get(f'{mainurl_corona}0{str(data.month)}-0{str(data.day-1)}-2020.csv')
    logger.info(req.status_code)
    with open('now.csv','wb+') as now:
        now.write(req.content)
    with open('now.csv','r') as now:
        now_dict=csv.DictReader(now)
        sort_dictlist=list(now_dict)
        sort_dictlist=sorted(sort_dictlist,key=get_confirmed,reverse=True)
    return sort_dictlist


log=[]
def log_f(func):
    def inner(*args, **kwargs):
        """For showing time"""
        now = datetime.datetime.now()
        func(*args,**kwargs)
        info = dict()
        info["username"]=args[0].effective_user.first_name
        try:
            info["username"]+= " " + args[0].effective_user.last_name
        except BaseException:
            pass
        info["nickname"]=args[0].effective_user.username
        info["funcname"]=func.__name__
        info["message"]=args[0].message.text
        info["date"]=str(now)
        global log
        log.append(info)
        with open("bot_log.txt", "a", encoding="utf-8") as log_open:
            for i in range(len(log)):
                print(log[i], file=log_open)
    return inner


@log_f
def corono_stats(update: Update, context: CallbackContext):
    corono_dictlist = get_corona_dictlist_yesterday()
    msg='Топ 5 местностей по заражению на сегодня:\n'
    for i in range(0,5):

        if len((corono_dictlist[i]['Province/State']))>0:
            msg+=(corono_dictlist[i]['Province/State']+':')
        msg+=corono_dictlist[i]['Country/Region']+'\n'
    update.message.reply_text(msg)
@log_f
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


@log_f
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')

@log_f
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

@log_f
def chat_history(update: Update, context: CallbackContext):
    """Echo the user history."""
    """message is the answer for a user"""
    message=''
    """File with the name of user"""
    with open(f"log_{update.effective_user.first_name}.txt","a", encoding="utf-8") as fopen:
        counter=0

        """searching last 5 or less messages for this user, logging to the file and forming the answer"""
        for i in range(len(log)):
            if (log[len(log)-1-i]['nickname'] == update.effective_user.username):
                print(log[len(log)-1-i],file=fopen)
                message=log[len(log)-1-i]["message"] + "\n" + message
                counter += 1
            if counter == 5:
                break

        update.message.reply_text(f"History:\n{message}")

@log_f
def fact(update: Update, context: CallbackContext):
    r = requests.get('https://cat-fact.herokuapp.com/facts')
    d = r.json()
    maxv = 0
    for i in range(len(d['all'])):
        if d['all'][i]['upvotes'] >= maxv:
            maxv = d['all'][i]['upvotes']
            fact = d['all'][i]['text']
    update.message.reply_text(f"Fact: \n{fact}")


@log_f
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
    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()

