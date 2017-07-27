import time

from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import jwt

from .models import User

TOKEN_SECRET = "temp-secret"  # 배포 환경에서 config.py 등의 파일로 빼내고 VCS 에서 제거할 예정~
TOKEN_EXPIRY_MS = 1000 * 3600 * 3  # 3 hours. 변환해주는 라이브러리가 있으면 좋겠다.

# Create your views here.


@csrf_exempt
def user_create(request):
    assert request.method == "POST"
    assert "email" in request.POST  # verification 로직은 사실 view 레이어가 아니라 serializer 레이어로 옮기는게 좋음!
    assert "password" in request.POST

    email = request.POST.get("email")
    password = request.POST.get("password")

    user = User()
    user.email = email
    user.set_password(password)  # user.password = password 로 바로 assign 하면 raw password 가 그대로 저장되어버린다.
    user.username = email  # Django 에서 username 컬럼이 UNIQUE constraint -> IntegrityError 를 피하기 위한 임시방편!
    user.save()

    data = {
        "id": user.pk
    }

    return JsonResponse(data=data)


@csrf_exempt
def token_create(request):
    assert request.method == "POST"
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


def get_profile(request, user_id):
    assert request.method == "GET"
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
