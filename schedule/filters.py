import coreapi
from django.utils.translation import ugettext_lazy as _
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ValidationError

from .models import Schedule


class ScheduleListFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):  # 여기서 받는 queryset = view 의 get_queryset 메서드가 넣는다.
        calendar_id = request.query_params.get("calendar_id", None)
        user_id = request.query_params.get("user_id", None)

        if calendar_id and not user_id:  # 특정 공유달력의 일정들을 요청하는 경우는 간단하다.
            return queryset.filter(calendar_id=calendar_id)
        elif not calendar_id and user_id:  # 특정 개인달력의 일정들을 요청하는 경우는 좀 복잡해진다.
            if user_id == str(request.user.id):  # 자신의 개인달력의 일정들을 요청하는 경우는 다 내려준다.
                queryset2 = Schedule.objects.filter(mapping__user_id=user_id)
            else:  # 타인의 개인달력의 일정들을 요청하는 경우에는, is_public 인 일정들만 내려준다.
                queryset2 = Schedule.objects.filter(mapping__user_id=user_id).filter(mapping__is_public=True)
            return queryset.intersection(queryset2)
        else:  # 둘 중 하나의 조건만 허용한다.
            raise ValidationError(detail=_("calendar_id or user_id is required."))

    def get_schema_fields(self, view):  # query parameter 에 대한 swagger UI 는 라이브러리가 자동 생성해주지 않는다.
        fields = [
            coreapi.Field(name="year_month", description="Year-Month (yyyy-MM)", required=True, location="query"),
            coreapi.Field(name="calendar_id", description="Calendar ID", required=False, location="query"),
            coreapi.Field(name="user_id", description="User ID", required=False, location="query"),
        ]
        return fields
