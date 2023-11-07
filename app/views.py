from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long Lorem Ipsum {i}',
        'tags': ['bender']
    } for i in range(10)
]

for item in QUESTIONS:
    if item['id'] % 2 == 0:
        item['tags'].append('black-jack')
    else:
        item['tags'].append('anime')

ANSWERS = [
    {
        'id': i,
        'content': f'Long Lorem Ipsum answer {i}'
    } for i in range(2)
]


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)

    return paginator.page(page)


def index(request):
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, 1)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'answers': ANSWERS})


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    return render(request, 'hot.html', {'questions': paginate(QUESTIONS, 1)})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')