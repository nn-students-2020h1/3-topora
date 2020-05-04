import requests
import csv
import datetime


class CoronaBdWork:

    def __init__(self, client):
        self.client = client

    def get_sorted_corona_list(self): #dict
        self.data_check(self.client.mongo_bd,
                        datetime.date.today() - datetime.timedelta(days=1))
        return self._corona_datalist_sort(list(
            self._get_collection_by_date(self.client.mongo_bd, datetime.date.today() -
                                                 datetime.timedelta(days=1)).find()))

    def _get_collection_by_date(self, bd, date):
        return bd[str(date.day) + str(date.month) + str(date.year)]

    def _corona_datalist_sort(self, corona_data: list):
        return sorted(corona_data, key=lambda record: int(
            record['Confirmed']), reverse=True)

    def data_check(self, bd, date):
        if str(date.day) + str(date.month) + str(date.year) in bd.list_collection_names():
            return 1
        else:
            self._corona_data_download(bd, date, self.get_corona_data_by_date(date))

    def _corona_data_download(self, bd, date, corona_data):
        self._corona_data_list_columns_modding(
            list(self._get_corona_data_list_from_req(corona_data)),
            ('Confirmed', 'Deaths', 'Recovered', 'Active'))
        map(self._get_collection_by_date(bd, date).insert_one,
            list(self._get_corona_data_list_from_req(corona_data)))

    def _corona_data_list_columns_modding(self, corona_data_list: list, columns_tuple: tuple):
        return list(map(lambda row: self._corona_data_column_modding(
            row, columns_tuple), corona_data_list))

    def _corona_data_column_modding(self, row: dict, columns_tuple: tuple):
        for column in columns_tuple:
            row[column] = int(row[column])
        return row

    def _get_corona_data_list_from_req(self, corona_data):
        return list(csv.DictReader(corona_data.content.decode(
                'utf-8').splitlines(), delimiter=','))

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