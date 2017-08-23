import coreapi
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ParseError

from .models import Schedule


class ScheduleListFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # filter_queryset 이 파라미터로 받는 queryset 은 view 의 get_queryset 메서드에서 반환한 값이다.
        calendar_id = request.query_params.get("calendar_id", None)
        query_user_id = request.query_params.get("user_id", None)

        if calendar_id and not query_user_id:
            return queryset.filter(calendar_id=calendar_id)
        elif not calendar_id and query_user_id:
            user_id = str(request.user.id)
            if query_user_id == user_id:  # 내 달력 조회 = Mapping 에서 request.user 로 필터링 -> 물린 Schedule
                queryset2 = Schedule.objects.filter(mapping__user_id=user_id)
            else:  # 남 달력 조회 = Mapping 에서 query param user_id 로 필터링 + is_public 으로 필터링 -> 물린 Schedule
                queryset2 = Schedule.objects.filter(mapping__user_id=query_user_id).filter(mapping__is_public=True)
            return queryset.intersection(queryset2)
        else:  # 둘 중 하나의 조건만 허용한다.
            raise ParseError()

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(name="year_month", description="Year-Month (yyyy-MM)", required=True, location="query"),
            coreapi.Field(name="calendar_id", description="Calendar ID", required=False, location="query"),
            coreapi.Field(name="user_id", description="User ID", required=False, location="query"),
        ]
        return fields
