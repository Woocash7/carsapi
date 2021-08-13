from rest_framework import serializers

from django.db.models import Avg

from api.models import Car, Rate

class CarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Car
        fields = ('make', 'model')


class CarListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = ('id','make', 'model', 'avg_rating')

    def get_avg_rating(self, obj):
        return obj.rates.all().aggregate(Avg('rating'))['rating__avg']


class RateSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='car.id')

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')

    def validate_rating(self, value):
        if not value in list(range(1,6)):
            raise serializers.ValidationError("Rating must be in range from 1 to 5")
        return value

class PopularCarSerializer(serializers.ModelSerializer):
    rates_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = ('id','make', 'model', 'rates_number')

    def get_rates_number(self, obj):
        return obj.rates.all().count()
