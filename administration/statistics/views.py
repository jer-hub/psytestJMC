from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Avg,Q, Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from personalityTest.models import Result as PersonalityResult
from riasec.models import Result as CareerResult
from iqtest.models import Result as IQResult
from administration.views import Is_Counselor
from .forms import IQStatForm, PersonalityStatForm, CareerStatForm
import datetime
from django.http import HttpResponse
from render_block import render_block_to_string

User = get_user_model()

career_avg_Q = (
        Avg("realistic"),
        Avg("investigative"),
        Avg("artistic"),
        Avg("social"),
        Avg("enterprising"),
        Avg("conventional"),
    )

personality_avg_Q = (
    Avg("openness"),
    Avg("conscientious"),
    Avg("extroversion"),
    Avg("agreeable"),
    Avg("neurotic"),
)

distinct_iq_result = IQResult.objects.all().distinct("user")
exceptional = distinct_iq_result.filter(Q(result__gte=36) & Q(result__lte=40))
excellent = distinct_iq_result.filter(Q(result__gte=31) & Q(result__lte=35))
verygood = distinct_iq_result.filter(Q(result__gte=25) & Q(result__lte=30))
good = distinct_iq_result.filter(Q(result__gte=19) & Q(result__lte=24))
average = distinct_iq_result.filter(Q(result__gte=15) & Q(result__lte=18))
poor = distinct_iq_result.filter(Q(result__gte=0) & Q(result__lte=14))

distinct_personality_user_subquery = PersonalityResult.objects.order_by('user_id').values('user_id').distinct()
distinct_career_user_subquery = CareerResult.objects.order_by('user_id').values('user_id').distinct()

career_labels = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
personality_labels = ['Openness', 'Conscientious', 'Extroversion', 'Agreeable', 'Neurotic']

