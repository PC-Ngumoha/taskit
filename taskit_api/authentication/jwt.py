""" Contains code for the implementation of a JWT Authentication Mechanism """
from authentication.models import User
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        auth_items = auth_header.split(' ')

        if len(auth_items) != 2:
            raise AuthenticationFailed("Supplied token is not valid")

        token = auth_items[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms='HS256')
            email = payload.get('email')
            user = User.objects.get(email=email)

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token, please login again")
        except jwt.DecodeError:
            raise AuthenticationFailed("Error decoding token")
        except User.DoesNotExist:
            raise AuthenticationFailed("No existing user for provided token")
