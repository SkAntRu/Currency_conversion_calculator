from django.shortcuts import render


def index(request):
    """
    HTTPResponse to currency_conversion_calculator.html
    """
    return render(request, 'currency_conversion_api/currency_conversion_calculator.html')