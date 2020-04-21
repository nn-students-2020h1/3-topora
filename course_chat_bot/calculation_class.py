import datetime
import requests
import logging
import csv
import os


class Calculations:

    @staticmethod
    def get_msg_for_corona():    # str
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
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
        with open('now.csv', 'wb+') as now:
            now.write(req.content)
        with open('now.csv', 'r') as now:
            now_dict = csv.DictReader(now)
            sort_dictlist = list(now_dict)
            sort_dictlist = sorted(sort_dictlist, key=lambda record: int(
                record['Confirmed']), reverse=True)
        os.remove('now.csv')
        return sort_dictlist

    @staticmethod
    def corona_stats_dynamics():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger(__name__)
        data = datetime.date.today() - datetime.timedelta(days=1)
        date_prev = data-datetime.timedelta(days=1)
        req_yesterday = Calculations.get_corona_data_by_date(date_prev)
        req_today = Calculations.get_corona_data_by_date(data)
        yesterday = Calculations.sum_confirmed(req_yesterday)
        today = Calculations.sum_confirmed(req_today)
        msg = "Со вчерашнего дня заразилось " + str(today-yesterday) + " человек"
        return msg

    @staticmethod
    def sum_confirmed(req: requests.Response):
        sum_conf = 0
        with open('now.csv', 'wb+') as now:
            now.write(req.content)
        with open('now.csv', 'r') as now:
            now_dict = csv.DictReader(now)
            amount = []
            for row in now_dict:
                amount.append(int(row['Confirmed']))
            sum_conf = sum(amount)
        return sum_conf

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
        position = html_weather.find('<div class="link__condition day-anchor i-bem" data-bem=') + len(
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
        r = requests.get('https://cat-fact.herokuapp.com/facts')
        if r.status_code != 200:
            return 'Error occurred'
        try:
            msg = Calculations.fact_parse(r)
        except BaseException:
            return 'Error occurred'
        return f'Fact: \n{msg}'

    @staticmethod
    def fact_parse(req: requests.Response):  # str
        try:
            d = req.json()
            maxv = 0
            for i in range(len(d['all'])):
                if d['all'][i]['upvotes'] >= maxv:
                    maxv = d['all'][i]['upvotes']
                    fact = d['all'][i]['text']
            return fact
        except BaseException:
            return None
