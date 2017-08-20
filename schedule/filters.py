import coreapi
from rest_framework.filters import BaseFilterBackend


class ScheduleListFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # calendar_id = request.query_params.get("calendar_id", None)
        # user_id = request.query_params.get("user_id", None)
        #
        # if calendar_id is not None:
        #     queryset = queryset.filter(calendar_id=calendar_id)
        # if user_id is not None:
        #     queryset = queryset.filter()
        #     queryset |= Schedule.objects.filter(user_id=user_id)

        return queryset

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(name="year_month", description="Year-Month (yyyy-MM)", required=True, location="query"),
            coreapi.Field(name="calendar_id", description="Calendar ID", required=False, location="query"),
            coreapi.Field(name="user_id", description="User ID", required=False, location="query"),
        ]
        return fields
