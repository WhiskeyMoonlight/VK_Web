from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Question, Answer, Tag, best_users


# Create your views here.


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
    questions = Question.manager.new()
    context = {
        'questions': paginate(questions, page),
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    item = Question.manager.get(id=question_id)
    answers = Answer.manager.answers_of_question(question_id)
    context = {
        'question': item,
        'answers': answers,
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'question.html', context)


def settings(request):
    context = {
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'settings.html', context)


def register(request):
    context = {
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'register.html', context)


def hot(request):
    page = request.GET.get('page', 1)
    questions = Question.manager.hot(3)
    context = {
        'questions': paginate(questions, page),
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'hot.html', context)


def ask(request):
    context = {
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'ask.html', context)


def login(request):
    context = {
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'login.html', context)


def tag(request, tag_name):
    tag_questions = list(Question.manager.question_of_tag(tag_name))
    page = request.GET.get('page', 1)
    context = {
        'questions': paginate(tag_questions, page),
        'tag_name': tag_name,
        'best_users': best_users(10),
        'tags': Tag.manager.popular_tags(5),
    }
    return render(request, 'tag.html', context)


def handler404(request, exception):
    context = {'page_title': '404'}
    return render(request, '404.html', context)
