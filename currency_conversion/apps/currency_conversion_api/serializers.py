from rest_framework import serializers
from currency_conversion.apps.currency_conversion_app.models import CurrencyConversionRating


class CurrencyConversionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConversionRating
        fields = ('currency_date', 'CZK', 'EUR', 'PLN')

