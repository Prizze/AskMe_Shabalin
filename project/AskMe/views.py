from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Profile, Answer, AnswerReaction, QuestionReaction, Tag
from django.contrib import auth
from .forms import LoginForm, UserForm, AskForm, AnswerForm, SettingsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect
from math import ceil
import json
from django.http import JsonResponse


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
    
    tags = Tag.objects.get_top_tags()
    page = paginate(questions, request, per_page = 20)
    data ={
        "questions": page.object_list,
        "page_obj": page,
        "tags": tags
    }
    return render(request, "index.html", context=data)

def hot(request):
    hot_questions = Question.objects.get_hot()
    page = paginate(hot_questions, request, per_page = 20)
    tags = Tag.objects.get_top_tags()
    data = {
        "questions": page.object_list,
        "page_obj": page,
        "tags": tags
    }
    return render(request, "hot.html", context = data)

@login_required(redirect_field_name="continue")
def ask(request):
    form = AskForm()
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(profile=request.user.profile)
            return redirect('question', question_id=question.id)
        
    tags = Tag.objects.get_top_tags()
    data={
        "tags": tags,
        "form": form
    }
    return render(request, "ask.html", context=data)

def tag_questions(request, tag_name):
    tags = Tag.objects.get_top_tags()
    tag = Tag.objects.filter(name=tag_name).first()
    questions = Question.objects.get_questions_by_tag(tag)
    page = paginate(questions, request, per_page = 4)
    data = {
        "tag": tag,
        "questions":page.object_list,
        "page_obj":page,
        "tags": tags
    }
    return render(request, "tag.html", context=data)

@login_required(redirect_field_name="continue")
def user_settings(request):
    form = SettingsForm(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    tags = Tag.objects.get_top_tags()
    data = {
        "tags": tags,
        "form": form
    }
    return render(request, "settings.html", context=data)

def get_next_url(request, default='index'):
    next_url = request.GET.get('continue')

    if not next_url:
        next_url = request.POST.get('continue')

    return next_url or default

def login(request):
    form = LoginForm()
    next_url = get_next_url(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(next_url)
            else:
                form.add_error('username', 'Некорректные данные для входа.')
                form.add_error('password','')
                
    tags = Tag.objects.get_top_tags()
    data={
        "tags": tags,
        "form": form,
        'continue': next_url
    }
    return render(request, "login.html", context=data)
    
@login_required(redirect_field_name="continue")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(reverse('index'))
    tags = Tag.objects.get_top_tags()
    data={
        "tags": tags,
        "form": form
    }
    return render(request, "register.html", context=data)

def get_redirect_url_for_answer(question, answer_id, answers_queryset, per_page=5):
    total_answers = answers_queryset.count()
    last_page = ceil(total_answers / per_page)
    return f"{question.get_absolute_url()}?page={last_page}#answer-{answer_id}"


def one_question(request, question_id):
    question = Question.objects.filter(id=question_id).first()
    answers = Answer.objects.get_answers(question)
    page = paginate(answers, request, per_page = 10)
    form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(profile=request.user.profile, question=question)
            return redirect('question', question_id=question.id)

    tags = Tag.objects.get_top_tags()
    data={
        "question": question,
        "tags": tags,
        "page_obj":page,
        "answers": page.object_list,
        "form": form
    }
    return render(request,"one_question.html", context=data)

@require_POST
@login_required
def get_likes_status(request, id):
    body = json.loads(request.body) 
    is_question = body.get('is_question')

    if is_question == 'true':
        question = Question.objects.filter(id=id).first()
        is_liked = QuestionReaction.objects.filter(profile=request.user.profile, question=question).exists()
    else:
        answer = Answer.objects.filter(id=id).first()
        is_liked = AnswerReaction.objects.filter(profile=request.user.profile, answer=answer).exists()
    
    return JsonResponse({
        'is_liked': is_liked
    })

@require_POST
@login_required
def like_async(request, id):
    body = json.loads(request.body) 
    reaction_type = body.get('type')
    is_question = body.get('is_question')

    if is_question == 'true':
        question = Question.objects.filter(id=id).first()
        reaction = QuestionReaction(profile=request.user.profile, question=question, reaction=reaction_type)
    else:
        answer = Answer.objects.filter(id=id).first()
        reaction = AnswerReaction(profile = request.user.profile, answer=answer, reaction=reaction_type)

    reaction.save()

    if is_question == 'true':
        rating = reaction.question.rating
    else:
        rating = reaction.answer.rating

    return JsonResponse({
        'like_count': rating
    })

@login_required
def set_correct(request, id):
    body = json.loads(request.body) 
    is_correct = body.get('is_correct')
    print(body)
    print(is_correct)

    answer = Answer.objects.filter(id=id).first()

    if answer.question.profile.user!= request.user:
        return JsonResponse({'error': 'Permission denied'})

    answer.is_correct = is_correct
    answer.save()
    return JsonResponse({
        'success': True
    })

@login_required
def is_correct(request, id):
    answer = Answer.objects.filter(id=id).first()
    if answer.is_correct:
        is_correct = True
    else:
        is_correct = False

    return JsonResponse({
        'is_correct': is_correct
    })

