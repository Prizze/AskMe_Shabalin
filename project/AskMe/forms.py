from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Profile, Question, Tag, Answer
import uuid

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-50'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-50'}), required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise ValidationError('Логин не может быть пустым.')
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise ValidationError('Пароль не может быть пустым.')
        return password

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-50'}), required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-50'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-50'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-50'}), required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError('Логин не может быть пустым.')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError('Почта не может быть пустой') 


        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')

        return email

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if not password or not password_confirmation:
            self.add_error('password', 'Пароль не должен быть пустым')
            self.add_error('password_confirmation', 'Пароль не должен быть пустым')

        elif password != password_confirmation:
            self.add_error('password', 'Пароли не совпадают')
            self.add_error('password_confirmation', 'Пароли не совпадают')

        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            profile = Profile(user=user)
            profile.save()

        return user
    

class AskForm(forms.ModelForm):
    tags = forms.CharField(label='Тэги вопроса', required=False)

    class Meta:
        model = Question
        fields = ['title', 'body', 'tags']    
        labels = {
            'title': 'Ваш вопрос',
            'body': 'Описание вопроса'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['body'].required = False

    def clean_tags(self):
        tag_string = self.cleaned_data['tags']
        tags = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
        if not tags:
            raise forms.ValidationError("Добавьте хотя бы один тег.")
        return tags

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError('Пожалуйста, введите вопрос')
        return title
    
    def clean_body(self):
        body = self.cleaned_data['body']
        if not body:
            raise ValidationError('Пожалуйста, введите текст вопроса')
        return body

    def save(self, commit=True, profile=None):
        question = super().save(commit=False)
        
        if profile:
            question.profile = profile
        
        if commit:
            question.save()
            tags = self.cleaned_data['tags']
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
        
        return question

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['body']
        labels = {
            'body': 'Ваш ответ'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if not body:
            raise ValidationError('Пожалуйста, заполните поле')
        return body
    
    def save(self, commit=True, profile=None, question=None):
        answer = super().save(commit=False)
        answer.profile = profile
        answer.question = question
        
        if commit:
            answer.save()

        return answer
    
class SettingsForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']
    

    def __init__(self, *args, **kwargs):
        print (args)
        user = kwargs.pop('user')
        print (user)
        super().__init__(*args, **kwargs)

        if user:
            print(user)
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            if user.profile.nickname:
                self.fields['nickname'].initial = user.profile.nickname
            if user.profile.avatar:
                self.fields['avatar'].initial = user.profile.avatar.url

        self.fields = {
            'username': self.fields['username'],
            'email': self.fields['email'],
            'nickname': self.fields['nickname'],
            'avatar': self.fields['avatar'],
        }


    
