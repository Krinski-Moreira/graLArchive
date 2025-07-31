from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lenses/', views.lenses, name='lenses'),
    path('help/', views.help, name='help'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('export_csv_comp', views.export_csv_comp, name='export_csv_comp'),
    path('download/', views.download, name='download'),
    path('components/', views.components, name='components'),
    path('acknowledgements/', views.acknowledgements, name = "acknowledgements"),
    path('lenses/<str:Name>', views.lensDetailView.as_view(), name='lens_detail')
]