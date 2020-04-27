import datetime
import requests
import logging
import csv
import pymongo
from random import random

class Calculations:

    @staticmethod
    def get_msg_for_corona():    # str
        date = datetime.date.today() - datetime.timedelta(days=1)
        try:
            req = Calculations.get_corona_data_by_date(date)
            sort_dictlist = Calculations.sort_corona_dict(req)
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
    def sort_corona_dict(req: requests.Response):
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        corona_collection_today = bd.corona_today
        Calculations.data_check(corona_collection_today)
        sort_dictlist = []
        for line in corona_collection_today.find():
            sort_dictlist.append(line)
        sort_dictlist = sorted(sort_dictlist, key=lambda record: int(
            record['Confirmed']), reverse=True)
        return sort_dictlist

    @staticmethod
    def data_check(corona_collection_today):
        corona_file_exists = False
        for line in corona_collection_today.find():
            date_list = {}
            date_list['year'] = (int(line['Last_Update'][:10].split('-')[0]))
            date_list['month'] = (int(line['Last_Update'][:10].split('-')[1]))
            date_list['day'] = (int(line['Last_Update'][:10].split('-')[2]))
            if date_list['year'] == datetime.date.today().year \
                    and date_list['month'] == datetime.date.today().month \
                    and date_list['day'] == datetime.date.today().day:
                corona_file_exists = True
        if not corona_file_exists:
            Calculations.data_download()

    @staticmethod
    def data_download():
        Calculations.copy_today_to_yesterday()
        date = datetime.date.today() - datetime.timedelta(days=1)
        req = Calculations.get_corona_data_by_date(date)
        Calculations.db_corona_write(req)

    @staticmethod
    def copy_today_to_yesterday():
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        corona_collection_yesterday = bd.corona_yesterday
        corona_collection_yesterday.drop()
        corona_collection_today = bd.corona_today
        for line in corona_collection_today.find():
            corona_collection_yesterday.insert_one(line)

    @staticmethod
    def db_corona_write(req: requests.Response):
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        corona_collection_today = bd.corona_today
        corona_collection_today.drop()
        list_regions = list(csv.DictReader(req.content.decode('utf-8').splitlines(), delimiter=','))
        for row in list_regions:
            row['Confirmed'] = int(row['Confirmed'])
        for line in list_regions:
            corona_collection_today.insert_one(line)

    @staticmethod
    def corona_stats_dynamics():
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        corona_collection_today = bd.corona_today
        Calculations.data_check(corona_collection_today)
        msg = "Со вчерашнего дня заразилось " + \
              str(Calculations.today_yesterday_diff()) + " человек"
        return msg

    @staticmethod
    def today_yesterday_diff():
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        corona_collection_today = bd.corona_today
        corona_collection_yesterday = bd.corona_yesterday
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
            msg = Calculations.fact_selection()
        except BaseException:
            return "Error occurred"
        return f'Fact: \n{msg}'

    @staticmethod
    def fact_selection():
        client = pymongo.MongoClient()
        bd = client.mongo_bd
        cat_facts = bd.cat_facts
        numb = int(random()*20)
        record = cat_facts.find_one({'id': numb})
        if not type(record['text']) == str:
            Calculations.cat_database_set_up(cat_facts)
            record = cat_facts.find_one({'id': numb})
        return record['text']

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

