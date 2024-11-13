from django.contrib import admin
from django.urls import path
from AskMe import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = "index"),
    path('hot/', views.hot, name = "hot"),
    path('ask/', views.ask, name = "ask"),
    path('tag/<str:tag_name>', views.tag_questions, name = "tag"),
    path('settings/', views.user_settings, name = "settings"),
    path('login/', views.login, name = "login"),
    path('signup/', views.register, name = "register"),
    path('question/<int:question_id>', views.one_question, name = "question")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 