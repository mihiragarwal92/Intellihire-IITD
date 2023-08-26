import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime

from .models import User, Quiz, Question, Score


COLORS = ['light', 'middle', 'dark']


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, 'quizmaker/index.html')
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
def quizzes(request, category):
    if (category == 'all'):
        quizzes_tmp = Quiz.objects.filter(public=True).order_by('timestamp').all()
        quizzes = []
        for quiz in quizzes_tmp:
            if len(quiz.questions.all()) > 0:
                quizzes.append(quiz)

    elif (category == 'own'):
        quizzes = Quiz.objects.filter(author=request.user).order_by('timestamp').all()

    return JsonResponse([quiz.serialize() for quiz in quizzes], safe=False)


@csrf_exempt
@login_required
def quiz(request, quiz_id):
    # Save new or edited quiz
    if request.method == 'POST':
        return save_quiz(request, quiz_id)
    
    # Query for requested quiz
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found.'}, status=404)

    # Return quiz contents, including its questions
    questions = quiz.questions.all()
    return JsonResponse({
        'quiz': quiz.serialize(),
        'questions':  [question.serialize() for question in questions]
    })


@login_required
def save_quiz(request, quiz_id):
    data = json.loads(request.body)
    title = data.get('title', '')
    description = data.get('description', '')
    visibility = data.get('visibility', '')
    if (visibility == 'public'):
        public = True
    else:
        public = False

    if title == ['']:
        return JsonResponse({
            'error': 'Title cannot be empty.'
        }, status=400)

    # Edit
    if quiz_id: 
        # Query for requested quiz
        try:
            quiz = Quiz.objects.get(author=request.user, pk=quiz_id)
        except Quiz.DoesNotExist:
            return JsonResponse({'error': 'Quiz not found.'}, status=404)
        quiz.title = title
        quiz.description = description
        quiz.public = public

    # Save new quiz
    else:
        random.seed(datetime.now().timestamp())
        colour_class = random.choice(COLORS)
        quiz = Quiz(
            author=request.user,
            title=title,
            description=description,
            public = public,
            colour_class=colour_class
        )

    quiz.save()
    return JsonResponse({
        'message': 'Quiz saved successfully.',
        'quiz': quiz.pk
        }, status=201)


@login_required
def remove_quiz(request, quiz_id):
    # Query for requested quiz
    try:
        quiz = Quiz.objects.get(author=request.user, pk=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found.'}, status=404)
    
    quiz.delete()
    return JsonResponse({'message': 'Quiz removed successfully.'}, status=201)


@csrf_exempt
@login_required
def question(request, question_id):
    # Save new or edited quiz
    if request.method == 'POST':
        return save_question(request, question_id)
    
    # Query for requested question
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found.'}, status=404)

    # Return question
    return JsonResponse({'question': question.serialize()})


@login_required
def save_question(request, question_id):
    data = json.loads(request.body)
    quiz_id = data.get('quiz', '')
    text = data.get('text', '')
    image = data.get('image', '')
    type = data.get('type', '')
    right_answer = data.get('right_answer', '')
    wrong_answer1 = data.get('wrong_answer1', '')
    wrong_answer2 = data.get('wrong_answer2', '')
    wrong_answer3 = data.get('wrong_answer3', '')
    isTrue = data.get('isTrue', '')

    if text == ['']:
        return JsonResponse({
            'error': 'Question cannot be empty.'
        }, status=400)
    
    if type != ['true_false'] and right_answer == ['']:
        return JsonResponse({
            'error': 'Answer cannot be empty.'
        }, status=400)

    try:
        quiz = Quiz.objects.get(author=request.user, pk=quiz_id)
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found.'}, status=404)

    # Edit question
    if question_id: 
        # Query for requested question
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found.'}, status=404)
        question.type = type
        question.text = text
        question.image = image
        question.right_answer = right_answer
        question.wrong_answer1 = wrong_answer1
        question.wrong_answer2 = wrong_answer2
        question.wrong_answer3 = wrong_answer3
        question.isTrue = isTrue

    # Save new question
    else:
        question = Question(
            quiz = quiz,
            text = text,
            image = image,
            type = type,
            right_answer = right_answer,
            wrong_answer1 = wrong_answer1,
            wrong_answer2 = wrong_answer2,
            wrong_answer3 = wrong_answer3,
            isTrue = isTrue
        )

    question.save()
    return JsonResponse({'message': 'Question saved successfully.'}, status=201)



@login_required
def remove_question(request, question_id):
    # Query for requested question
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found.'}, status=404)
    
    question.delete()
    return JsonResponse({'message': 'Question removed successfully.'}, status=201)


@csrf_exempt
@login_required
def score(request, category, quiz_id):
    # Save new score
    if request.method == 'POST' and category == 'save':
        return save_score(request)
    
    if category == 'all':
        scores = Score.objects
    
    elif category == 'own':
        scores = request.user.scores
    
    else:
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return JsonResponse({'error': 'Quiz not found.'}, status=404)
        scores = quiz.scores

    scores = scores.order_by('-score_percent')[:10]
    return JsonResponse([score.serialize() for score in scores], safe=False)


@login_required
def save_score(request):
    data = json.loads(request.body)
    quiz_id = data.get('quiz', '')
    score = int(data.get('score', ''))

    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found.'}, status=404)

    total = len(quiz.questions.all())

    score = Score(
        user=request.user,
        quiz=quiz,
        score=score,
        total=total,
        score_percent=round(score/total, 2)*100
    )

    score.save()
    return JsonResponse({'message': 'Score saved successfully.'}, status=201)


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'quizmaker/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'quizmaker/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'quizmaker/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'quizmaker/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'quizmaker/register.html')
