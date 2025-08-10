import django_filters
from .models import Contact

class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr="icontains", label="First name")
    last_name = django_filters.CharFilter(lookup_expr="icontains", label="Last name")
    organization = django_filters.CharFilter(
        field_name="organization__name", lookup_expr="icontains", label="Organization"
    )

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "organization"]
