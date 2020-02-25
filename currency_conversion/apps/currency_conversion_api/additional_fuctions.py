from currency_conversion.apps.currency_conversion_app.models import CurrencyConversionRating


def send_notification_to_administrator(exception, var=None):
    """Send notification to administrator"""
    pass


def save_today_cur_conversion(rate):
    """
    Save currency conversion rate in
    currency_conversion.apps.currency_conversion_api.models.CurrencyConversionRating instance

    attributes:
    rate : frozenset = {
            'date' : timestamp,
            'rates': frozenset = {
                'CZK': float(CZK),
                'EUR': float(EUR),
                'PLN': float(PLN),
            }

    return new instance.pk of CurrencyConversionRating or name of exception
    """

    rates = rate['rates']
    try:
        new_rate = CurrencyConversionRating(
            currency_date=rate['date'],
            CZK=rates['CZK'],
            EUR=rates['EUR'],
            PLN=rates['PLN'],
        )
        new_rate.save()
    except KeyError as keyerr:
        send_notification_to_administrator(keyerr, rate)
        return 'KeyError'
    return new_rate.pk
