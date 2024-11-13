from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Profile, Answer, AnswerReaction, QuestionReaction, Tag
import copy

 
QUESTIONS = []
for i in range(30):
    QUESTIONS.append({
        "title": 'title ' + str(i),
        "id": i,
        "text": 'text ' + str(i)
    })

TAGS = []
for i in range(5):
    TAGS.append({
        "name": 'tag' + str(i),
        "id": i
    })

def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1) 
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request, per_page = 20)
    data ={
        "is_user_logged_in": True,
        "questions": page.object_list,
        "page_obj": page,
        "tags": TAGS
    }
    return render(request, "index.html", context=data)

def hot(request):
    hot_questions = Question.objects.get_hot()
    page = paginate(hot_questions, request, per_page = 20)
    data = {
        "is_user_logged_in": True,
        "questions": page.object_list,
        "page_obj": page,
        "tags": TAGS
    }
    return render(request, "hot.html", context = data)

def ask(request):
    data={
        "tags": TAGS,
        "is_user_logged_in": True,
    }
    return render(request, "ask.html", context=data)

def tag_questions(request, tag_name):
    tag = Tag.objects.filter(name=tag_name).first()
    questions = Question.objects.get_questions_by_tag(tag)
    page = paginate(questions, request, per_page = 4)
    data = {
        "tag": tag,
        "questions":page.object_list,
        "page_obj":page,
        "tags": TAGS
    }
    return render(request, "tag.html", context=data)

def user_settings(request):
    data = {
        "is_user_logged_in": True,
        "tags": TAGS
    }
    return render(request, "settings.html", context=data)

def login(request):
    data={
        "is_user_logged_in": False,
        "tags": TAGS
    }
    return render(request, "login.html", context=data)

def register(request):
    data={
        "is_user_logged_in": False,
        "tags": TAGS
    }
    return render(request, "register.html", context=data)

def one_question(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    answers = Answer.objects.get_answers(question)
    page = paginate(answers, request, per_page = 5)
    data={
        "is_user_logged_in": True,
        "question": question,
        "tags": TAGS,
        "page_obj":page,
        "answers": page.object_list
    }
    return render(request,"one_question.html", context=data)

