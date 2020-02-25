import requests
import logging
from django.utils.timezone import pytz
from datetime import datetime
from currency_conversion.celery import celery_app
from currency_conversion.apps.currency_conversion_api.additional_fuctions import \
    send_notification_to_administrator,\
    save_today_cur_conversion
from celery.exceptions import MaxRetriesExceededError

openexchangerates_utc = pytz.timezone('UTC')
logger = logging.getLogger('currency_conversion.apps.currency_conversion_api.tasks')


@celery_app.task(bind=True, default_retry_delay=10 * 60, max_retries=13)
def get_today_cur_conversion(self, url):
    """
    Get current currency conversion rate from https://openexchangerates.org

    attributes:
    url : str
    contain url to invoke api openexchangerates.org

    invoke save_today_cur_conversion(rate)
    rate = frozenset{
        'date' : timestamp,
        'rates': frozenset{
            'CZK': float(CZK),
            'EUR': float(EUR),
            'PLN': float(PLN),
        }

    return new instance.pk of CurrencyConversionRating or name of exception
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_response = response.json()
    except requests.exceptions.HTTPError as exc:
        # MaxRetriesExceededError Exception dont raises, so i did this
        if get_today_cur_conversion.request.retries + 1 == get_today_cur_conversion.max_retries:
            logger.error('''MaxRetriesExceededError: \nmax_retries count={max_retries}, 'JSON:{response}
            '''.format(max_retries=get_today_cur_conversion.max_retries,
                       response=response
                       )
                        )
            send_notification_to_administrator(MaxRetriesExceededError, response)
            return 'MaxRetriesExceededError'
        # MaxRetriesExceededError Exception dont raises, so i did this
        else:
            raise self.retry(exc=exc)

    # Don't work, MaxRetriesExceededError dont raises
    # except MaxRetriesExceededError as max_retries_exception:
    #     send_notification_to_administrator(max_retries_exception, response)
    #     return

    try:
        date = datetime.fromtimestamp(json_response['timestamp']).replace(tzinfo=openexchangerates_utc)
        rates = json_response['rates']
    except KeyError as keyerr:
        logger.error('Key error error occurred: {}\nJSON:\n{}'.format(keyerr, json_response))
        send_notification_to_administrator(keyerr, response)
        return 'KeyError'
    cur_rates = dict({'CZK': rates['CZK'], 'EUR': rates['EUR'], 'PLN': rates['PLN']})
    rate = dict({'date': date, 'rates': cur_rates})
    return save_today_cur_conversion(rate)
