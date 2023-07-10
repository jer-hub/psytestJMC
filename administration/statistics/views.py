from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Avg,Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from personalityTest.models import Result as PersonalityResult
from riasec.models import Result as CareerResult
from iqtest.models import Result as IQResult
from administration.views import Is_Counselor
from .forms import IQStatForm

User = get_user_model()

riasec_avg = (
        Avg("realistic"),
        Avg("investigative"),
        Avg("artistic"),
        Avg("social"),
        Avg("enterprising"),
        Avg("conventional"),
    )

personality_avg = (
    Avg("openness"),
    Avg("conscientious"),
    Avg("extroversion"),
    Avg("agreeable"),
    Avg("neurotic"),
)

distinct_iq_result = IQResult.objects.all().distinct("user")
exceptional = Count("result", filter=Q(result__gte=36) & Q(result__lte=40))
excellent = Count("result", filter=Q(result__gte=31) & Q(result__lte=35))
verygood = Count("result", filter=Q(result__gte=25) & Q(result__lte=30))
good = Count("result", filter=Q(result__gte=19) & Q(result__lte=24))
average = Count("result", filter=Q(result__gte=15) & Q(result__lte=18))
poor = Count("result", filter=Q(result__gte=0) & Q(result__lte=14))
iq_result = distinct_iq_result.annotate()



career_labels = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
personality_labels = ['Openness', 'Conscientious', 'Extroversion', 'Agreeable', 'Neurotic']

