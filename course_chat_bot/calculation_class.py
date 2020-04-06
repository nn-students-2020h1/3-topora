import datetime
import requests
import logging
import csv

class calculatons:

    @staticmethod
    def get_corona_dictlist_yesterday():    #returns str
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger(__name__)
        data = datetime.date.today() - datetime.timedelta(days=1)
        mainurl_corona = 'https://raw.github.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        if data.day > 10:
            if data.month >= 10:
                req = requests.get(f'{mainurl_corona}{str(data.month)}-{str(data.day)}-2020.csv')
            else:
                req = requests.get(f'{mainurl_corona}0{str(data.month)}-{str(data.day)}-2020.csv')
        else:
            if data.month > 10:
                req = requests.get(f'{mainurl_corona}{str(data.month)}-0{str(data.day)}-2020.csv')
            else:
                req = requests.get(f'{mainurl_corona}0{str(data.month)}-0{str(data.day)}-2020.csv')
        logger.info(req.status_code)
        with open('now.csv', 'wb+') as now:
            now.write(req.content)
        with open('now.csv', 'r') as now:
            now_dict = csv.DictReader(now)
            sort_dictlist = list(now_dict)
            sort_dictlist = sorted(sort_dictlist, key=lambda record: int(record['Confirmed']), reverse=True)
        msg = 'Топ 5 местностей по зарегистрированным заражениям на сегодня:\n'
        for i in range(0, 5):
            if len((sort_dictlist[i]['Province_State'])) > 0:
                msg += sort_dictlist[i]['Province_State'] + ':'
            msg += sort_dictlist[i]['Country_Region'] + '\n'
        return msg

    @staticmethod
    def corona_stats_dynamics():
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger(__name__)
        data = datetime.date.today() - datetime.timedelta(days=1)
        mainurl_corona = 'https://raw.github.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

        #################################################################################################
        #prev_day
        day=data.day-1
        month=data.month-1
        if day>0:
            if day > 10:
                if data.month >= 10:
                    req1 = requests.get(f'{mainurl_corona}{str(data.month)}-{str(day)}-2020.csv')
                else:
                    req1 = requests.get(f'{mainurl_corona}0{str(data.month)}-{str(day)}-2020.csv')
            else:
                if data.month > 10:
                    req1 = requests.get(f'{mainurl_corona}{str(data.month)}-0{str(day)}-2020.csv')
                else:
                    req1 = requests.get(f'{mainurl_corona}0{str(data.month)}-0{str(day)}-2020.csv')
        else:
            day=30
            if day > 10:
                if month >= 10:
                    req1 = requests.get(f'{mainurl_corona}{str(month)}-{str(day)}-2020.csv')
                else:
                    req1 = requests.get(f'{mainurl_corona}0{str(month)}-{str(day)}-2020.csv')
            else:
                if month > 10:
                    req1 = requests.get(f'{mainurl_corona}{str(month)}-0{str(day)}-2020.csv')
                else:
                    req1 = requests.get(f'{mainurl_corona}0{str(month)}-0{str(day)}-2020.csv')
        logger.info(req1.status_code)
        #################################################################################################
        #today
        if data.day > 10:
            if data.month >= 10:
                req = requests.get(f'{mainurl_corona}{str(data.month)}-{str(data.day)}-2020.csv')
            else:
                req = requests.get(f'{mainurl_corona}0{str(data.month)}-{str(data.day)}-2020.csv')
        else:
            if data.month > 10:
                req = requests.get(f'{mainurl_corona}{str(data.month)}-0{str(data.day)}-2020.csv')
            else:
                req = requests.get(f'{mainurl_corona}0{str(data.month)}-0{str(data.day)}-2020.csv')
        logger.info(req.status_code)
        ##################################################################################################
        today=0
        yesterday=0
        with open('now.csv', 'wb+') as now:
            now.write(req.content)
        with open('yest.csv', 'wb+') as yest:
            yest.write(req1.content)
        with open('now.csv', 'r') as now:
            now_dict = csv.DictReader(now)
            amount=[]
            for row in now_dict:
                amount.append(int(row['Confirmed']))
            today=sum(amount)
        with open('yest.csv', 'r') as yest:
            yest_dict = csv.DictReader(yest)
            amount=[]
            for row in yest_dict:
                amount.append(int(row['Confirmed']))
            yesterday=sum(amount)
        msg="Со вчерашнего дня заразилось " + str(today-yesterday) + " человек"
        return msg


    @staticmethod
    def get_weather(): #returns str
        message = ''
        r = requests.get(
            'https://yandex.ru/pogoda/47?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content=wizard_desktop_main&utm_term=title')
        d = r.text
        position = d.rfind(
            '<div class="temp fact__temp fact__temp_size_s" role="text"><span class="temp__pre-a11y a11y-hidden">Текущая температура</span><span class="temp__value">') + len(
            '<div class="temp fact__temp fact__temp_size_s" role="text"><span class="temp__pre-a11y a11y-hidden">Текущая температура</span><span class="temp__value">')
        temperature = ''
        i = 0
        while d[position + i] != "<":
            temperature += d[position + i]
            i += 1
        position = d.find('<div class="link__condition day-anchor i-bem" data-bem=') + len(
            '<div class="link__condition day-anchor i-bem" data-bem=')
        fl = False
        condition = ''
        i = 0
        while d[position + i] != "<":
            if fl:
                condition += d[position + i]
            if d[position + i] == ">":
                fl = True
            i += 1
        message += 'Температура: ' + temperature + "\n" + condition
        return message

    @staticmethod
    def get_cat_fact():
        r = requests.get('https://cat-fact.herokuapp.com/facts')
        d = r.json()
        maxv = 0
        for i in range(len(d['all'])):
            if d['all'][i]['upvotes'] >= maxv:
                maxv = d['all'][i]['upvotes']
                fact = d['all'][i]['text']
        return f'Fact: \n{fact}'