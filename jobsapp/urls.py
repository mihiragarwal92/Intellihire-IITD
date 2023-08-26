from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
        path('delete/<int:job_id>', delete, name='job-delete'),
    ])),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    path('employer/jobs/edit/<int:pk>', JobUpdateView.as_view(), name='employer-jobs-update'),
    path('upload/', upload_document, name='upload_document'),
    path('about', AboutView.as_view(), name='about-us'),
    path('contact', ContactView.as_view(), name='contact-us'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)