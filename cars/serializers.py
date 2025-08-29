from rest_framework import serializers
from .models import Car, CarImage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id', 'username', 'first_name', 'last_name','email', 'is_staff', 'is_superuser']
        # read_only_fields = ['id', 'is_staff', 'is_superuser']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'caption']

class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'id', 'title', 'slug', 'price', 'main_image', 
            'make', 'model', 'year', 'mileage', 'fuel_type', 
            'transmission', 'condition', 'is_featured'
        ]

class CarDetailSerializer(serializers.ModelSerializer):
    additional_images = CarImageSerializer(many=True, read_only=True)
    features_list = serializers.SerializerMethodField()
    # main_image = serializers.SerializerMethodField() 

    class Meta:
        model = Car
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'main_image',
            'make', 'model', 'year', 'mileage', 'fuel_type', 'transmission',
            'condition', 'color', 'engine_size', 'doors', 'seats',
            'primary_damage', 'keys',  'drive', 'body_style',
            'features', 'features_list', 'additional_images', 'created_at'
        ]

    def get_features_list(self, obj):
        return obj.get_features_list()

class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'title', 'description', 'price', 'main_image',
            'make', 'model', 'year', 'mileage', 'fuel_type', 'transmission',
            'condition', 'color', 'engine_size', 'doors', 'seats',
            'features', 'is_featured', 'is_available'
        ]


