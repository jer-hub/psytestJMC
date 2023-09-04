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
from django_htmx.http import trigger_client_event

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

        personalityStatForm = PersonalityStatForm()
        context["personalityStatForm"] = personalityStatForm
        context["personality_count"] = distinct_personality_user_subquery.count()
        personality_avg = PersonalityResult.objects.filter(user_id__in=Subquery(distinct_personality_user_subquery)).aggregate(*personality_avg_Q)
        context["personality_avg"] = personality_avg
        personality_avg_list = list(personality_avg.values())
        context["personality_avg_list"] = personality_avg_list
        context["personality_labels"] = personality_labels

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
        context['iq_count'] = sum(context['iq_avg'])

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

class IQStats(LoginRequiredMixin, Is_Counselor, TemplateView):
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
        data['iq_count'] = sum(data['iq_avg'])
        html = render_block_to_string(self.template_name, 'iq_scripts', data)
        response = HttpResponse(html)
        return response

class PersonalityStats(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = 'statistics/personality-section.html'
    def get(self, request, *args, **kwargs):
        q = parse_keyword_query(self.request.GET)
        personality_avg = PersonalityResult.objects.filter(Q(user_id__in=Subquery(distinct_personality_user_subquery)) & q).aggregate(*personality_avg_Q)
        data = {}
        data["personality_avg"] = personality_avg
        personality_avg_list = list(personality_avg.values())
        data["personality_avg_list"] = personality_avg_list
        data["personality_count"] = PersonalityResult.objects.filter(Q(user_id__in=Subquery(distinct_personality_user_subquery)) & q).count()
        data["personality_labels"] = personality_labels
        html = render_block_to_string(self.template_name, 'personality_script', data)
        response = HttpResponse(html)
        return response

class CareerStats(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = 'statistics/career-section.html'
    def get(self, request, *args, **kwargs):
        q = parse_keyword_query(self.request.GET)
        career_avg = CareerResult.objects.filter(Q(user_id__in=Subquery(distinct_career_user_subquery)) & q).aggregate(*career_avg_Q)
        data = {}
        data["career_avg"] = career_avg
        career_avg_list = list(career_avg.values())
        data["career_avg_list"] = career_avg_list
        data["career_count"] = CareerResult.objects.filter(Q(user_id__in=Subquery(distinct_career_user_subquery)) & q).count()
        data["career_labels"] = career_labels
        html = render_block_to_string(self.template_name, 'career_script', data)
        response = HttpResponse(html)
        return response

def iq_count(request, count):
    html = render_block_to_string("statistics/partials/iq_stat.html", 'iq_count', {
        "iq_count" : count
    })
    response = HttpResponse(html)
    return response