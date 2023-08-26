from django.contrib import admin

from .models import User, Quiz, Question, Score
# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ("serialize",)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("serialize",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ("serialize",)


admin.site.register(User, UserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Score, ScoreAdmin)