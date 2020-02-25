from currency_conversion.apps.currency_conversion_app import views
from django.urls import path

app_name = 'currency_conversion_app'
urlpatterns = [
    path('', views.index),
]
