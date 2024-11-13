from django.contrib import admin
from .models import Profile, Question, Answer, Tag, QuestionReaction, AnswerReaction

# Регистрация моделей для административной панели
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(QuestionReaction)
admin.site.register(AnswerReaction)
# Register your models here.
