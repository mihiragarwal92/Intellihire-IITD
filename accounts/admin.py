from django.contrib import admin
from .models import User
from jobsapp.models import Job, Applicant ,Document

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Applicant)
admin.site.register(Document)