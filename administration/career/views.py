from typing import Any
from django_htmx.http import retarget, reswap
from django.shortcuts import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from administration.views import Is_Counselor
from riasec.models import OfferedProgram
from accounts.models import Program

from .forms import AddCareerQuestionForm, AddOfferedProgramForm

from riasec.models import Question

class CareerView(LoginRequiredMixin, Is_Counselor, ListView):
    model = Question
    template_name = "career/career.html"
    context_object_name = "questions"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = AddCareerQuestionForm()
        return context



class GetQuestions(CareerView):
    template_name = "career/questions.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def add_question(request):
    form = AddCareerQuestionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Created successfully', extra_tags="success")
        return redirect('administration:get-career-questions')
    else:
        messages.warning(request, 'Error', extra_tags="danger")
        return redirect('administration:get-career-questions')

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def update_question(request, pk):
    question = Question.objects.get(id=pk)
    form = AddCareerQuestionForm(request.POST or None, instance=question)
    context = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully', extra_tags="success")
            return redirect('administration:get-career-questions')
        else:   
            messages.warning(request, 'Error', extra_tags="danger")
            return redirect('administration:update-career-question', pk=pk)

    context['form'] = form
    return render(request, "career/partials/form.html", context)

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def delete_question(request):
    if request.is_ajax:
        checkedboxes = request.GET.getlist('checkedboxes[]')
        if checkedboxes:
            Question.objects.filter(id__in=checkedboxes).delete()
            data = messages.success(request, 'Deleted Successfully' , extra_tags='success')
        else:
            data = messages.success(request, 'Please select a question to delete' , extra_tags='danger')

    return JsonResponse(data, safe=False)

class ManageInterestView(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = "career/manage_interest.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["realistic_programs"] = OfferedProgram.objects.filter(interest=OfferedProgram.Interest.REALISTIC)
        context["investigative_programs"] = OfferedProgram.objects.filter(interest=OfferedProgram.Interest.INVESTIGATIVE)
        context["artistic_programs"] = OfferedProgram.objects.filter(interest=OfferedProgram.Interest.ARTISTIC)
        context["social_programs"] = OfferedProgram.objects.filter(interest=OfferedProgram.Interest.SOCIAL)
        context["enterprising_programs"] = OfferedProgram.objects.filter(interest=OfferedProgram.Interest.ENTERPRISING)
        context["conventional_programs"] = OfferedProgram.objects.filter(interest=OfferedProgram.Interest.CONVENTIONAL)
        context['addOfferedProgramForm'] = AddOfferedProgramForm()
        return context

class AddInterest(LoginRequiredMixin, Is_Counselor, TemplateView):
    def get(self, request):
        return super().get(request)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        interest = self.request.POST["interest"]
        program_id = self.request.POST["program"]
        if not program_id == "" and not interest == "":
            program = Program.objects.get(id=int(program_id))
            instance, created = OfferedProgram.objects.get_or_create(interest=interest, program=program)
            context["offeredPrograms"] = OfferedProgram.objects.filter(interest=interest)
            return retarget(render(request, "career/partials/interest_list.html", context), f"#{interest}")
        else:
            print("invalid")
            return reswap(HttpResponse("Invalid"), "none")

class DeleteInterest(LoginRequiredMixin, Is_Counselor, TemplateView):
    def get(self, request):
        return super().get(request)
    
    def post(self, request, *args, **kwargs):
        print("posting...")
        checkedboxes = self.request.POST.getlist("checkedboxes[]")
        print(checkedboxes)
        for checkedbox in checkedboxes:
            splitted_cb = checkedbox.split(":")
            program = Program.objects.get(id=splitted_cb[1])
            OfferedProgram.objects.get(interest=splitted_cb[0], program=program).delete()
        return redirect("administration:manage-interest")