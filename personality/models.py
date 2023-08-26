# from django.db import models

# class PersonalityPrediction(models.Model):
#     GENDER_CHOICES = (
#         ('Female', 'Female'),
#         ('Male', 'Male'),
#     )

#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Female')  # Default value set to 'Female'
#     age = models.IntegerField()
#     openness = models.FloatField()
#     neuroticism = models.FloatField()
#     conscientiousness = models.FloatField()
#     agreeableness = models.FloatField()
#     extraversion = models.FloatField()
#     predicted_personality = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.gender} - Age: {self.age} - Predicted Personality: {self.predicted_personality}"
