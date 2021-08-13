from rest_framework import mixins
from rest_framework import viewsets

from api.models import Car
from api.serializers import CarSerializer

class CreateListDestroyCarViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    make = None
    model = None
    lookup_field = 'id'