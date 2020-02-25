from django.test import TestCase
from datetime import datetime
from currency_conversion.apps.currency_conversion_app.models import CurrencyConversionRating
from django.utils.timezone import pytz
from datetime import timedelta


class TestCurrencyConversionRating(TestCase):

    @classmethod
    def setUpTestData(cls):
        loc_utc = pytz.timezone('UTC')
        good_json = {
            'date': datetime(2020, 2, 23, 15, 0, 27).replace(tzinfo=loc_utc),
            'rates': {
                'CZK': 23.10135,
                'EUR': 0.92191,
                'PLN': 3.9528
            }
        }
        rates = good_json['rates']
        good_currency_conversion = CurrencyConversionRating(currency_date=good_json['date'],
                                                            CZK=rates['CZK'],
                                                            EUR=rates['EUR'],
                                                            PLN=rates['PLN']
                                                            )
        good_currency_conversion.save()

    def test___str__(self):
        """Test that str(instance) of CurrencyConversionRating class return
        'pk:{pk} \ndate: {currency_date}' string
        """
        currency_conversion_instance = CurrencyConversionRating.objects.first()
        self.assertEqual(str(currency_conversion_instance),
                         'pk:{pk} \ndate: {currency_date}'.format(pk=currency_conversion_instance.pk,
                                                                  currency_date=currency_conversion_instance.currency_date
                                                                  ),
                         f'''
                         __str__ method of CurrencyConversionRating going wrong
                         {str(currency_conversion_instance)}
                         pk:{currency_conversion_instance.pk} \ndate: {currency_conversion_instance.currency_date}
                         '''
                         )

    def test_current_rate_newest_instance_exists(self):
        """Test that CurrencyConversionRating.current_rate() static method returns newest instance of class
        """
        currency_conversion_instance = CurrencyConversionRating.get_current_rate()
        self.assertIsInstance(currency_conversion_instance, CurrencyConversionRating,
                              '''
                              They are no currency_conversion_instances in database or 
                              current_rate() returned not instance of CurrencyConversionRating class
                              currency_conversion_instance:
                              {}
                              '''.format(currency_conversion_instance)
                              )

        # Adding two more instances where *.currency_date <= currency_conversion_instance.currency_date
        loc_utc = pytz.timezone('UTC')
        json = {
            'date': datetime(2020, 2, 23, 15, 0, 27).replace(tzinfo=loc_utc),
            'rates': {
                'CZK': 23.10135,
                'EUR': 0.92191,
                'PLN': 3.9528
            }
        }
        rates = json['rates']
        bad_pk = []
        for i in range(3):
            more_currency_conversion_instance = CurrencyConversionRating(currency_date=json['date'] - timedelta(days=i),
                                                                         CZK=rates['CZK'],
                                                                         EUR=rates['EUR'],
                                                                         PLN=rates['PLN']
                                                                         )
            more_currency_conversion_instance.save()
            bad_pk.append(more_currency_conversion_instance.pk)

        # After adding more instances in BD repeat current_rate()
        currency_conversion_instance = CurrencyConversionRating.get_current_rate()
        newest_currency_conversion_instance = CurrencyConversionRating.objects.order_by('-currency_date')[0]
        self.assertTrue(currency_conversion_instance.currency_date <= newest_currency_conversion_instance.currency_date,
                        '''
                        Returned instance of current_rate() static method not the newest instance
                        of  CurrencyConversionRating class
                        '''
                        )

    def test_current_rate_instance_not_exists(self):
        CurrencyConversionRating.objects.all().delete()
        currency_conversion_instance = CurrencyConversionRating.get_current_rate()
        self.assertNotIsInstance(currency_conversion_instance, CurrencyConversionRating,
                                 'They are currency_conversion_instances in database'
                                 )
        self.assertEqual(currency_conversion_instance, '',
                         'Returned not empty string, != ""'
                         )
