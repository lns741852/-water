from django.urls import path
from . import views

app_name = 'clockInlinebot'
urlpatterns = [
    path('callback', views.callback),
    path('get_location', views.get_location),
    path('get_location_punchout', views.get_location_punchout),
    path('get_location_overin', views.get_location_overin),
    path('get_location_overout', views.get_location_overout),


]
