from django.urls import path

from administration.career.views import CareerView, DeleteInterest, GetQuestions, ManageInterestView, AddInterest, add_question, delete_question, update_question


urlpatterns = [
    path('', CareerView.as_view(), name='career'),
    path('manage-interest/', ManageInterestView.as_view(), name='manage-interest'),
    path('add-interest/', AddInterest.as_view(), name='add-interest'),
    path('delete-interest/', DeleteInterest.as_view(), name='delete-interest'),
    path('get-questions/', GetQuestions.as_view(), name='get-career-questions'),
    path('add/question/', add_question, name='add-career-question'),
    path('delete/question/', delete_question, name='delete-career-question'),
    path('update/question/<int:pk>', update_question, name='update-career-question')
]