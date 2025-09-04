# myapp/authentication.py
from firebase_admin import auth as firebase_auth
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return None
        
        try:
            id_token = auth_header.split(" ").pop()
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Firebase ID token")

        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        name = decoded_token.get("name", "")

        from django.contrib.auth import get_user_model
        User = get_user_model()

        user, _ = User.objects.get_or_create(email=email, defaults={"username": uid, "first_name": name.split(" ")[0], "last_name": " ".join(name.split(" ")[1:])})
        
        return (user, None)

