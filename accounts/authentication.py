from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
import pdb

class CookieJWTAuthentication(JWTStatelessUserAuthentication):
    def authenticate(self, request):
        cookie_access_token = request.COOKIES.get('access_token')

        if not cookie_access_token:
            return None

        try:
            validated_token = self.get_validated_token(cookie_access_token)
            user = self.get_user(validated_token)
        except InvalidToken:
            return None

        return (user, None)
