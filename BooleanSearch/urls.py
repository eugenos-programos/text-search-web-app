from django.urls import path

from BooleanSearch import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh_database', views.refresh_database, name='refresh database'),
    path('help', views.help, name='help'),
    path('search', views.search, name='search'),
    path('validate', views.validate, name='validate')
]
