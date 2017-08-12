import time

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import User
from .serializers import TokenSerializer, UserSerializer

TOKEN_SECRET = "temp-secret"  # 배포 환경에서 config.py 등의 파일로 빼내고 VCS 에서 제거할 예정~
TOKEN_EXPIRY_MS = 1000 * 3600 * 3  # 3 hours. 변환해주는 라이브러리가 있으면 좋겠다.


class UserCreate(generics.CreateAPIView):
    """
    새로운 계정을 생성합니다.
    """
    serializer_class = UserSerializer


class TokenCreate(generics.CreateAPIView):
    """
    계정에 접근할 수 있는 access token 을 생성합니다.
    """
    serializer_class = TokenSerializer


@api_view(['GET'])
def profile_detail(request, user_id):
    """
    주석을 적으면 swagger 가 이를 사용한다.
    """
    assert "HTTP_AUTHORIZATION" in request.META

    token_header = request.META.get("HTTP_AUTHORIZATION")
    token = token_header[len("moodal token="):]
    payload = jwt.decode(jwt=token, key=TOKEN_SECRET)
    assert "email" in payload
    assert "id" in payload
    assert "expiry" in payload
    assert int(user_id) == payload.get("id")

    data = {
        "email": payload.get("email"),
        "id": payload.get("id"),
        "expiry": payload.get("expiry")
    }

    return JsonResponse(data=data)
