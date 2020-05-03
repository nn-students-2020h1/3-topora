import datetime
import requests
import csv
import pymongo
from random import random


class Calculations:

    @staticmethod
    def get_msg_for_corona():    # str
        try:
            sort_dictlist = Calculations.sort_corona_dict()
        except BaseException:
            return 'Error occurred'
        msg = 'Топ 5 местностей по зарегистрированным заражениям на сегодня:\n'
        for i in range(0, 5):
            if len((sort_dictlist[i]['Province_State'])) > 0:
                msg += sort_dictlist[i]['Province_State'] + ':'
            msg += sort_dictlist[i]['Country_Region'] + '\n'
        return msg

    @staticmethod
    def get_corona_data_by_date(date):  # Responce
        mainurl_corona = 'https://raw.github.com/CSSEGISandData' \
                         '/COVID-19/master/csse_covid_19_data' \
                         '/csse_covid_19_daily_reports/'
        try:
            if date.day >= 10:
                if date.month >= 10:
                    req = requests.get(f'{mainurl_corona}'
                                       f'{str(date.month)}-'
                                       f'{str(date.day)}-2020.csv')
                else:
                    req = requests.get(f'{mainurl_corona}'
                                       f'0{str(date.month)}-'
                                       f'{str(date.day)}-2020.csv')
            else:
                if date.month > 10:
                    req = requests.get(f'{mainurl_corona}'
                                       f'{str(date.month)}-'
                                       f'0{str(date.day)}-2020.csv')
                else:
                    req = requests.get(f'{mainurl_corona}'
                                       f'0{str(date.month)}-'
                                       f'0{str(date.day)}-2020.csv')
            return req
        except BaseException:
            return None

    @staticmethod
    def sort_corona_dict():
        date = datetime.date.today() - datetime.timedelta(days=1)
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        name_date = str(date.day) + str(date.month) + str(date.year)
        Calculations._data_check(bd, date)
        corona_collection_today = bd[name_date]
        sort_dictlist = []
        for line in corona_collection_today.find():
            sort_dictlist.append(line)
        sort_dictlist = sorted(sort_dictlist, key=lambda record: int(
            record['Confirmed']), reverse=True)
        return sort_dictlist

    @staticmethod
    def _data_check(bd, date):
        if str(date.day) + str(date.month) + str(date.year) in bd.list_collection_names():
            return 1
        else:
            Calculations._corona_data_download(bd, date, Calculations.get_corona_data_by_date(date))

    @staticmethod
    def _get_collection_by_date(bd, date):
        return bd[str(date.day) + str(date.month) + str(date.year)]

    @staticmethod
    def _corona_data_download(bd, date, corona_data):
        #collection = bd[str(date.day) + str(date.month) + str(date.year)]
        for row in list(csv.DictReader(corona_data.content.decode(
                'utf-8').splitlines(), delimiter=',')):
            row['Confirmed'] = int(row['Confirmed'])
            Calculations._get_collection_by_date(bd, date).insert_one(row)

    @staticmethod
    def corona_stats_dynamics():
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        Calculations._data_check(bd, datetime.date.today() - datetime.timedelta(days=1))
        Calculations._data_check(bd, datetime.date.today() - datetime.timedelta(days=2))
        msg = "Со вчерашнего дня заразилось " + \
              str(Calculations.today_yesterday_diff(bd)) + " человек"
        return msg

    @staticmethod
    def date_to_col_name(date):
        return str(date.day) + str(date.month) + str(date.year)

    @staticmethod
    def today_yesterday_diff(bd):
        corona_collection_today = bd[Calculations.date_to_col_name(
            datetime.date.today() - datetime.timedelta(days=1))]
        corona_collection_yesterday = bd[Calculations.date_to_col_name(
            datetime.date.today() - datetime.timedelta(days=2))]
        sum_today = list(corona_collection_today.aggregate
                         ([{'$group': {'_id': 1, 'all': {'$sum': '$Confirmed'}}}]))[0]['all']
        sum_yesterday = list(corona_collection_yesterday.aggregate
                             ([{'$group': {'_id': 1, 'all': {'$sum': '$Confirmed'}}}]))[0]['all']
        return sum_today-sum_yesterday

    @staticmethod
    def get_weather():  # str
        message = ''
        try:
            resp = Calculations.get_position_weather()
            html_weather = resp['html_text']
            position = resp['position']
        except BaseException:
            return 'Error occurred'
        temperature = ''
        counter = 0
        while html_weather[position + counter] != "<":
            temperature += html_weather[position + counter]
            counter += 1
        position = html_weather.find('<div class="link__condition'
                                     ' day-anchor i-bem" data-bem=') + len(
            '<div class="link__condition day-anchor i-bem" data-bem=')
        fl = False
        condition = ''
        counter = 0
        while html_weather[position + counter] != "<":
            if fl:
                condition += html_weather[position + counter]
            if html_weather[position + counter] == ">":
                fl = True
            counter += 1
        message += 'Температура: ' + temperature + "\n" + condition
        return message

    @staticmethod
    def get_position_weather():
        req = requests.get(
            'https://yandex.ru/pogoda/47?utm_source'
            '=serp&utm_campaign'
            '=wizard&utm_medium=desktop&utm_content='
            'wizard_desktop_main&utm_term=title')
        if req.status_code != 200:
            return None
        html_weather = req.text
        position = html_weather.rfind(
            '<div class="temp fact__temp fact__temp_size_s" role="text">'
            '<span class="temp__pre-a11y a11y-hidden">'
            'Текущая температура</span><span class="temp__value">') + len(
            '<div class="temp fact__temp fact__temp_size_s" role="text">'
            '<span class="temp__pre-a11y a11y-hidden">'
            'Текущая температура</span><span class="temp__value">')
        if position < 0:
            return None
        else:
            return {'html_text': html_weather, 'position': position}

    @staticmethod
    def get_cat_fact():
        try:
            msg = Calculations.fact_selection(pymongo.MongoClient().mongo_bd)
        except BaseException:
            return "Error occurred"
        return f'Fact: \n{msg}'

    @staticmethod
    def fact_selection(bd):
        if not 'cat_facts' in bd.list_collection_names():
            Calculations.cat_database_set_up(bd['cat_facts'])
        return bd['cat_facts'].find_one({'id': int(random() * 20)})['text']

    @staticmethod
    def cat_database_set_up(cat_facts):
        req = requests.get('https://cat-fact.herokuapp.com/facts')
        if req.status_code != 200:
            return 'Error occurred'
        cat_facts.drop()
        json_facts = req.json()
        most_upvoted = sorted(json_facts['all'], key=lambda fact: int(fact['upvotes']), reverse=True)
        counter = 0
        for line in most_upvoted:
            line['id'] = counter
            counter += 1
        cat_facts.insert_many(most_upvoted)

