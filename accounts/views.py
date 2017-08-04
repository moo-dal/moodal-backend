import time

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import User
from .serializers import UserSerializer

TOKEN_SECRET = "temp-secret"  # 배포 환경에서 config.py 등의 파일로 빼내고 VCS 에서 제거할 예정~
TOKEN_EXPIRY_MS = 1000 * 3600 * 3  # 3 hours. 변환해주는 라이브러리가 있으면 좋겠다.


class UserCreate(generics.CreateAPIView):
    """
    새로운 계정을 생성합니다.
    """
    serializer_class = UserSerializer


@api_view(['POST'])
@csrf_exempt
def token_create(request):
    assert "email" in request.POST  # verification 로직은 사실 view 레이어가 아니라 serializer 레이어로 옮기는게 좋음!
    assert "password" in request.POST

    email = request.POST.get("email")
    password = request.POST.get("password")

    user = User.objects.get(email=email)
    assert user.check_password(password)

    payload = {
        "email": email,
        "id": user.pk,
        "expiry": int(time.time() * 1000) + TOKEN_EXPIRY_MS
    }
    token = jwt.encode(payload=payload, key=TOKEN_SECRET).decode("utf-8")
    data = {
        "token": token,
        "id": user.pk
    }

    return JsonResponse(data=data)


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