class Statistics(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = "statistics/stats.html"
    model = User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["riasec_male"] = CareerResult.objects.filter(user__profile__sex="Male").aggregate(*riasec_avg)
        context["riasec_female"] = CareerResult.objects.filter(user__profile__sex="Female").aggregate(*riasec_avg)
        context["riasec_college"] = CareerResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*riasec_avg)
        context["riasec_grade"] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*riasec_avg)
        context["riasec_junior"] = CareerResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*riasec_avg)
        context["riasec_senior"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*riasec_avg)
        context["rm_count"] = CareerResult.objects.filter(user__profile__sex="Male").count()
        context["rf_count"] = CareerResult.objects.filter(user__profile__sex="Female").count()
        context["career_college_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="College").count()
        context["career_senior_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").count()
        context["career_junior_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").count()
        context["career_grade_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").count()

        context["personality_male"] = PersonalityResult.objects.filter(user__profile__sex="Male").aggregate(*personality_avg)
        context["personality_female"] = PersonalityResult.objects.filter(user__profile__sex="Female").aggregate(*personality_avg)
        context["personality_college"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*personality_avg)
        context["personality_senior"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*personality_avg)
        context["personality_junior"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*personality_avg)
        context["personality_grade"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*personality_avg)
        context["pm_count"] = PersonalityResult.objects.filter(user__profile__sex="Male").count()
        context["pf_count"] = PersonalityResult.objects.filter(user__profile__sex="Female").count()
        context["personality_college_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").count()
        context["personality_senior_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").count()
        context["personality_junior_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").count()
        context["personality_grade_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").count()
        
        iqStatForm = IQStatForm()
        context["iqStatForm"] = iqStatForm

        return context

class IQStats(TemplateView):
    template_name = 'statistics/iq_stat.html'

    def get(self, request, *args, **kwargs):
        info = self.request.GET
        print(info)
        # print(IQStatForm(info or None))
        exceptional = distinct_iq_result.filter(Q(result__gte=36) & Q(result__lte=40)).count()
        excellent = distinct_iq_result.filter(Q(result__gte=31) & Q(result__lte=35)).count()
        verygood = distinct_iq_result.filter(Q(result__gte=25) & Q(result__lte=30)).count()
        good = distinct_iq_result.filter(Q(result__gte=19) & Q(result__lte=24)).count()
        average = distinct_iq_result.filter(Q(result__gte=15) & Q(result__lte=18)).count()
        poor = distinct_iq_result.filter(Q(result__gte=0) & Q(result__lte=14)).count()
        data = {}
        data['labels'] = IQResult.labelTextChoices.labels
        data['avg'] = [exceptional, excellent, verygood, good, average, poor]
        data['total'] = IQResult.objects.all().count()
        return JsonResponse(data)


@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_male(request):
    data ={}
    data['labels'] = career_labels
    data['avg'] = CareerResult.objects.filter(user__profile__sex="Male").aggregate(*riasec_avg)
    return JsonResponse(data)


@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_female(request):
    data ={}
    data['labels'] = career_labels
    data['avg'] = CareerResult.objects.filter(user__profile__sex="Female").aggregate(*riasec_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_college(request):
    data ={}
    data['labels'] = career_labels
    data['avg'] = CareerResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*riasec_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_senior(request):
    data ={}
    data['labels'] = career_labels
    data['avg'] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*riasec_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_junior(request):
    data ={}
    data['labels'] = career_labels
    data['avg'] = CareerResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*riasec_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_grade(request):
    data ={}
    data['labels'] = career_labels
    data['avg'] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*riasec_avg)
    return JsonResponse(data)



@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_male(request):
    data ={}
    data['labels'] = personality_labels
    data['avg'] = PersonalityResult.objects.filter(user__profile__sex="Male").aggregate(*personality_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_female(request):
    data ={}
    data['labels'] = personality_labels
    data['avg'] = PersonalityResult.objects.filter(user__profile__sex="Female").aggregate(*personality_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_college(request):
    data ={}
    data['labels'] = personality_labels
    data['avg'] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*personality_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_senior(request):
    data ={}
    data['labels'] = personality_labels
    data['avg'] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*personality_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_junior(request):
    data ={}
    data['labels'] = personality_labels
    data['avg'] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*personality_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_grade(request):
    data ={}
    data['labels'] = personality_labels
    data['avg'] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*personality_avg)
    return JsonResponse(data)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def career_category(request):
    category = request.GET['career_category']
    context = {}
    
    if category == '1':
        context["riasec_male"] = CareerResult.objects.filter(user__profile__sex="Male").aggregate(*riasec_avg)
        context["riasec_female"] = CareerResult.objects.filter(user__profile__sex="Female").aggregate(*riasec_avg)
        context["riasec_college"] = CareerResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*riasec_avg)
        context["riasec_grade"] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*riasec_avg)
        context["riasec_junior"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*riasec_avg)
        context["riasec_senior"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*riasec_avg)
        context["rm_count"] = CareerResult.objects.filter(user__profile__sex="Male").count()
        context["rf_count"] = CareerResult.objects.filter(user__profile__sex="Female").count()
        context["career_college_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="College").count()
        context["career_senior_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").count()
        context["career_junior_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").count()
        context["career_grade_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").count()
        return render(request, 'statistics/partials/career_all.html', context)

    elif category == '2':
        context["rm_count"] = CareerResult.objects.filter(user__profile__sex="Male").count()
        context["rf_count"] = CareerResult.objects.filter(user__profile__sex="Female").count()
        context["riasec_male"] = CareerResult.objects.filter(user__profile__sex="Male").aggregate(*riasec_avg)
        context["riasec_female"] = CareerResult.objects.filter(user__profile__sex="Female").aggregate(*riasec_avg)
        return render(request, 'statistics/partials/career_sex.html', context)

    elif category == '3':
        context["riasec_college"] = CareerResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*riasec_avg)
        context["career_college_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="College").count()
        return render(request, 'statistics/partials/career_college.html', context)

    elif category == '4':
        context["riasec_senior"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*riasec_avg)
        context["career_senior_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").count()
        return render(request, 'statistics/partials/career_senior.html', context)

    elif category == '5':
        context["riasec_junior"] = CareerResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*riasec_avg)
        context["career_junior_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").count()
        return render(request, 'statistics/partials/career_junior.html', context)

    elif category == '6':
        context["riasec_grade"] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*riasec_avg)
        context["career_grade_count"] = CareerResult.objects.filter(user__profile__educationlevel__name="Grade School").count()
        return render(request, 'statistics/partials/career_grade.html', context)

    return HttpResponse('')

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
@require_http_methods(["GET"])
def personality_category(request):
    category = request.GET['personality_category']
    context = {}
    
    if category == '1':
        context["personality_male"] = PersonalityResult.objects.filter(user__profile__sex="Male").aggregate(*personality_avg)
        context["personality_female"] = PersonalityResult.objects.filter(user__profile__sex="Female").aggregate(*personality_avg)
        context["personality_college"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*personality_avg)
        context["personality_senior"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*personality_avg)
        context["personality_junior"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*personality_avg)
        context["personality_grade"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*personality_avg)
        context["pm_count"] = PersonalityResult.objects.filter(user__profile__sex="Male").count()
        context["pf_count"] = PersonalityResult.objects.filter(user__profile__sex="Female").count()
        context["personality_college_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").count()
        context["personality_senior_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").count()
        context["personality_junior_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").count()
        context["personality_grade_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").count()
        return render(request, 'statistics/partials/personality_all.html', context)

    elif category == '2':
        context["pm_count"] = PersonalityResult.objects.filter(user__profile__sex="Male").count()
        context["pf_count"] = PersonalityResult.objects.filter(user__profile__sex="Female").count()
        context["personality_male"] = PersonalityResult.objects.filter(user__profile__sex="Male").aggregate(*personality_avg)
        context["personality_female"] = PersonalityResult.objects.filter(user__profile__sex="Female").aggregate(*personality_avg)
        return render(request, 'statistics/partials/personality_sex.html', context)

    elif category == '3':
        context["personality_college"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").aggregate(*personality_avg)
        context["personality_college_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="College").count()
        return render(request, 'statistics/partials/personality_college.html', context)

    elif category == '4':
        context["personality_senior"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").aggregate(*personality_avg)
        context["personality_senior_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Senior Highschool").count()
        return render(request, 'statistics/partials/personality_senior.html', context)

    elif category == '5':
        context["personality_junior"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").aggregate(*personality_avg)
        context["personality_junior_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Junior Highschool").count()
        return render(request, 'statistics/partials/personality_junior.html', context)

    elif category == '6':
        context["personality_grade"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").aggregate(*personality_avg)
        context["personality_grade_count"] = PersonalityResult.objects.filter(user__profile__educationlevel__name="Grade School").count()
        return render(request, 'statistics/partials/personality_grade.html', context)

    return HttpResponse('')