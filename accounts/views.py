from rest_framework import generics

from .authentications import JWTAuthentication
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
    응답받은 token 을 HTTP Header 에 "Authorization" 을 key 로 넣어서 인증합니다. 
    """
    serializer_class = TokenSerializer


class TokenValidate(generics.RetrieveAPIView):
    """
    토큰을 검증합니다. 올바른 토큰일 경우 유저 정보를 내려줍니다.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = UserSerializer

    def get_object(self):
        user = User.objects.get(pk=self.request.user.pk)
        return user
