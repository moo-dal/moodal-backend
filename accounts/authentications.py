import time

import jwt
from jwt.exceptions import DecodeError
from rest_framework import authentication

from .models import User

TOKEN_SECRET = "temp-secret"  # 배포 환경에서 config.py 등의 파일로 빼내고 VCS 에서 제거할 예정~
TOKEN_EXPIRY_MS = 1000 * 3600 * 3  # 3 hours. 변환해주는 라이브러리가 있으면 좋겠다.


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            payload = jwt.decode(jwt=token, key=TOKEN_SECRET)

            pk = payload.get("id")
            email = payload.get("email")
            name = payload.get("username")
            expiry = payload.get("expiry")

            assert int(time.time() * 1000) < expiry

            user = User(pk=pk, email=email, username=name)

            return user, None
        except DecodeError:
            return None, None
