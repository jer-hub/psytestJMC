from django.contrib.auth import get_user_model
from django import forms
from django.db.models import Q

import django_filters
from django_filters import DateFilter, CharFilter

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    username = CharFilter(
        method="user_filter",
        label="User",
        widget=forms.TextInput(
            attrs={
                "class": "form-control admin-users-search",
                "placeholder": "Search name, username, or email",
                "aria-label": "Search users",
            }
        ),
    )
    date_joined = DateFilter(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    start_date = DateFilter(
        field_name="date_joined",
        lookup_expr="gte",
        label="Joined from",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    end_date = DateFilter(
        field_name="date_joined",
        lookup_expr="lte",
        label="Joined until",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "last_name",
            "first_name",
            "is_superuser",
            "date_joined",
            "email",
        ]

    def user_filter(self, queryset, name, value):
        for term in value.split():
            queryset = queryset.filter(
                Q(first_name__icontains=term)
                | Q(last_name__icontains=term)
                | Q(username__icontains=term)
                | Q(email__icontains=term)
            )
            return queryset
