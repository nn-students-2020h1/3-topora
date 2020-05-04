import requests
import csv
import datetime


class CoronaBdWork:

    def __init__(self, client):
        self.client = client

    def get_sorted_corona_list(self):  # dict
        if self.data_check(self.client.mongo_bd,
                           datetime.date.today() -
                           datetime.timedelta(days=1)) > 0:
            return self._corona_datalist_sort(list(
                self._get_collection_by_date(self.client.mongo_bd,
                                             datetime.date.today() -
                                             datetime.timedelta(days=1)
                                             ).find()))
        else:
            return 'Error occured'

    def _get_collection_by_date(self, bd, date):
        return bd[str(date.day) + str(date.month) + str(date.year)]

    def _corona_datalist_sort(self, corona_data: list):
        return sorted(corona_data, key=lambda record: int(
            record['Confirmed']), reverse=True)

    def data_check(self, bd, date):
        if str(date.day) + str(date.month) + str(date.year) in \
                bd.list_collection_names():
            return 1
        else:
            try:
                self._corona_data_download(bd, date,
                                           self._get_corona_data_by_date(date))
                return 2
            except BaseException:
                return 0

    def _corona_data_download(self, bd, date, corona_list):
        self._get_collection_by_date(bd, date).insert_many(
            self._corona_data_list_columns_modding(
                corona_list,
                ('Confirmed', 'Deaths', 'Recovered', 'Active')
            )
        )

    def _corona_data_list_columns_modding(self,
                                          corona_data_list: list,
                                          columns_tuple: tuple):
        return list(map(lambda row: self._corona_data_column_modding(
            row, columns_tuple), corona_data_list))

    def _corona_data_column_modding(self, row: dict, columns_tuple: tuple):
        for column in columns_tuple:
            row[column] = int(row[column])
        return row

    def _date_to_col_name(self, date):
        return str(date.day) + str(date.month) + str(date.year)

    def today_yesterday_diff(self):
        bd = self.client.mongo_bd
        if not self.data_check(bd, datetime.date.today() -
                               datetime.timedelta(days=1)) > 0:
            return -1
        if not self.data_check(bd, datetime.date.today() -
                               datetime.timedelta(days=2)) > 0:
            return -1
        corona_collection_today = bd[self._date_to_col_name(
            datetime.date.today() - datetime.timedelta(days=1))]
        corona_collection_yesterday = bd[self._date_to_col_name(
            datetime.date.today() - datetime.timedelta(days=2))]
        sum_today = list(corona_collection_today.aggregate
                         ([{'$group': {'_id': 1, 'all':
                          {'$sum': '$Confirmed'}}}]))[0]['all']
        sum_yesterday = list(corona_collection_yesterday.aggregate
                             ([{'$group': {'_id': 1, 'all':
                              {'$sum': '$Confirmed'}}}]))[0]['all']
        return sum_today-sum_yesterday

    @staticmethod
    def _get_corona_data_by_date(date):  # list
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
            if req.status_code == 200:
                return list(csv.DictReader(req.content.decode(
                    'utf-8').splitlines(), delimiter=','))
            else:
                raise BaseException
        except BaseException:
            return None
