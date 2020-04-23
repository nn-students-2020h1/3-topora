import unittest
from unittest import mock
from log_class import Logger
import datetime

logger = Logger()


@logger.log_func
def simple_action(update):
    return None


class TestLoggerLogFunc(unittest.TestCase):

    def setUp(self):
        self.update = mock.MagicMock()
        self.update.message.text = 'testing'
        self.update.effective_user.first_name = 'Jack'
        self.update.effective_user.username = "Jack nickname"
        self.update.effective_user.last_name = None

    def test_log_func_text(self):
        simple_action(self.update)
        self.assertEqual(logger.log[0]['message'], 'testing')

    def test_log_func_username(self):
        simple_action(self.update)
        self.assertEqual(logger.log[0]['username'], 'Jack')

    def test_log_func_func_name(self):
        simple_action(self.update)
        self.assertEqual(logger.log[0]['funcname'], 'simple_action')

    def test_log_func_date(self):
        simple_action(self.update)
        self.assertEqual(logger.log[0]['date'][:4],
                         str(datetime.datetime.now().year))

    def test_log_func_except(self):
        self.assertRaises(BaseException, simple_action(self.update))

    def test_history_1(self):
        simple_action(self.update)
        simple_action(self.update)
        simple_action(self.update)
        simple_action(self.update)
        simple_action(self.update)
        self.assertEqual(logger.last_5_history(self.update)
                         .split('\n')[1], 'testing')

    def test_history_2(self):
        logger.log = []
        simple_action(self.update)
        self.assertEqual(len(logger.last_5_history(self.update)
                             .split()), 2)

    def test_history_3(self):
        logger.log = []
        simple_action(self.update)
        self.update_tyler = mock.MagicMock()
        self.update_tyler.message.text = 'nothing'
        self.update_tyler.effective_user.username = 'Tyler Durden'
        self.update_tyler.effective_user.first_name = 'Tyler'
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        self.assertEqual(len(logger.last_5_history(self.update).split()), 2)

    def test_history_4(self):
        logger.log = []
        simple_action(self.update)
        self.update_tyler = mock.MagicMock()
        self.update_tyler.message.text = 'nothing'
        self.update_tyler.effective_user.username = 'Tyler Durden'
        self.update_tyler.effective_user.first_name = 'Tyler'
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        self.assertEqual(len(logger.last_5_history(
            self.update_tyler).split()), 4)

    def test_history_5(self):
        logger.log = []
        simple_action(self.update)
        self.update.effective_user.username = 'Tyler Durden'


if __name__ == '__main__':
    unittest.main()
