from django.urls import path
from . import views

app_name = 'diversion'

urlpatterns = [
    path('', views.home, name='home'),
    path('page-one/', views.page_one, name='page_one'),
    path('page-two/', views.page_two, name='page_two'),
] 