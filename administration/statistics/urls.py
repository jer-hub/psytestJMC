from django.urls import path
from .views import (
    Statistics,
    IQStats,
    PersonalityStats,
    CareerStats,
    iq_count,
)

urlpatterns = [
    path('', Statistics.as_view(), name="statistics"),
    path('iq_stats/', IQStats.as_view(), name="iq-stats"),
    path('personality_stats/', PersonalityStats.as_view(), name="personality-stats"),
    path('career_stats/', CareerStats.as_view(), name="career-stats"),
    path('iq_count/<int:count>/', iq_count, name="iq_count"),
]