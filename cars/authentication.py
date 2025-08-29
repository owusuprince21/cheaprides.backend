from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to get the JWT from cookies instead of the Authorization header
        access_token = request.COOKIES.get('access_token')
        if access_token is None:
            return None  # No token, DRF will move to the next authentication class

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token
