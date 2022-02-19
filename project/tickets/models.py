from django.db import models


# Create your models here.
# guest - movie -- reservation

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)
    date = models.DateField()
    def __str__(self):
        return self.movie



class Guest(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)


