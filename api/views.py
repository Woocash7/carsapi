import requests
import json
from functools import partial

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

from django.shortcuts import render
from django.http import Http404
from django.db.models import Count

from api.mixins import CreateListDestroyCarViewSet
from api.serializers import CarListSerializer, RateSerializer, PopularCarSerializer
from api.models import Car, Rate


class CarViewSet(CreateListDestroyCarViewSet):
    def list(self, request, *args, **kwargs):
        self.serializer_class = CarListSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.make = request.data['make']
        self.model = request.data['model']

        try:
            if self.check_model_exists():
                car_obj, created = Car.objects.get_or_create(
                    make=self.make,
                    model=self.model
                )
                return self.return_response(
                    {
                        'make': self.make,
                        'model': self.model
                    }, 
                    status.HTTP_201_CREATED
                )
            else:
                return self.return_response("Car does not exists", status.HTTP_404_NOT_FOUND)
        except requests.exceptions.HTTPError:
            return self.return_response("Connection error", status.HTTP_503_SERVICE_UNAVAILABLE)
        except json.decoder.JSONDecodeError:
            return self.return_response("JSON decoding error error", status.HTTP_503_SERVICE_UNAVAILABLE)
        
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return self.return_response("Car has been deleted")
        except Http404:
            return self.return_response("Car does not exist", status.HTTP_404_NOT_FOUND)

    def check_model_exists(self):
        models_for_make_url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{self.make}?format=json'
        results = requests.get(models_for_make_url).json()['Results']
        exists = list(filter(partial(self.search_model), results))
        if exists:
            return True
        else:
            return False

    def search_model(self, model_dict):
        return self.model == model_dict['Model_Name']

    def return_response(self, message=None, status_code=status.HTTP_200_OK):
        return Response(
            {
                'message': message
            },
            status=status_code
        )


class RateCreate(CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = RateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car_id = serializer.data['car_id']

        try:
            car_obj = Car.objects.get(id=car_id)
            Rate.objects.create(
                car=car_obj,
                rating=serializer.data['rating']
            )
            return self.return_response("Rating has been added", status.HTTP_201_CREATED)
        except Car.DoesNotExist:
            return self.return_response("Car does not exist", status.HTTP_404_NOT_FOUND)
    
    def return_response(self, message=None, status_code=status.HTTP_200_OK):
        return Response(
            {
                'message': message
            },
            status=status_code
        )

class PopularCarList(ListAPIView):
    queryset = Car.objects.all().annotate(count=Count('rates')).order_by('-count')
    serializer_class = PopularCarSerializer