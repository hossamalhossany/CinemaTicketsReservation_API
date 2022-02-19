from django.http.response import JsonResponse, Http404

from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Guest, Movie, Reservation
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
class CBV_list(APIView):
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


# 4.2  GET , PUT , DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)

        except Guest.DoesNotExist:
            raise Http404

    # GET
    def get(self, request, pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    # PUT
    def put(self, request, pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, requst, pk):
        guest = self.get_object(pk=pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 mixins list
class Mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 get , put , delete
class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


# 6 Generics
# 6.1 GET , POST
class Generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 6.2 GET , PUT , DELETE
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# 7 viewset
class ViewSets_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class ViewSets_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ViewSets_Reservations(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8 find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        movie=request.data['movie'],
        hall=request.data['hall']
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        movie=request.data['movie'],
        hall=request.data['hall']
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
