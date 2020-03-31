import datetime
import logging
from telegram import Bot, Update

class logger:
    def __init__(self):
        self.log=[]

    def log_func(self,func):
        def inner(*args, **kwargs):
            """For showing time"""
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.INFO)
            inner_logger = logging.getLogger(__name__)
            now = datetime.datetime.now()
            func(*args, **kwargs)
            info = dict()
            info["username"] = args[0].effective_user.first_name
            try:
                info["username"] += " " + args[0].effective_user.last_name
            except BaseException:
                pass
            info["nickname"] = args[0].effective_user.username
            info["funcname"] = func.__name__
            info["message"] = args[0].message.text
            info["date"] = str(now)
            self.log.append(info)
            with open("bot_log.txt", "a", encoding="utf-8") as log_open:
                for i in range(len(self.log)):
                    print(self.log[i], file=log_open)
            inner_logger.info(self.log)
        return inner

    def last_5_history(self,update: Update):
        """Echo the user history."""
        """message is the answer for a user"""
        message = ''
        """File with the name of user"""
        # может вынести поиск по логу в класс
        with open(f"log_{update.effective_user.first_name}.txt", "a", encoding="utf-8") as fopen:
            counter = 0
            """searching last 5 or less messages for this user, logging to the file and forming the answer"""
            for i in range(len(self.log)):
                if (self.log[len(self.log) - 1 - i]['nickname'] == update.effective_user.username):
                    print(self.log[len(self.log) - 1 - i], file=fopen)
                    message = self.log[len(self.log) - 1 - i]["message"] + "\n" + message
                    counter += 1
                if counter == 5:
                    break
            return f'History:\n{message}'
