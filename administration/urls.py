from django.urls import path

from .views import (
    AssignedUsers,
    Home,
    PendingUsers,
    SetSchedule,
    UserDetailView,
    RQuestionsTemplateView,
    PQuestionsTemplateView,
    RQuestionsCreateView,
    PQuestionsCreateView,
    RQuestionsEditView,
    PQuestionsEditView,
    RDeleteQuestions,
    PDeleteQuestions,
    HistorySchedules,
    MissedSchedules,
    ResetSchedule,
    UpcomingSchedules,
    UserDetailUpdate,
    UserManagement,
    UserSchedules,
    approve_user,
    deleteRecord,
    return_user,
    send_msg,
)


app_name='administration'

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('user-management/', UserManagement.as_view(), name='user-management'),
    path('user-management/<int:pk>/update', UserDetailUpdate.as_view(), name='user-detail-update'),
    path('pending-users/', PendingUsers.as_view(), name='pending-users'),
    path('assigned-users/', AssignedUsers.as_view(), name='assigned-users'),
    path('stats/<user>/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<user>/<int:pk>/approve', approve_user, name='approve-user'),
    path('<user>/<int:pk>/return', return_user, name='return-user'),
    path('<int:r_pk>/<r_user>/<int:p_pk>/<p_user>/delete/', deleteRecord, name='delete-record'),
    path('set-schedule/<username>/set-schedule/', SetSchedule.as_view(), name='set-schedule'),
    path('schedules/', UserSchedules.as_view(), name='schedules'),
    path('schedules/missed/', MissedSchedules.as_view(), name='missed-schedules'),
    path('schedules/upcoming/', UpcomingSchedules.as_view(), name='upcoming-schedules'),
    path('schedules/history/', HistorySchedules.as_view(), name='history-schedules'),
    path('schedules/<int:pk>/reset-schedule/', ResetSchedule.as_view(), name='reset-schedule'),
    path('rquestions/', RQuestionsTemplateView.as_view(), name='rquestions'),
    path('pquestions/', PQuestionsTemplateView.as_view(), name='pquestions'),
    path('rquestions/create/riasec/', RQuestionsCreateView.as_view(), name='rquestions_add'),
    path('pquestions/create/personality/', PQuestionsCreateView.as_view(), name='pquestions_add'),
    path('rquestions/<slug:slug>/riasec/edit', RQuestionsEditView.as_view(), name='rquestions_edit'),
    path('pquestions/<slug:slug>/personality/edit', PQuestionsEditView.as_view(), name='pquestions_edit'),
    path('rquestions/<slug:slug>/riasec/delete', RDeleteQuestions.as_view(), name='rquestions_delete'),
    path('pquestions/<slug:slug>/personality/delete', PDeleteQuestions.as_view(), name='pquestions_delete'),
    path('<user>/send-msg', send_msg, name='send-msg'),
]