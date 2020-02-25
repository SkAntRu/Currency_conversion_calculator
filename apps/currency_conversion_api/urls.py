from currency_conversion.apps.currency_conversion_api import views
from django.urls import path

app_name = 'currency_conversion_api'
urlpatterns = [
    path('rating/', views.get_actual_rate),
    path('date/', views.get_actual_date),
    path('convert_currencies/<str:source_currency>:<str:source_amount>-<str:final_currency>', views.convert_currencies),
]
