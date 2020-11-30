from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.db.models import F
from .serializers import CitiesSerializer, CountriesSerializer
from .models import Countries, Cities
from clients.models import Client
import json
from django.core.exceptions import ObjectDoesNotExist



@api_view(["POST"])
@csrf_exempt
def rewrite(request):
    with open("json/cities.json", "r", encoding="utf8") as json_file:
        cities = json.load(json_file)
        last = Cities.objects.all().order_by('-name')
        for i in range(len(last)):
            if last[i] != cities[i]:
                print(f"{last[i]} is unfound")
        # print("The length is : ")
        # print(len(cities))
        # print("finded? : ")
        # print(last)
        
        # with open('json/rest.json', 'w', encoding="utf8") as f:
        #     json.dump(restCities, f, ensure_ascii=False)
    return JsonResponse([{"Opned":"Created!"}], safe=False, status=status.HTTP_201_CREATED)



@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAdminUser])
def deleteThedoubleCities(request):
    cities = Cities.objects.all().order_by('-name')
    for city in cities:
        findThe = Cities.objects.filter(name=city.name, country=city.country, lat=city.lat, lng=city.lng)
        if len(findThe) > 1:
            print(city.name + f" => Is doublected---- ({len(findThe)}) times")
            for i in range(len(findThe)-1):
                findThe[i].delete()
                print("deleted!")
        last = Cities.objects.all().count() 
    return JsonResponse([{"finally":last}], safe=False, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAdminUser])
def addCities(request):
    payload = json.loads(request.body)
    for Item in payload:
        add_Cities = Cities.objects.create(
            country=Item["country"],
            name=Item["name"],
            lat=Item["lat"],
            lng=Item["lng"]
        )
    return JsonResponse([{"Message":"Created!"}], safe=False, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAdminUser])
def addCountry(request):
    payload = json.loads(request.body)
    for Item in payload:
        add_county = Countries.objects.create(
            name=Item["name"],
            code=Item["code"]
        )
    return JsonResponse([{"Message":"Created!"}], safe=False, status=status.HTTP_201_CREATED)



@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def getCities(request):
    user = request.user
    # Client checking
    try:
        findClient = Client.objects.get(user=user)
        findClient.requestsNumber += 1
        findClient.save()
        # ?query=String : for the keyword
        # ?max=Int : for the max results
        # ?country=Boolean : for fetching the country 
        limit = 10
        query = request.GET.get('query', None)
        isLimit = request.GET.get('max', None)
        if isLimit is not None:
            limit = int(isLimit)
        isCountry = request.GET.get('country', None)
        data = []
        # start searching
        # this will return the cities that match the query
        find = Cities.objects.filter(name__contains=query)[0:limit]
        # Now we have to see if the country needed for the request
        if isCountry is not None:
            for item in find:
                country = Countries.objects.get(code=item.country)
                data.append({
                    "name": item.name,
                    "lat": float(item.lat),
                    "lng": float(item.lng),
                    "country": {
                        "name": country.name,
                        "code": country.code
                    },
                })
        else:
            for item in find:
                data.append({
                    "name": item.name,
                    "lat": item.lat,
                    "lng": item.lng,
                })
        # Now the data is ready to fetch
        # length for counting the number of results that we found!
        length = find.count()
        # the response will customized before returnet
        response = {
                "response":
                {
                    "length": length,
                    "items": data
                }
            }
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({"err":"unvalid token key"}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return JsonResponse({"err":"Something terrible went wrong"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


# GET THE COUNTRIES!
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def getCountries(request):
    user = request.user
    # Client checking
    try:
        findClient = Client.objects.get(user=user)
        findClient.requestsNumber += 1
        findClient.save()
        # ?query=String : for the keyword
        # ?limit=Int : for the max results
        # ?cities=Boolean : for fetching the cities 
        # ?max_cities=Int
        limit = 10
        citiesLimit = 10
        query = request.GET.get('query', None)
        isLimit = request.GET.get('limit', None)
        maxCities = request.GET.get('max_cities', None)
        isCities = request.GET.get('cities', None)
        if isLimit is not None:
            limit = int(isLimit)
        if maxCities is not None:
            citiesLimit = int(maxCities)
        data = []
        # start searching
        # this will return the countries that match the query
        find = Countries.objects.filter(name__contains=query)[0:limit]
        # Now we have to see if the cities needed for the request
        if isCities is not None:
            for item in find:
                custom = []
                cities = Cities.objects.filter(country__contains=item.code)[0:citiesLimit]
                print(cities)
                for city in cities:
                    custom.append({
                        "name": city.name,
                        "lat": float(city.lat),
                        "lng": float(city.lng),
                    })
                
                data.append({
                    "name": item.name,
                    "code": item.code,
                    "cities": custom,
                })
        else:
            for item in find:
                data.append({
                    "name": item.name,
                    "code":item.code
                })
        # Now the data is ready to fetch
        # length for counting the number of results that we found!
        length = find.count()
        # the response will customized before returnet
        response = {
                "response":
                {
                    "length": length,
                    "items": data
                }
            }
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({"err":"unvalid token key"}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return JsonResponse({"err": "Something terrible went wrong"}, safe=False, status=status.HTTP_400_BAD_REQUEST)



# GET THE COORDINATES!
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def getCoordinates(request):
    user = request.user
    # Client checking
    try:
        findClient = Client.objects.get(user=user)
        findClient.requestsNumber += 1
        findClient.save()
        # ?city=String : for the keyword
        # ?lat=float : for the lat
        # ?lng=float : for the lng
        city = request.GET.get('city', None)
        lat = request.GET.get('lat', None)
        lng = request.GET.get('lng', None)
        data = None
        err = None
        if city is not None:
            cityResult = Cities.objects.filter(name__contains=city)[0:1]
            if cityResult.count() > 0:
                if cityResult is not None:
                    country = Countries.objects.get(code=cityResult[0].country)
                    data = {
                        "name": cityResult[0].name,
                        "lat": cityResult[0].lat,
                        "lng": cityResult[0].lng,
                        "country": {
                            "country": country.name,
                            "code": country.code
                        }
                    }
                else:
                    data = {
                        "err": "Not found"
                    }
            else:
                err= {
                    "err": "city not found"
                }
        elif lat is not None and lng is not None:
            cityResult = Cities.objects.filter(lat=lat, lng=lng)[0:1]
            if cityResult.count() > 0:
                if cityResult is not None:
                    country = Countries.objects.get(code=cityResult[0].country)
                    data = {
                        "name": cityResult[0].name,
                        "lat": cityResult[0].lat,
                        "lng": cityResult[0].lng,
                        "country": {
                            "country": country.name,
                            "code": country.code
                        }
                    }
                else:
                    data = {
                        "err": "Not found"
                    }
            else:
                err= {
                    "err": "city not found"
                }
        else:
            data = {
                    "err": "Not found"
            }
        
        if data is not None:
            response = {
                "response":
                {
                    "results": data
                }
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        elif err is not None:
            response = err
            return JsonResponse(response, safe=False, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"err":"something wrong!"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ObjectDoesNotExist:
        return JsonResponse({"err":"unvalid token key"}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return JsonResponse({"err": "Something terrible went wrong"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
