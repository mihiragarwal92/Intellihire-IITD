from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Quiz(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    colour_class = models.CharField(max_length=10, default='light')

    def serialize(self):
        return {
            'id': self.id,
            'author': self.author.username,
            'title': self.title,
            'description': self.description,
            'timestamp': self.timestamp.strftime('%b %d %Y, %I:%M %p'),
            'public': self.public,
            'colour_class': self.colour_class
        }
    
class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(blank=False)
    image = models.CharField(max_length=2083, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    type = models.CharField(max_length=20, blank=False, default=None)

    right_answer = models.CharField(max_length=250, default=None)

    wrong_answer1 = models.CharField(max_length=250, default=None)
    wrong_answer2 = models.CharField(max_length=250, default=None)
    wrong_answer3 = models.CharField(max_length=250, default=None)

    isTrue = models.BooleanField(default=True)

    def serialize(self):
        return {
            'id': self.id,
            'quiz': self.quiz.id,
            'text': self.text,
            'image': self.image,
            'timestamp': self.timestamp.strftime('%b %d %Y, %I:%M %p'),
            'type': self.type,
            'right_answer': self.right_answer,
            'wrong_answer1': self.wrong_answer1,
            'wrong_answer2': self.wrong_answer2,
            'wrong_answer3': self.wrong_answer3,
            'isTrue': self.isTrue
        }

class Score(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='scores')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    score_percent = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'quiz_id': self.quiz.id,
            'quiz_title': self.quiz.title,
            'score': self.score,
            'total': self.total,
            'score_percent': self.score_percent,
            'timestamp': self.timestamp.strftime('%b %d %Y, %I:%M %p')
        }
        
    