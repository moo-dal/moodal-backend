from rest_framework import generics

from .authentications import JWTAuthentication
from .serializers import ProfileSerializer, TokenSerializer, UserSerializer

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


class ProfileRetrieve(generics.RetrieveAPIView):
    """
    계정 프로필 정보를 조회합니다.
    """
    authentication_classes = (JWTAuthentication, )
    serializer_class = ProfileSerializer

    def get_object(self):
        assert int(self.kwargs.get("user_id")) == self.request.user.pk
        return self.request.user
