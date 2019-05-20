from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import  DetailView
from .models import Survey, Answer, Response
from django.http import Http404, HttpResponse
from lazysignup.decorators import allow_lazy_user
from django.contrib.auth.decorators import user_passes_test


def clear_session(request):
    request.session.clear()
    return redirect('home')


@allow_lazy_user
def home(request):
    if request.user.is_superuser:
        return redirect('admin_home')
    else:
        surveys = Survey.objects.filter(active=True)
        if surveys.exists():
            return redirect('survey_detail', surveys.first().slug)
        else:
            return render(request, 'portal/home.html', {'surveys': surveys})
        # surveys = Survey.objects.active()
        # return render(request, 'portal/home.html', {'surveys': surveys})


class SurveyDetailView(DetailView):
    template_name = 'portal/survey_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'survey'

    model = Survey

    def get_object(self, queryset=None):
        survey = super().get_object(queryset=queryset)
        if not survey.active:
            raise Http404('Invalid Request')
        return survey


@allow_lazy_user
def survey_start(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    if survey.has_questions:
        if request.method == "POST":
            post_dict = request.POST
            response = Response.objects.get_or_create(user=request.user, survey=survey, user_feedback=post_dict['feedback'])[0]
            Answer.objects.bulk_create([Answer(question_id=int(choice[7:]), choice_id=int(post_dict[choice]), response=response) for choice in post_dict if 'choice_' in choice])
            return redirect('survey_submitted')
        else:
            user_responses = Response.objects.filter(user=request.user, survey=survey)
            if not user_responses.exists():
                questions = survey.question_set.all()
                return render(request, 'portal/survey_start.html', {'questions': questions, 'survey': survey})
            else:
                if user_responses.first().check_complete:
                    return redirect('survey_already_done', slug=slug)
                else:
                    user_responses.first().delete()
                    questions = survey.question_set.all()
                    return render(request, 'portal/survey_start.html', {'questions': questions, 'survey': survey})
    else:
        return HttpResponse('Survey has no question')


@allow_lazy_user
def survey_already_done(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    return render(request, 'portal/survey_already_done.html', {'survey': survey})


@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    surveys = Survey.objects.active()
    return render(request, 'my_admin/home.html', {'surveys': surveys})


@user_passes_test(lambda u: u.is_superuser)
def survey_report(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    report_dict = survey.get_question_wise_report
    return render(request, 'my_admin/survey_q_wise_report.html',
                  {'survey': survey, 'report_dict': report_dict, 'total_votes': survey.response_set.count()})
