from typing import Any, Dict, List, Optional
import datetime
import calendar
import logging

from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Member
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


def get_start_date_eleven_months_ago(ref_date: datetime.date) -> datetime.date:
    """
    Calculates the date exactly 11 months before the reference date,
    adjusting day of the month appropriately using calendar.monthrange.
    """
    year = ref_date.year
    month = ref_date.month - 11
    while month <= 0:
        month += 12
        year -= 1
    last_day = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, min(ref_date.day, last_day))


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_dashboard_new_users(request: Request) -> CustomResponse:
    """
    GET /dashboard/getDashboardNewUsers
    Fetches the number of new registered users grouped by month for the last 12 months.
    """
    res_body: Dict[str, Any] = {}
    try:
        result_map: Dict[str, int] = {}
        now_date = timezone.now().date()

        # Initialize result map for the last 12 months with 0
        for i in range(11, -1, -1):
            year = now_date.year
            month = now_date.month - i
            while month <= 0:
                month += 12
                year -= 1
            key = f"{year:04d}-{month:02d}"
            result_map[key] = 0

        # Calculate threshold date (11 months ago)
        start_date = get_start_date_eleven_months_ago(now_date)
        start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
        if timezone.is_aware(timezone.now()):
            start_datetime = timezone.make_aware(start_datetime)

        # Query and aggregate using Django ORM with TruncMonth, values, and annotate
        db_results = (
            Member.objects
            .filter(dateRegistered__gte=start_datetime)
            .annotate(year_month=TruncMonth('dateRegistered'))
            .values('year_month')
            .annotate(user_count=Count('memberId'))
            .order_by('year_month')
        )

        for row in db_results:
            dt = row.get('year_month')
            if dt:
                key = dt.strftime('%Y-%m')
                if key in result_map:
                    result_map[key] = int(row.get('user_count') or 0)

        # Construct final sorted list matching Java Response Contract
        final_result: List[Dict[str, Any]] = []
        months_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        for i in range(11, -1, -1):
            year = now_date.year
            month = now_date.month - i
            while month <= 0:
                month += 12
                year -= 1

            key = f"{year:04d}-{month:02d}"
            month_name = months_abbr[month - 1]
            yy = str(year)[-2:]
            label = f"{month_name}-{yy}"

            final_result.append({
                "month": label,
                "newUsers": result_map[key]
            })

        res_body["newUsersList"] = final_result
        return CustomResponse(data=res_body, status=200, message="Get Dashboard New Users fetched successfully.")
    except Exception as ex:
        logger.error(f"GetDashboardNewUsers Error : {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="error")
