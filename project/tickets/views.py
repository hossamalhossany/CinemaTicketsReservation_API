from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status,filters
from rest_framework.response import Response

from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer


# Create your views here. hossam at home

# 1 without rest framework and  without models

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


# 2 without rest framework and from  models
def no_rest_from__model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response, safe=False)


# 3 Functions based views
# 3.1  GET and POST
@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 3.2 GET , PUT, DELETE
@api_view()
def ddd():
    pass
