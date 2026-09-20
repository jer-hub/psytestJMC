from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model

from django_htmx.http import trigger_client_event

from accounts.models import Profile
from riasec.models import Result as CareerResult, Answer as CareerAnswer
from personality_test.models import (
    RecommendedProgram,
    Result as PersonalityResult,
    Answer as PersonalityAnswer,
)

User = get_user_model()


@user_passes_test(lambda u: u.is_superuser)
def approve_user(request, user_pk):
    try:
        profile = Profile.objects.get(user__id=user_pk)
        profile.is_result = True
        profile.save()
    except Exception:
        pass
    subject = "Well done!"
    message = (
        "Your result is now available. Go to the app > Assessment > View Result "
        f"or go directly here http://jmcproject.herokuapp.com/profile/{profile.user.username}/{profile.user.id}/"
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [profile.user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=True)

    messages.success(request, "Approved", extra_tags="success")
    response = HttpResponse("")
    trigger_client_event(response, "alert", {})
    trigger_client_event(response, "btn_approve", {})
    trigger_client_event(response, "pending_result", {})
    return response


@user_passes_test(lambda u: u.is_superuser)
def unapprove_user(request, user_pk):
    try:
        profile = Profile.objects.get(user__id=user_pk)
        profile.is_result = False
        profile.save()
    except Exception:
        pass

    messages.success(request, "Unapproved", extra_tags="success")
    response = HttpResponse("")
    trigger_client_event(response, "alert", {})
    trigger_client_event(response, "btn_approve", {})
    return response


@user_passes_test(lambda u: u.is_superuser)
def delete_career(request, pk):
    user = User.objects.get(pk=pk)

    try:
        r = CareerResult.objects.get(user_id=pk)
        r.delete()
    except CareerResult.DoesNotExist:
        pass

    CareerAnswer.objects.filter(user=user).delete()

    messages.success(request, "Record has been deleted", extra_tags="success")
    return render(request, "userprofile/partials/tab-career.html")


@user_passes_test(lambda u: u.is_superuser)
def delete_personality(request, pk):
    user = User.objects.get(pk=pk)

    try:
        p = PersonalityResult.objects.get(user_id=pk)
        p.delete()
    except PersonalityResult.DoesNotExist:
        pass

    PersonalityAnswer.objects.filter(user=user).delete()
    RecommendedProgram.objects.filter(user=user).delete()

    messages.success(request, "Record has been deleted", extra_tags="success")
    return render(request, "userprofile/partials/tab-personality.html")


@user_passes_test(lambda u: u.is_superuser)
def send_msg(request, username):
    obj = Profile.objects.get(user__username=username)
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [obj.user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=True)
    return redirect("administration:pending-results")


def handle_alert(request):
    return render(request, "administration/partials/alert.html")
