from django.db import models


class CurrencyConversionRating(models.Model):
    """
    Class CurrencyConversionRating

    Attributes:
        date : datetime - date of conversion rate
        CZK : float     - Czech koruna rate
        EUR : float     - Euro rate
        PLN : float     - Polish złoty rate

    all rates represent in USD
    """

    currency_date = models.DateTimeField('rate date', auto_now=False, blank=False, unique=False)  # unique=False
    CZK = models.FloatField('CZK rate', blank=False)
    EUR = models.FloatField('EUR rate', blank=False)
    PLN = models.FloatField('PLN rate', blank=False)

    @staticmethod
    def get_current_rate():
        """
        Return actual currency conversion rating
        The latest CurrencyConversionRating instance by 'currency_date' field

        return newest instance of CurrencyConversionRating
        """

        try:
            actual_rate = (CurrencyConversionRating.objects.latest('currency_date'))
        except CurrencyConversionRating.DoesNotExist:
            actual_rate = ''
        return actual_rate

    def __str__(self):
        return f'pk:{self.pk} \ndate: {self.currency_date}'

    @staticmethod
    def get_actual_date():
        """
        Function to return date of newest currency conversion rate

        return newest date : datetime.date(YYYY, MM, DD)
        """
        actual_rate = CurrencyConversionRating.get_current_rate()
        actual_datetime = actual_rate.currency_date
        actual_date = actual_datetime.date()

        return actual_date

    class Meta:
        verbose_name = 'Currency conversion rating'
        verbose_name_plural = 'Currencies conversion rating'
