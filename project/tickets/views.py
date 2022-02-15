from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation


# Create your views here.

# without rest framework and  without models

def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'hossam',
            'mobile': 123456789
        },
        {
            'id': 1,
            'name': 'yahia',
            'mobile': 9865428
        }
    ]
    return JsonResponse(guests, safe=False)

# without rest framework and from  models
def no_rest_from__model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response, safe=False)
