from django.urls import include, path
from . import views

urlpatterns = [
  path('cities/new/', views.addCities),
  path('countries/new/', views.addCountry),
  path('cities/delete/', views.deleteThedoubleCities),


  # The qurey resquests will handel here!



  path('cities/', views.getCities),
  path('countries/', views.getCountries),
  path('coordinates/', views.getCoordinates),
  path('rewrite/', views.rewrite),
]