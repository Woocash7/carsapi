import json

from django.test import TestCase, Client
from django.shortcuts import reverse
from django.conf import settings

from api.models import Car, Rate

# Create your tests here.

class CarsAPI(TestCase):
    fixtures = ['test_fixtures.yaml'] # test model for settings.SHORTENED_URL_LENGTH = 5
    car_obj = None
    post_car_dict = {
        'make': 'mazda',
        'model': 'Mazda6'
    }
    post_rate_dict = {
        'car_id': 1,
        'rating': 2
    }

    def setUp(self):
        self.car_obj = Car.objects.get(pk=1)

    def test_post_new_car(self):
        c = Client()
        car_count = Car.objects.all().count()
        response = c.post(reverse('api:car-list'), data=self.post_car_dict, follow=True)
        self.assertEqual(car_count+1, Car.objects.all().count())
        self.assertEqual(response.status_code, 201)

    def test_get_car_list(self):
        c = Client()
        response = c.get(reverse('api:car-list'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_car(self):
        c = Client()
        car_count = Car.objects.all().count()
        response = c.delete(reverse('api:car-detail', args=[self.car_obj.id]), follow=True)
        self.assertEqual(car_count-1, Car.objects.all().count())
        self.assertEqual(response.status_code, 200)

    def test_can_not_get_car_detail(self):
        c = Client()
        response = c.get(reverse('api:car-detail', args=[self.car_obj.id]), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_post_rate(self):
        c = Client()
        rate_count = Rate.objects.all().count()
        response = c.post(reverse('api:rate-detail'), data=self.post_rate_dict, follow=True)
        self.assertEqual(rate_count+1, Rate.objects.all().count())
        self.assertEqual(response.status_code, 201)

    def test_can_not_get_rate(self):
        c = Client()
        response = c.get(reverse('api:rate-detail'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_can_not_delete_rate(self):
        c = Client()
        response = c.delete(reverse('api:rate-detail'), follow=True)
        self.assertEqual(response.status_code, 405)

    def test_get_popular_car_list(self):
        c = Client()
        response = c.get(reverse('api:popular-list'), follow=True)
        response_json = response.json()
        self.assertEqual(response_json, sorted(response_json, key=lambda car: car['rates_number'], reverse=True))
        self.assertEqual(response.status_code, 200)