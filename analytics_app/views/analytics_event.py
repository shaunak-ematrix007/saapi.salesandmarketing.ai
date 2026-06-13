from typing import Any, Dict, List, Optional
import base64
import datetime
from decimal import Decimal, ROUND_HALF_UP
import pymongo
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Userlist, CampaignsEmailSend
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString
from django.conf import settings

# Initialize PyMongo MongoClient using project settings
client: pymongo.MongoClient = pymongo.MongoClient(settings.MONGODB_SETTINGS['uri'])
db: Any = client[settings.MONGODB_SETTINGS['database']]


def parse_dto_date(date_str: Optional[str]) -> Optional[datetime.datetime]:
    """
    Parses date strings with pattern MM/dd/yyyy or other standard ISO patterns.
    """
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None


def get_start_and_end_date(
    filter_type: str,
    start_date_provided: Optional[datetime.datetime],
    end_date_provided: Optional[datetime.datetime]
) -> Dict[str, Optional[int]]:
    """
    Returns start and end millisecond timestamps in UTC based on DateFilterType.
    """
    today = datetime.date.today()

    def to_ms(dt: datetime.datetime) -> int:
        return int(dt.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)

    start_date: Optional[int] = None
    end_date: Optional[int] = None

    if filter_type == "TODAY":
        start_date = to_ms(datetime.datetime.combine(today, datetime.time.min))
        end_date = to_ms(datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time.min))
    elif filter_type == "YESTERDAY":
        start_date = to_ms(datetime.datetime.combine(today - datetime.timedelta(days=1), datetime.time.min))
        end_date = to_ms(datetime.datetime.combine(today, datetime.time.min))
    elif filter_type == "LAST_7_DAYS":
        start_date = to_ms(datetime.datetime.combine(today - datetime.timedelta(days=6), datetime.time.min))
        end_date = to_ms(datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time.min))
    elif filter_type == "LAST_30_DAYS":
        start_date = to_ms(datetime.datetime.combine(today - datetime.timedelta(days=29), datetime.time.min))
        end_date = to_ms(datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time.min))
    elif filter_type == "THIS_MONTH":
        first_day_this_month = today.replace(day=1)
        start_date = to_ms(datetime.datetime.combine(first_day_this_month, datetime.time.min))
        end_date = to_ms(datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time.min))
    elif filter_type == "LAST_MONTH":
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - datetime.timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        start_date = to_ms(datetime.datetime.combine(first_day_last_month, datetime.time.min))
        end_date = to_ms(datetime.datetime.combine(first_day_this_month, datetime.time.min))
    elif filter_type == "CUSTOM":
        if start_date_provided and end_date_provided:
            start_date = int(start_date_provided.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
            end_date = int((end_date_provided + datetime.timedelta(days=1)).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)

    return {"startDate": start_date, "endDate": end_date}


def get_start_date_end_date_list_for_chart(
    filter_type: str,
    start_date_provided: Optional[datetime.datetime],
    end_date_provided: Optional[datetime.datetime]
) -> Dict[str, Dict[str, int]]:
    """
    Returns day-by-day start/end timestamps in local time for chart formatting.
    """
    result: Dict[str, Dict[str, int]] = {}
    today = datetime.datetime.now()
    days = 0

    if filter_type == "TODAY":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        days = 1
    elif filter_type == "YESTERDAY":
        start_date = (today - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        days = 1
    elif filter_type == "LAST_7_DAYS":
        start_date = (today - datetime.timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)
        days = 7
    elif filter_type == "LAST_30_DAYS":
        days = 30
        start_date = (today - datetime.timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif filter_type == "THIS_MONTH":
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today
        days = (end_date - start_date).days + 1
    elif filter_type == "CUSTOM":
        if not start_date_provided or not end_date_provided:
            return result
        start_date = start_date_provided.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date_provided.replace(hour=0, minute=0, second=0, microsecond=0)
        days = (end_date - start_date).days + 1
    else:
        return result

    current_cal = start_date
    for _ in range(days):
        day_start = current_cal.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = current_cal.replace(hour=23, minute=59, second=59, microsecond=999000)

        date_key = day_start.strftime("%m/%d/%Y")
        result[date_key] = {
            "start": int(day_start.timestamp() * 1000),
            "end": int(day_end.timestamp() * 1000)
        }
        current_cal += datetime.timedelta(days=1)

    return result


# MongoDB Repository Translations using pymongo aggregates

def count_distinct_device_ids(website_id: str, from_ts: int, to_ts: int) -> int:
    pipeline = [
        {"$match": {"website_id": website_id, "timestamp": {"$gte": from_ts, "$lt": to_ts}}},
        {"$group": {"_id": "$device_id"}},
        {"$count": "distinctDeviceCount"}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return results[0]["distinctDeviceCount"] if results else 0


def count_total_distinct_sessions(website_id: str, from_ts: int, to_ts: int) -> int:
    pipeline = [
        {"$match": {"website_id": website_id, "timestamp": {"$gte": from_ts, "$lt": to_ts}}},
        {"$group": {"_id": "$session_id"}},
        {"$count": "distinctDeviceCount"}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return results[0]["distinctDeviceCount"] if results else 0


def count_total_distinct_pages(website_id: str, from_ts: int, to_ts: int) -> int:
    pipeline = [
        {"$match": {"website_id": website_id, "timestamp": {"$gte": from_ts, "$lt": to_ts}}},
        {"$group": {"_id": "$page_view_id"}},
        {"$count": "distinctDeviceCount"}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return results[0]["distinctDeviceCount"] if results else 0


def get_all_unique_device_ids(website_id: str, from_ts: Optional[int], to_ts: Optional[int]) -> List[Dict[str, Any]]:
    match_filter: Dict[str, Any] = {"website_id": website_id}
    if from_ts is not None and to_ts is not None:
        match_filter["timestamp"] = {"$gte": from_ts, "$lt": to_ts}
    pipeline = [
        {"$match": match_filter},
        {"$group": {
            "_id": "$device_id",
            "country": {"$first": "$host_data.address.country"},
            "state": {"$first": "$host_data.address.state"},
            "city": {"$first": "$host_data.address.city"}
        }},
        {"$project": {
            "deviceId": "$_id",
            "country": 1,
            "state": 1,
            "city": 1,
            "_id": 0
        }}
    ]
    return list(db.analytics_events.aggregate(pipeline))


def get_all_unique_campaign_ids(website_id: str, from_ts: Optional[int], to_ts: Optional[int]) -> List[str]:
    match_filter: Dict[str, Any] = {"website_id": website_id, "campaign_id": {"$nin": [None, ""]}}
    if from_ts is not None and to_ts is not None:
        match_filter["timestamp"] = {"$gte": from_ts, "$lt": to_ts}
    pipeline = [
        {"$match": match_filter},
        {"$group": {"_id": "$campaign_id"}},
        {"$project": {"campaignId": "$_id", "_id": 0}}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return [r["campaignId"] for r in results if r.get("campaignId")]


def get_all_unique_user_ids(website_id: str, from_ts: Optional[int], to_ts: Optional[int]) -> List[str]:
    match_filter: Dict[str, Any] = {"website_id": website_id, "user_id": {"$nin": [None, "unknown", ""]}}
    if from_ts is not None and to_ts is not None:
        match_filter["timestamp"] = {"$gte": from_ts, "$lt": to_ts}
    pipeline = [
        {"$match": match_filter},
        {"$group": {"_id": "$user_id"}},
        {"$project": {"userId": "$_id", "_id": 0}}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return [r["userId"] for r in results if r.get("userId")]


def get_all_unique_user_ids_for_campaign(website_id: str, campaign_id: str) -> List[str]:
    pipeline = [
        {"$match": {"website_id": website_id, "campaign_id": campaign_id}},
        {"$group": {"_id": "$user_id"}},
        {"$project": {"userId": "$_id", "_id": 0}}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return [r["userId"] for r in results if r.get("userId")]


def get_page_logs_for_session(session_id: str) -> List[Dict[str, Any]]:
    events = list(db.analytics_events.find({"session_id": session_id}).sort("timestamp", 1))
    result: List[Dict[str, Any]] = []
    for event in events:
        logs = event.get("log")
        if not logs:
            continue
        try:
            logs = sorted(logs, key=lambda x: int(x.get("timestamp", 0)))
        except Exception:
            pass
        if not logs:
            continue
        start = int(logs[0].get("timestamp", 0))
        end = int(logs[-1].get("timestamp", 0))
        duration = end - start + 2000
        result.append({
            "pageViewId": event.get("page_view_id"),
            "pageUrl": logs[0].get("page_url"),
            "pageTitle": logs[0].get("page_title"),
            "duration": duration,
            "referrer": event.get("referrer")
        })
    return result


def format_device_host_data(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return {}

    device_info = doc.get("device_info") or {}
    formatted_device_info = {
        "os": device_info.get("os"),
        "browser": device_info.get("browser"),
        "deviceType": device_info.get("device_type") or device_info.get("deviceType"),
        "screenResolution": device_info.get("screen_resolution") or device_info.get("screenResolution")
    }

    host_data = doc.get("host_data") or {}
    address = host_data.get("address") or {}

    formatted_address = {
        "country": address.get("country"),
        "countryFlag": address.get("countryFlag") or address.get("country_flag"),
        "city": address.get("city"),
        "countryCode": address.get("countryCode") or address.get("country_code"),
        "latitude": address.get("latitude"),
        "longitude": address.get("longitude"),
        "state": address.get("state"),
        "stateCode": address.get("stateCode") or address.get("state_code"),
        "layer": address.get("layer")
    }

    tz_info = address.get("timeZone") or address.get("timezone") or {}
    formatted_tz = {
        "currentTime": tz_info.get("currentTime") or tz_info.get("current_time"),
        "code": tz_info.get("code"),
        "utcOffset": tz_info.get("utcOffset") or tz_info.get("utc_offset") or 0,
        "name": tz_info.get("name"),
        "dstOffset": tz_info.get("dstOffset") or tz_info.get("dst_offset") or 0,
        "id": tz_info.get("id")
    }
    formatted_address["timeZone"] = formatted_tz

    geom = address.get("geometry") or {}
    formatted_geom = {
        "type": geom.get("type"),
        "coordinates": geom.get("coordinates") or []
    }
    formatted_address["geometry"] = formatted_geom

    meta = host_data.get("meta") or {}
    formatted_meta = {
        "code": meta.get("code") or 0
    }

    formatted_host_data = {
        "proxy": host_data.get("proxy", False),
        "ip": host_data.get("ip"),
        "meta": formatted_meta,
        "address": formatted_address
    }

    return {
        "deviceInfo": formatted_device_info,
        "hostData": formatted_host_data
    }


def get_host_and_device_data_for_session(session_id: str) -> Dict[str, Any]:
    doc = db.analytics_events.find_one(
        {"session_id": session_id},
        {"device_info": 1, "host_data": 1, "_id": 0}
    )
    return format_device_host_data(doc)


def get_aggregate_sessions(
    id_val: str,
    field: str,
    website_id: str,
    from_ts: int,
    to_ts: int
) -> List[Dict[str, Any]]:
    pipeline = [
        {"$match": {
            field: id_val,
            "website_id": website_id,
            "timestamp": {"$exists": True, "$gte": from_ts, "$lt": to_ts}
        }},
        {"$group": {
            "_id": "$session_id",
            "firstTimestamp": {"$min": "$timestamp"}
        }},
        {"$project": {
            "sessionId": "$_id",
            "firstTimestamp": 1,
            "_id": 0
        }}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    output: List[Dict[str, Any]] = []
    for session in results:
        sess_id = session.get("sessionId")
        output.append({
            "sessionId": sess_id,
            "timestamp": session.get("firstTimestamp"),
            "pageLogs": get_page_logs_for_session(sess_id),
            "deviceHostData": get_host_and_device_data_for_session(sess_id)
        })
    return output


def get_minute_past_data(website_id: str, timestamp: int, call_count: int) -> List[Dict[str, Any]]:
    temp_count = min(call_count, 30)
    start_ts = timestamp - (temp_count * 60 * 1000)
    pipeline = [
        {"$match": {"website_id": website_id, "timestamp": {"$gte": start_ts, "$lt": timestamp}}},
        {"$group": {
            "_id": "$device_id",
            "country": {"$first": "$host_data.address.country"},
            "state": {"$first": "$host_data.address.state"},
            "city": {"$first": "$host_data.address.city"},
            "ip": {"$first": "$host_data.ip"},
            "os": {"$first": "$device_info.os"},
            "browser": {"$first": "$device_info.browser"},
            "deviceType": {"$first": "$device_info.device_type"}
        }},
        {"$project": {
            "deviceId": "$_id",
            "country": 1,
            "state": 1,
            "city": 1,
            "ip": 1,
            "os": 1,
            "browser": 1,
            "deviceType": 1,
            "_id": 0
        }}
    ]
    return list(db.analytics_events.aggregate(pipeline))


def get_page_url_counts_by_website_and_timestamp(website_id: str, from_ts: int, to_ts: int) -> List[Dict[str, Any]]:
    pipeline = [
        {"$match": {"website_id": website_id, "timestamp": {"$gte": from_ts, "$lte": to_ts}}},
        {"$group": {"_id": "$page_url", "count": {"$sum": 1}}},
        {"$project": {"page_url": "$_id", "count": 1, "_id": 0}}
    ]
    results = list(db.analytics_events.aggregate(pipeline))
    return [{"page_url": r.get("page_url"), "count": r.get("count")} for r in results]


def get_country_count_by_device_id(website_id: str, from_ts: int, to_ts: int) -> List[Dict[str, Any]]:
    pipeline = [
        {"$match": {"website_id": website_id, "timestamp": {"$gte": from_ts, "$lte": to_ts}}},
        {"$group": {
            "_id": {
                "country": "$host_data.address.country",
                "countryCode": "$host_data.address.countryCode",
                "deviceId": "$device_id"
            }
        }},
        {"$group": {
            "_id": {
                "country": "$_id.country",
                "countryCode": "$_id.countryCode"
            },
            "deviceCount": {"$sum": 1}
        }},
        {"$project": {
            "fullCountry": "$_id.country",
            "country": "$_id.countryCode",
            "value": "$deviceCount",
            "_id": 0
        }}
    ]
    return list(db.analytics_events.aggregate(pipeline))


# View Endpoints (Strictly Function-Based Views)

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_devices_users_campaigns(request: Request) -> CustomResponse:
    """
    POST /analytics/getDevicesUsersCampaigns
    Retrieve unique device lists, users list, or campaign lists filtered by website and date.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        website_id: str = data.get("websiteId", "")
        filter_type: str = data.get("filterType", "")
        date_filter_type: str = data.get("dateFilterType", "")
        start_date_provided = parse_dto_date(data.get("startDate"))
        end_date_provided = parse_dto_date(data.get("endDate"))

        # In Java: Long finalMemberId = 6L; (hardcoded in controller)
        member_id: int = 6

        date_map = get_start_and_end_date(date_filter_type, start_date_provided, end_date_provided)
        start_date = date_map.get("startDate")
        end_date = date_map.get("endDate")

        results: List[Dict[str, Any]] = []

        if filter_type == "DEVICE":
            unique_device_ids = get_all_unique_device_ids(website_id, start_date, end_date)
            for e in unique_device_ids:
                device_data = dict()
                device_data["value"] = e.get("deviceId")
                country = str(e.get("country") or "")
                state = str(e.get("state") or "")
                city = str(e.get("city") or "")

                name_builder = "Anonymous: "
                if state:
                    name_builder += state + " "
                if city:
                    name_builder += f"({city}), "
                if country:
                    name_builder += country

                # Equivalent to replaceAll(", $", "")
                if name_builder.endswith(", "):
                    name_builder = name_builder[:-2]
                if name_builder.endswith(","):
                    name_builder = name_builder[:-1]

                device_data["name"] = name_builder.strip()
                device_data["type"] = filter_type
                results.append(device_data)

        elif filter_type == "USER":
            unique_user_ids = get_all_unique_user_ids(website_id, start_date, end_date)
            for e in unique_user_ids:
                if not e:
                    continue
                try:
                    # Double base64 decode
                    decoded_once = base64.b64decode(e.encode('utf-8')).decode('utf-8')
                    decoded_twice = base64.b64decode(decoded_once.encode('utf-8')).decode('utf-8')
                    user_id = int(decoded_twice)
                    user = Userlist.objects.get(memberId=member_id, emailId=user_id)
                except Exception:
                    continue
                
                device_data = {
                    "value": e,
                    "name": f"User: {user.firstName or ''} {user.lastName or ''}".strip(),
                    "userId": user.emailId,
                    "groupId": user.groupId,
                    "type": filter_type
                }
                results.append(device_data)

        elif filter_type == "CAMPAIGN":
            unique_campaign_ids = get_all_unique_campaign_ids(website_id, start_date, end_date)
            for e in unique_campaign_ids:
                if not e:
                    continue
                users_data: List[Dict[str, Any]] = []
                unique_user_ids_for_campaign = get_all_unique_user_ids_for_campaign(website_id, e)
                for u in unique_user_ids_for_campaign:
                    if not u:
                        continue
                    try:
                        decoded_once = base64.b64decode(u.encode('utf-8')).decode('utf-8')
                        decoded_twice = base64.b64decode(decoded_once.encode('utf-8')).decode('utf-8')
                        user_id = int(decoded_twice)
                        user = Userlist.objects.get(memberId=member_id, emailId=user_id)
                    except Exception:
                        continue
                    
                    users_data.append({
                        "value": u,
                        "name": f"{user.firstName or ''} {user.lastName or ''}".strip(),
                        "userId": user.emailId,
                        "groupId": user.groupId,
                        "type": "USER"
                    })

                try:
                    # Decrypt campaign send ID
                    camp_send_id = int(DecryptString.setEncDecUser(e, "display", "Y"))
                    campaign_email_send = CampaignsEmailSend.objects.get(id=camp_send_id)
                except Exception:
                    continue

                device_data = {
                    "value": e,
                    "name": f"Campaign: {campaign_email_send.campName}",
                    "type": filter_type,
                    "users": users_data
                }
                results.append(device_data)

        elif filter_type == "ALL":
            # Add USER results
            unique_user_ids = get_all_unique_user_ids(website_id, start_date, end_date)
            for e in unique_user_ids:
                if not e:
                    continue
                try:
                    decoded_once = base64.b64decode(e.encode('utf-8')).decode('utf-8')
                    decoded_twice = base64.b64decode(decoded_once.encode('utf-8')).decode('utf-8')
                    user_id = int(decoded_twice)
                    user = Userlist.objects.get(memberId=member_id, emailId=user_id)
                except Exception:
                    continue

                results.append({
                    "value": e,
                    "name": f"User: {user.firstName or ''} {user.lastName or ''}".strip(),
                    "userId": user.emailId,
                    "groupId": user.groupId,
                    "type": "USER"
                })
            
            # Add DEVICE results
            unique_device_ids = get_all_unique_device_ids(website_id, start_date, end_date)
            for e in unique_device_ids:
                country = str(e.get("country") or "")
                state = str(e.get("state") or "")
                city = str(e.get("city") or "")

                name_builder = "Anonymous: "
                if state:
                    name_builder += state + " "
                if city:
                    name_builder += f"({city}), "
                if country:
                    name_builder += country

                if name_builder.endswith(", "):
                    name_builder = name_builder[:-2]
                if name_builder.endswith(","):
                    name_builder = name_builder[:-1]

                results.append({
                    "value": e.get("deviceId"),
                    "name": name_builder.strip(),
                    "type": "DEVICE"
                })
        else:
            res_body["error"] = "Invalid filter type"

        res_body["list"] = results
        return CustomResponse(data=res_body, status=200, message="Fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_session_page_log_data(request: Request) -> CustomResponse:
    """
    POST /analytics/getSessionPageLogData
    Fetch aggregated session page log data based on ID type (DEVICE, USER, or CAMPAIGN).
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        id_val: str = data.get("id", "")
        website_id: str = data.get("websiteId", "")
        log_data_by: str = data.get("logDataBy", "")
        date_filter_type: str = data.get("dateFilterType", "")
        start_date_provided = parse_dto_date(data.get("startDate"))
        end_date_provided = parse_dto_date(data.get("endDate"))

        if log_data_by == "DEVICE":
            field = "device_id"
        elif log_data_by == "USER":
            field = "user_id"
        elif log_data_by == "CAMPAIGN":
            field = "campaign_id"
        else:
            raise ValueError(f"Invalid dataBy type: {log_data_by}")

        date_map = get_start_and_end_date(date_filter_type, start_date_provided, end_date_provided)
        start_date = date_map.get("startDate") or 0
        end_date = date_map.get("endDate") or 0

        sessions = get_aggregate_sessions(id_val, field, website_id, start_date, end_date)
        res_body["sessionData"] = sessions

        return CustomResponse(data=res_body, status=200, message="Fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request: Request) -> CustomResponse:
    """
    POST /analytics/getDashboardData
    Get metrics cards and chart data for dashboard visualization.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        website_id: str = data.get("websiteId", "")
        date_filter_type: str = data.get("dateFilterType", "")
        start_date_provided = parse_dto_date(data.get("startDate"))
        end_date_provided = parse_dto_date(data.get("endDate"))

        date_map = get_start_and_end_date(date_filter_type, start_date_provided, end_date_provided)
        start_date = date_map.get("startDate") or 0
        end_date = date_map.get("endDate") or 0

        # Calculate card metrics
        visits = count_total_distinct_sessions(website_id, start_date, end_date)
        unique_visitors = count_distinct_device_ids(website_id, start_date, end_date)
        page_views = count_total_distinct_pages(website_id, start_date, end_date)

        page_per_visits = float(page_views) / visits if visits > 0 else 0.0
        page_per_visits_rounded = float(Decimal(str(page_per_visits)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        card_data = {
            "visits": visits,
            "uniqueVisitors": unique_visitors,
            "pageViews": page_views,
            "pagePerVisits": page_per_visits_rounded
        }
        res_body["cardData"] = card_data

        # Calculate day-by-day chart data
        chart_data_list: List[Dict[str, int]] = []
        chart_dates = get_start_date_end_date_list_for_chart(
            date_filter_type, start_date_provided, end_date_provided
        )
        for date_key, timestamps in chart_dates.items():
            device_count = count_distinct_device_ids(website_id, timestamps["start"], timestamps["end"])
            chart_data_list.append({date_key: device_count})

        res_body["chartData"] = chart_data_list

        # Merge page & country data
        page_data_res = get_page_url_counts_by_website_and_timestamp(website_id, start_date, end_date)
        country_data_res = get_country_count_by_device_id(website_id, start_date, end_date)

        res_body["countryData"] = country_data_res
        res_body["pageData"] = page_data_res

        return CustomResponse(data=res_body, status=200, message="Fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_minute_active_users(request: Request) -> CustomResponse:
    """
    POST /analytics/getMinuteActiveUsers
    Get live analytics active users per minute count and geolocation/device summaries.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        website_id: str = data.get("websiteId", "")
        timestamp: int = int(data.get("timeStamp", 0))
        call_count: int = int(data.get("callCount", 0))

        active_users_data = get_minute_past_data(website_id, timestamp, 1)
        res_body["activeUsersCount"] = len(active_users_data)

        active_users_past_data = get_minute_past_data(website_id, timestamp, call_count)
        
        country_map: Dict[str, int] = {}
        state_map: Dict[str, int] = {}
        city_map: Dict[str, int] = {}
        os_map: Dict[str, int] = {}

        for user_data in active_users_past_data:
            country = user_data.get("country") or ""
            state = user_data.get("state") or ""
            city = user_data.get("city") or ""
            os = user_data.get("os") or ""

            country_map[country] = country_map.get(country, 0) + 1
            state_map[state] = state_map.get(state, 0) + 1
            city_map[city] = city_map.get(city, 0) + 1
            os_map[os] = os_map.get(os, 0) + 1

        data_map = {
            "country": country_map,
            "state": state_map,
            "city": city_map,
            "os": os_map
        }
        res_body["activeUsersData"] = data_map

        return CustomResponse(data=res_body, status=200, message="Fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_page_log_data(request: Request) -> CustomResponse:
    """
    POST /analytics/getPageLogData
    Fetch aggregated counts of pages visited.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        website_id: str = data.get("websiteId", "")
        date_filter_type: str = data.get("dateFilterType", "")
        start_date_provided = parse_dto_date(data.get("startDate"))
        end_date_provided = parse_dto_date(data.get("endDate"))

        date_map = get_start_and_end_date(date_filter_type, start_date_provided, end_date_provided)
        start_date = date_map.get("startDate") or 0
        end_date = date_map.get("endDate") or 0

        page_data = get_page_url_counts_by_website_and_timestamp(website_id, start_date, end_date)
        res_body["sessionData"] = {"data": page_data}

        return CustomResponse(data=res_body, status=200, message="Fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country_log_data(request: Request) -> CustomResponse:
    """
    POST /analytics/getCountryLogData
    Fetch aggregated country counts of visiting devices.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        website_id: str = data.get("websiteId", "")
        date_filter_type: str = data.get("dateFilterType", "")
        start_date_provided = parse_dto_date(data.get("startDate"))
        end_date_provided = parse_dto_date(data.get("endDate"))

        date_map = get_start_and_end_date(date_filter_type, start_date_provided, end_date_provided)
        start_date = date_map.get("startDate") or 0
        end_date = date_map.get("endDate") or 0

        country_data = get_country_count_by_device_id(website_id, start_date, end_date)
        res_body["sessionData"] = {"data": country_data}

        return CustomResponse(data=res_body, status=200, message="Fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")
