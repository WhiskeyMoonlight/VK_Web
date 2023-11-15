from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long Lorem Ipsum {i}',
        'tags': ['bender'],
    } for i in range(20)
]

for q in QUESTIONS:
    if q['id'] % 2 == 0:
        q['tags'].append('black-jack')
    else:
        q['tags'].append('anime')

ANSWERS = [
    {
        'id': i,
        'content': f'Long Lorem Ipsum answer {i}',
    } for i in range(2)
]


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages


def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'answers': ANSWERS})


def settings(request):
    return render(request, 'settings.html')


def register(request):
    return render(request, 'register.html')


def hot(request):
    page = request.GET.get('page', 1)
    return render(request, 'hot.html', {'questions': paginate(QUESTIONS, page)})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def tag(request, tag_name):
    tag_questions = []
    for Q in QUESTIONS:
        if tag_name in Q['tags']:
            tag_questions.append(Q)
    page = request.GET.get('page', 1)
    return render(request, 'tag.html',
                  {'questions': paginate(tag_questions, page), 'tag': tag_name})
