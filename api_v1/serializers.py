from rest_framework import serializers
from .models import Cities, Countries

## the cities serializers
# we will add this for the json responses
class CountriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Countries
        fields = ['name', 'code']

class CitiesSerializer(serializers.HyperlinkedModelSerializer):
    country = CountriesSerializer(many=False)
    class Meta:
        model = Cities
        fields = ['country', 'name', 'lat', 'lng']


