from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lens/', views.lens, name='lens'),
    path('export_csv', views.export_csv, name='export_csv')
]