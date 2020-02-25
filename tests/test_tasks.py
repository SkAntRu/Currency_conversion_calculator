from unittest import TestCase
from currency_conversion.settings import url, appID
from requests.exceptions import HTTPError
from currency_conversion.apps.currency_conversion_api.tasks import get_today_cur_conversion
from currency_conversion.apps.currency_conversion_app.models import CurrencyConversionRating


class TestCeleryTasks(TestCase):

    def setUp(self):
        self.url = url

    def test_get_today_cur_conversion_connection_error(self):
        """Test for get_today_cur_conversion() to catch requests.exceptions.HTTPError
        and Custom celery.exceptions.MaxRetriesExceededError

        if have some HTTP Errors
        firstly func return 'MaxRetriesExceededError' string when max_retries count reached
        secondly raises HTTPError
        """
        # breake url
        wrong_url = self.url + '111'
        with self.assertRaises(HTTPError):
            self.assertEqual(get_today_cur_conversion(url=wrong_url), 'MaxRetriesExceededError',
                             '''Func dont return "MaxRetriesExceededError" string, 
                             so send_notification_to_administrator() have not been called''')

    def test_get_today_cur_conversion_bad_json(self):
        """
        Test for get_today_cur_conversion() to catch KeyError, working with wrong response.json()
        """
        another_url = f'https://openexchangerates.org/api/currencies.json?app_id={appID}'
        self.assertEqual(get_today_cur_conversion(url=another_url), 'KeyError',
                         '''Func dont return "KeyError" string,
                         so send_notification_to_administrator() have not been called'''
                         )

    def test_get_today_cur_conversion_create_new_instance(self):
        """
        Test for get_today_cur_conversion(), must create new instance of CurrencyConversionRating
        """
        new_pk = get_today_cur_conversion(url=self.url)
        new_rate = CurrencyConversionRating.objects.get(pk=new_pk)
        self.assertIsInstance(new_rate, CurrencyConversionRating,
                              'new_rate is not instance of CurrencyConversionRating'
                              )

