from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/recent/', views.RecentCarsView.as_view(), name='recent-cars'),
    path('cars/featured/', views.FeaturedCarsView.as_view(), name='featured-cars'),
    path('cars/<slug:slug>/', views.CarDetailView.as_view(), name='car-detail'),
    path('cars/<slug:slug>/related/', views.RelatedCarsView.as_view(), name='related-cars'),
    path("auth/firebase-login/", views.firebase_login, name="firebase_login"),
    path('send-verification/', views.send_verification_email, name='send_verification_email'),
    path('admin/stats/', views.admin_stats_view, name='admin-stats'),
    path('admin/users/', views.admin_users_view, name='admin-users'),
    path('admin/add-car/', views.admin_add_car_view, name='admin-add-car'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', views.profile, name='profile'),
    path("cars/<slug:slug>/related/", views.RelatedCarsView.as_view(), name="related-cars"),

    # path('auth/user/', views.user_view, name='user'),
    # path('api/token/refresh/', views.refresh_token_view, name='cookie_token_refresh'),

]