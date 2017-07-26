from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User

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

