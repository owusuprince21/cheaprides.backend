from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Car, CarImage
from .serializers import CarListSerializer, CarDetailSerializer, UserSerializer
from firebase_admin import auth as firebase_auth
import json
from django.views.decorators.csrf import csrf_exempt


class CarListView(generics.ListAPIView):
    serializer_class = CarListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get_queryset(self):
        return Car.objects.filter(is_available=True)

class RecentCarsView(generics.ListAPIView):
    serializer_class = CarListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get_queryset(self):
        return Car.objects.filter(is_available=True)[:8]

class FeaturedCarsView(generics.ListAPIView):
    serializer_class = CarListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get_queryset(self):
        return Car.objects.filter(is_available=True, is_featured=True)

class CarDetailView(generics.RetrieveAPIView):
    serializer_class = CarDetailSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Car.objects.filter(is_available=True)

class RelatedCarsView(generics.ListAPIView):
    serializer_class = CarListSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get_queryset(self):
        car_slug = self.kwargs.get('slug')
        try:
            car = Car.objects.get(slug=car_slug)
            return Car.objects.filter(
                make=car.make, 
                is_available=True
            ).exclude(id=car.id)[:4]
        except Car.DoesNotExist:
            return Car.objects.none()

@csrf_exempt
def send_verification_email(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        if not email:
            return JsonResponse({"success": False, "error": "Email is required"}, status=400)

        action_code_settings = firebase_auth.ActionCodeSettings(
            url="https://cheaprides.com/",   # your live frontend domain
            handle_code_in_app=True
        )

        link = firebase_auth.generate_email_verification_link(email, action_code_settings)

        send_mail(
            subject="Verify your email",
            message=f"Click this link to verify your account: {link}",
            from_email=None,  # uses EMAIL_HOST_USER
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({"success": True, "message": "Verification email sent."})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
    
        
@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_login(request):
    token = request.data.get("token")
    try:
        decoded = firebase_auth.verify_id_token(token)
        uid = decoded["uid"]
        name = decoded.get("name", "")
        email = decoded.get("email", "")

        return Response({
            "uid": uid,
            "name": name,
            "email": email,
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats_view(request):
    print(f"🔍 Admin stats request from user: {request.user.username}")
    print(f"🔍 User authenticated: {request.user.is_authenticated}")
    print(f"🔍 User is_staff: {request.user.is_staff}")
    print(f"🔍 User is_superuser: {request.user.is_superuser}")
    print(f"🔍 User is_active: {request.user.is_active}")
    
    # Check if user is authenticated first
    if not request.user.is_authenticated:
        print("❌ User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if user has admin privileges
    if not (request.user.is_staff or request.user.is_superuser):
        print(f"❌ Access denied for user: {request.user.username}")
        print(f"❌ is_staff: {request.user.is_staff}, is_superuser: {request.user.is_superuser}")
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    print("✅ Admin access granted - fetching stats")
    
    # Car statistics by brand
    from django.db.models import Count
    car_stats = Car.objects.values('make').annotate(count=Count('id')).order_by('-count')
    
    # User statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = User.objects.filter(is_staff=True).count()
    
    # Car statistics
    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(is_available=True).count()
    featured_cars = Car.objects.filter(is_featured=True).count()
    
    print(f"✅ Returning admin stats successfully")
    return Response({
        'car_stats': car_stats,
        'user_stats': {
            'total': total_users,
            'active': active_users,
            'admins': admin_users
        },
        'car_overview': {
            'total': total_cars,
            'available': available_cars,
            'featured': featured_cars
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users_view(request):
    print(f"🔍 Admin users request from user: {request.user.username}")
    
    if not request.user.is_authenticated:
        print("❌ User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
    if not (request.user.is_staff or request.user.is_superuser):
        print(f"❌ Access denied for user: {request.user.username}")
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    print("✅ Admin users access granted")
    users = User.objects.all().values('id', 'username', 'email', 'is_active', 'is_staff', 'date_joined', 'last_login')
    return Response(list(users))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_add_car_view(request):
    print(f"🔍 Admin add car request from user: {request.user.username}")
    
    if not request.user.is_authenticated:
        print("❌ User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
    if not (request.user.is_staff or request.user.is_superuser):
        print(f"❌ Access denied for user: {request.user.username}")
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    print("✅ Admin add car access granted")
    
    try:
        # Create car instance
        car_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'make': request.data.get('make'),
            'model': request.data.get('model'),
            'year': request.data.get('year'),
            'mileage': request.data.get('mileage'),
            'fuel_type': request.data.get('fuel_type'),
            'transmission': request.data.get('transmission'),
            'condition': request.data.get('condition'),
            'color': request.data.get('color'),
            'engine_size': request.data.get('engine_size'),
            'doors': request.data.get('doors'),
            'seats': request.data.get('seats'),
            'features': request.data.get('features'),
            'is_featured': request.data.get('is_featured') == 'true',
            'is_available': request.data.get('is_available') == 'true',
        }
        
        # Handle main image
        main_image = request.FILES.get('main_image')
        if main_image:
            car_data['main_image'] = main_image
        
        from .serializers import CarCreateSerializer
        serializer = CarCreateSerializer(data=car_data)
        
        if serializer.is_valid():
            car = serializer.save()
            
            # Handle gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for image in gallery_images:
                CarImage.objects.create(
                    car=car,
                    image=image,
                    caption=f"Gallery image for {car.title}"
                )
            
            return Response({
                'message': 'Car added successfully',
                'car_id': car.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'error': f'Failed to add car: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)