import testtools
import unittest
import unittest.mock as mock
from unittest.mock import patch, call
from unittest.mock import MagicMock


from quasar.campaign_activity import full_backfill, backfill_since, _backfill

class CampaignActivityTest(unittest.TestCase):

    @patch('quasar.campaign_activity._backfill')
    def test_full_backfill(self, mock_backfill):
        full_backfill()
        self.assertEqual(mock_backfill.call_count, 1)

    @patch('quasar.campaign_activity._backfill')
    @patch('quasar.campaign_activity.sys')
    def test_backfill_since(self, mock_sys, mock_backfill):
        mock_sys.argv = ["backfill_since", 3]
        backfill_since()
        mock_backfill.assert_called_once_with(hours=3)


    @patch('quasar.campaign_activity.Scraper')
    @patch('quasar.database.MySQLdb')
    @patch('quasar.campaign_activity._get_start_page')
    @patch('quasar.campaign_activity._get_final_page')
    def test_scraper(self, mock_final_page, mock_start_page, mock_db, mock_scraper):

            mock_scraper.getJson.return_value = {'data': []}
            mock_final_page.return_value = 3
            mock_start_page.return_value = 0

            _backfill()

            self.assertEqual(mock_scraper.return_value.getJson.call_count, 4)

            expected_calls = [
                call('', params={'page':0}),
                call('', params={'page':1}),
                call('', params={'page':2}),
                call('', params={'page':3})
            ]
            mock_scraper.return_value.getJson.assert_has_calls(expected_calls, any_order=True)

# module.py
# import mypackage.MyClass

# def method_to_test:
#     instance = MyClass()
#     instance.some_side_effect_method(1, 2, 3)
#     return None


# test_module.py
# from module import method_to_test
# class MyTest(unittest.TestCase):

#     @mock.patch('module.MyClass')
#     def test_method_to_test(self, mock_class):
#         method_to_test()
#         self.assertEqual(mock_class.call_count, 1)