class Statistics(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = "statistics/stats.html"
    model = User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        careerStatForm = CareerStatForm()
        context["careerStatForm"] = careerStatForm
        context["career_count"] = distinct_career_user_subquery.count()
        career_avg = CareerResult.objects.filter(user_id__in=Subquery(distinct_career_user_subquery)).aggregate(*career_avg_Q)
        context["career_avg"] = career_avg
        career_avg_list = list(career_avg.values())
        context["career_avg_list"] = career_avg_list
        context["career_labels"] = career_labels
        print(context["career_avg"])

        personalityStatForm = PersonalityStatForm()
        context["personalityStatForm"] = personalityStatForm
        context["personality_count"] = distinct_personality_user_subquery.count()
        personality_avg = PersonalityResult.objects.filter(user_id__in=Subquery(distinct_personality_user_subquery)).aggregate(*personality_avg_Q)
        context["personality_avg"] = personality_avg
        personality_avg_list = list(personality_avg.values())
        context["personality_avg_list"] = personality_avg_list
        context["personality_labels"] = personality_labels
        print(context["personality_avg"])

        iqStatForm = IQStatForm()
        context["iqStatForm"] = iqStatForm
        exceptional = distinct_iq_result.filter(Q(result__gte=36) & Q(result__lte=40)).count()
        excellent = distinct_iq_result.filter(Q(result__gte=31) & Q(result__lte=35)).count()
        verygood = distinct_iq_result.filter(Q(result__gte=25) & Q(result__lte=30)).count()
        good = distinct_iq_result.filter(Q(result__gte=19) & Q(result__lte=24)).count()
        average = distinct_iq_result.filter(Q(result__gte=15) & Q(result__lte=18)).count()
        poor = distinct_iq_result.filter(Q(result__gte=0) & Q(result__lte=14)).count()
        context["iq_exceptional"] = exceptional
        context["iq_excellent"] = excellent
        context["iq_verygood"] = verygood
        context["iq_good"] = good
        context["iq_average"] = average
        context["iq_poor"] = poor
        context['iq_labels'] = IQResult.labelTextChoices.labels
        context['iq_avg'] = [exceptional, excellent, verygood, good, average, poor]

        return context

def iq_parse_keyword_query(keyword_dict):

    q = Q()
    for key, value in keyword_dict.items():
        if value:
            if "start_date" not in key and "end_date" not in key:
                q &= Q(**{"user__"+key: value})
    return q

def parse_keyword_query(keyword_dict):

    q = Q()
    for key, value in keyword_dict.items():
        if value:
            if "start_date" not in key and "end_date" not in key:
                q &= Q(**{"user__profile__"+key: value})
    return q

class IQStats(TemplateView):
    template_name = 'statistics/iq-section.html'

    def get(self, request, *args, **kwargs):
        start_date = None
        end_date = None
        if self.request.GET:
            if (self.request.GET["start_date_year"] and self.request.GET["start_date_month"] and self.request.GET["start_date_day"] and self.request.GET["end_date_year"]) and self.request.GET["end_date_month"] and self.request.GET["end_date_day"]:
                start_date = datetime.date(int(self.request.GET["start_date_year"]), 
                                           int(self.request.GET["start_date_month"]), 
                                           int(self.request.GET["start_date_day"]))
                end_date = datetime.date(int(self.request.GET["end_date_year"]), 
                                           int(self.request.GET["end_date_month"]), 
                                           int(self.request.GET["end_date_day"]))
                
            q = iq_parse_keyword_query(self.request.GET)
            if start_date and end_date:
                get_poor = poor.filter(q & Q(date_created__range=[start_date,end_date]))
                get_average = average.filter(q & Q(date_created__range=[start_date,end_date]))
                get_good = good.filter(q & Q(date_created__range=[start_date,end_date]))
                get_verygood = verygood.filter(q & Q(date_created__range=[start_date,end_date]))
                get_excellent = excellent.filter(q & Q(date_created__range=[start_date,end_date]))
                get_exceptional = exceptional.filter(q & Q(date_created__range=[start_date,end_date]))
            else:
                get_poor = poor.filter(q)
                get_average = average.filter(q)
                get_good = good.filter(q)
                get_verygood = verygood.filter(q)
                get_excellent = excellent.filter(q)
                get_exceptional = exceptional.filter(q)
            
        data = {}
        data['iq_labels'] = IQResult.labelTextChoices.labels
        data['iq_avg'] = [get_exceptional.count(), get_excellent.count(), get_verygood.count(), get_good.count(), get_average.count(), get_poor.count()]
        data['total'] = sum(data['iq_avg'])
        html = render_block_to_string(self.template_name, 'iq_scripts', data)
        response = HttpResponse(html)
        return response

class PersonalityStats(TemplateView):
    template_name = 'statistics/personality-section.html'
    def get(self, request, *args, **kwargs):
        q = parse_keyword_query(self.request.GET)
        personality_avg = PersonalityResult.objects.filter(Q(user_id__in=Subquery(distinct_personality_user_subquery)) & q).aggregate(*personality_avg_Q)
        data = {}
        data["personality_avg"] = personality_avg
        personality_avg_list = list(personality_avg.values())
        data["personality_avg_list"] = personality_avg_list
        data["personality_labels"] = personality_labels
        html = render_block_to_string(self.template_name, 'personality_script', data)
        response = HttpResponse(html)
        return response

class CareerStats(TemplateView):
    template_name = 'statistics/career-section.html'
    def get(self, request, *args, **kwargs):
        q = parse_keyword_query(self.request.GET)
        career_avg = CareerResult.objects.filter(Q(user_id__in=Subquery(distinct_career_user_subquery)) & q).aggregate(*career_avg_Q)
        data = {}
        data["career_avg"] = career_avg
        career_avg_list = list(career_avg.values())
        data["career_avg_list"] = career_avg_list
        data["career_labels"] = career_labels
        html = render_block_to_string(self.template_name, 'career_script', data)
        response = HttpResponse(html)
        return response

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