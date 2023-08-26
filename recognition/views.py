from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404


import json
import re
import time




def questions(request):
    
    return render(request,"recognitions/questionPage.html")

