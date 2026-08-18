from .models import Tenants, Clients
from types import SimpleNamespace
from django.forms.models import model_to_dict
from django.db.models import Q

def get_tenants(
    detail_filters=None,
    select_fields=None,
    where_conditions=None,
    exclude_conditions=None,
    return_type="first"
):
    detail_filters = detail_filters or {}
    where_conditions = where_conditions or {}
    select_fields = select_fields or {}
    exclude_conditions = exclude_conditions or {}

    queryset = Tenants.objects.select_related("details")

    filters = Q()

    # detail_filters
    for field, value in detail_filters.get("tenant", {}).items():
        filters &= Q(**{field: value})

    for field, value in detail_filters.get("tenant_details", {}).items():
        filters &= Q(**{f"details__{field}": value})

    # where_conditions
    for field, value in where_conditions.get("tenant", {}).items():
        if field == "or":
            or_filter = Q()
            for or_field, or_value in value.items():
                or_filter |= Q(**{or_field: or_value})
            filters &= or_filter
        else:
            filters &= Q(**{field: value})

    for field, value in where_conditions.get("tenant_details", {}).items():
        if field == "or":
            or_filter = Q()
            for or_field, or_value in value.items():
                or_filter |= Q(**{f"details__{or_field}": or_value})
            filters &= or_filter
        else:
            filters &= Q(**{f"details__{field}": value})

    queryset = queryset.filter(filters)

    exclude_filters = Q()
    for field, value in exclude_conditions.get("tenant", {}).items():
        exclude_filters |= Q(**{field: value})

    for field, value in exclude_conditions.get("tenant_details", {}).items():
        exclude_filters |= Q(**{f"details__{field}": value})

    if exclude_filters:
        queryset = queryset.exclude(exclude_filters)

    tenant_fields = select_fields.get("tenant", [])
    detail_fields = select_fields.get("tenant_details", [])

    results = []

    for tenant in queryset:

        row = {}

        # If select_fields not provided, return all tenant fields
        if not tenant_fields:
            tenant_fields = [
                field.name
                for field in tenant._meta.fields
            ]

        for field in tenant_fields:
            row[field] = getattr(tenant, field)

        if hasattr(tenant, "details"):

            # If select_fields not provided, return all detail fields
            if not detail_fields:
                detail_fields = [
                    field.name
                    for field in tenant.details._meta.fields
                ]

            for field in detail_fields:
                row[field] = getattr(tenant.details, field)

        results.append(row)

    if return_type == "first":
        return SimpleNamespace(**results[0]) if results else None

    return [SimpleNamespace(**row) for row in results]

def get_tenant_common_object(tenant_obj, tenant_details_obj):
    tenant = model_to_dict(tenant_obj)
    tenant_details = model_to_dict(tenant_details_obj)

    return SimpleNamespace(**{**tenant, **tenant_details})

def get_client_id_by_tenant_id(tenant_id):
    client = Clients.objects.filter(cliTenantId=tenant_id).first()
    if client:
        return client.cliId
    return 0

def get_tenant_id_by_client_id(client_id):
    client = Clients.objects.filter(cliId=client_id).first()
    if client:
        return client.cliTenantId
    return 0

def get_client_timezone(tenant_id):
    try:
        client = Clients.objects.filter(cliTenantId=tenant_id).first()
        if client:
            return client.cliTimeZone or "UTC"
        else:
            return "UTC"
    except Clients.DoesNotExist:
        return "UTC"