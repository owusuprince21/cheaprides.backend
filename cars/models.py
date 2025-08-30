from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from cloudinary.forms import CloudinaryFileField

class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
        ('gas', 'Gas'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('accident', 'Accident'),
        ('damaged', 'Damaged'),
        ('certified', 'Certified Pre-owned'),
    ]

    CAR_BRAND = [
        ('audi', 'AUDI'),
        ('bently', 'BENTLY'),
        ('bmw', 'BMW'),
        ('ford', 'FORD'),
        ('gmc', 'GMC'),
        ('honda', 'HONDA'),
        ('hyundai', 'HYUNDAI'),
        ('jaguar', 'JAGUAR'),
        ('jeep', 'JEEP'),
        ('kia', 'KIA'),
        ('land rover', 'LAND ROVER'),
        ('lexus', 'LEXUS'),
        ('mazda', 'MAZDA'),
        ('mercedes', 'MERCEDES'),
        ('mitsubishi', 'MITSUBISHI'),
        ('nissan', 'NISSAN'),
        ('porsche', 'PORSCHE'),
        ('toyota', 'TOYOTA'),
    ]

    CAR_YEAR = [
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = CloudinaryField('image', folder='cars/images', blank=True, null=True)
    
    # Car specifications
    make = models.CharField(max_length=100, choices=CAR_BRAND)
    model = models.CharField(max_length=100)
    year = models.CharField(max_length=5, choices=CAR_YEAR)
    mileage = models.IntegerField(help_text="Mileage in kilometers")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    color = models.CharField(max_length=50)
    engine_size = models.CharField(max_length=50, blank=True)
    doors = models.IntegerField(default=4)
    seats = models.IntegerField(default=5)
    primary_damage = models.CharField(max_length=100, blank=True, null=True)
    keys = models.BooleanField(default=False, help_text="Does the car come with keys?")
    # cylinders = models.PositiveIntegerField(blank=True, null=True)
    drive = models.CharField(max_length=50, blank=True, null=True)  # e.g., FWD, AWD, RWD
    body_style = models.CharField(max_length=50, blank=True, null=True)  # e.g., SUV, Sedan
    # owner = models.ForeignKey(User, related_name='cars', on_delete=models.CASCADE)
    
    # Additional features
    features = models.TextField(blank=True, help_text="Comma-separated list of features")
    
    # Meta information
    is_featured = models.BooleanField(default=False, help_text="Show in hot sales")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_features_list(self):
        if self.features:
            return [feature.strip() for feature in self.features.split(',')]
        return []

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='additional_images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder='cars/images', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.car.title} - Image"