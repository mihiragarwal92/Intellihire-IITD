from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Model
# Create your views here.
reloadModel = joblib.load("./models/train_model.pkl")
scaler = StandardScaler()

def home(request):
    
    return render(request,"personality/index.html")

def result(request):
   
   if request.method == 'POST':
      
      gender = request.POST.get('gender')
      if(gender == "Female"):
        gender_no = 1
      else:
        gender_no = 2
      age = request.POST.get('age')
      openness = request.POST.get('openness')
      neuroticism = request.POST.get('neuroticism')
      conscientiousness = request.POST.get('conscientiousness')
      agreeableness = request.POST.get('agreeableness')
      extraversion = request.POST.get('extraversion')
      result = np.array([gender_no, age, openness,neuroticism, conscientiousness, agreeableness, extraversion], ndmin = 2)
      final = scaler.fit_transform(result)
      print(request)
      personality = str(reloadModel.predict(final)[0])
      context={'personality':personality}
      print(personality)
   return render(request,"personality/submit.html",context)

    