
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView,UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job, Applicant
User = get_user_model()

class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)
    
    def presen_t(self):
        published_jobs = Job.objects.filter(filled=True).order_by('-created_at')
        jobs = published_jobs.filter(is_closed=False)
        total_candidates = User.objects.filter(role='employee').count()
        total_companies = User.objects.filter(role='employer').count()
        context = {

                'total_candidates': total_candidates,
                'total_companies': total_companies,
                'total_jobs': len(jobs),
                'total_completed_jobs':len(published_jobs.filter(is_closed=True))
                 
                    }
        return context

class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class JobUpdateView(UpdateView):
    template_name = 'jobs/update.html'
    form_class = CreateJobForm
    model = Job
    extra_context = {
        'title': 'Update Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Retrieve the object being updated
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    job.filled = not job.filled
    job.save()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


@login_required(login_url=reverse_lazy('accounts:login'))
def delete(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        print('job')
        job.delete()
    except Job.DoesNotExist:
        print("not exists") 

    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))
