from course_chat_bot.sources.Calc_src.Corona_src import CoronaBdWork
import unittest
from unittest import mock
import mongomock
from datetime import date, timedelta


class TesrCoronaSrc(unittest.TestCase):

    def setUp(self):
        self.client = mongomock.MongoClient()
        self.CBW = CoronaBdWork(self.client)

    def test_get_sorted_corona_list_type(self):
        self.assertIsInstance(self.CBW.get_sorted_corona_list()
                              [0]['Confirmed'], int)

    def test_data_check_1(self):
        weirddate = date(2020, 5, 1)
        self.assertEqual(self.CBW.data_check(self.client.mongo_db,
                                             weirddate), 2)

    def test_data_check_2(self):
        tomorrow = date.today() + timedelta(days=1)
        self.assertEqual(self.CBW.data_check(self.client.mongo_db,
                                             tomorrow), 0)

    def test_today_yesterday_diff_error(self):
        tomorrow = date.today() + timedelta(days=1)
        self.CBW.data_check = mock.MagicMock(return_value=self.
                                             CBW.data_check(
                                                self.client.mongo_db,
                                                tomorrow))
        print(self.CBW.data_check(self.client.mongo_db,
                                  date.today() - timedelta(days=1)))
        self.assertEqual(self.CBW.today_yesterday_diff(), -1)

    def test_today_yesterday_diff_right(self):
        self.assertTrue(self.CBW.today_yesterday_diff() > 0)
