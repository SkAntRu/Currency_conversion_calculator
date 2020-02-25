from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from currency_conversion.apps.currency_conversion_app.models import CurrencyConversionRating
from currency_conversion.apps.currency_conversion_api.serializers import CurrencyConversionRatingSerializer
from django.conf import settings

# import currencies tuple
CURRENCIES = getattr(settings, 'CURRENCIES', None)


@api_view(['GET'])
def get_actual_rate(request):
    """
    Return actual currency conversion rating rate
    """
    actual_rating = CurrencyConversionRating.get_current_rate()
    actual_rating_serializer = CurrencyConversionRatingSerializer(actual_rating)
    return JsonResponse(actual_rating_serializer.data, safe=False)


@api_view(['GET'])
def get_actual_date(request):
    """
    Return Date of newest conversion rating
    """
    actual_date = CurrencyConversionRating.get_actual_date()
    # timestamp_actual_date = actual_date.
    content = {'actual_date': actual_date}
    return JsonResponse(content)


@api_view(['GET'])
def convert_currencies(request, source_currency, final_currency, source_amount):
    """
    Return converted amount in final currency
    """
    try:
        _source_amount = float(source_amount)
    except ValueError:
        error_text = '''Amount of source currency wrong. Should be float, ex: 1.47. Your amount = {}
        '''.format(source_amount).rstrip()

        error_content = {'error_text': error_text}
        return JsonResponse(error_content)
    actual_rating = CurrencyConversionRating.get_current_rate()
    actual_rating_data = model_to_dict(actual_rating, fields=CURRENCIES)
    # add 'USD' rate
    actual_rating_data['USD'] = 1.0
    final_coefficient = actual_rating_data[final_currency] / actual_rating_data[source_currency]
    final_amount = _source_amount * final_coefficient
    content = {'final_amount': round(final_amount, 2)}
    return JsonResponse(content)


@api_view(['GET'])
def test(request, source_currency, final_currency, source_amount):
    print(source_currency, final_currency, source_amount)
    return JsonResponse(source_currency, final_currency, source_amount)
