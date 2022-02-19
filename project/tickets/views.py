from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework.views import APIView


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
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)

        # GET
        if request.method == 'GET':
            serializer = GuestSerializer(guest)
            return Response(serializer.data)

        # PUT
        elif request.method == 'PUT':
            serializer = GuestSerializer(guest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # DELETE
        elif request.method == 'DELETE':
            guest.delete()
            return Response(status=status.HTTP_200_OK)

    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 4 CBV Class Based View
# 4.1  list and create == GET and POST
class CBV_lsit(APIView):
    def get(self, request):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
