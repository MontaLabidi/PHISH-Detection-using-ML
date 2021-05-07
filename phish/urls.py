from django.conf.urls import url
from django.urls import path

from . import views  # import views so we can use them in urls.

app_name = 'phish'

urlpatterns = [
    url(r'^$', views.index),  # "/store" will call the method "index" in "views.py"
    path('verify/', views.verify, name='verify'),
    path('review/', views.index, name='review')
]
