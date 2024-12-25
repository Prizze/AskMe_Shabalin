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
    path('profile/edit', views.user_settings, name = "settings"),
    path('login/', views.login, name = "login"),
    path('signup/', views.register, name = "register"),
    path('question/<int:question_id>', views.one_question, name = "question"),
    path('logout',views.logout, name = "logout"),
    path('question/<int:id>/like_async/', views.like_async, name='like_async'),
    path('question/<int:id>/get_likes_status/', views.get_likes_status, name='get_likes_status'),
    path('question/<int:id>/set_correct/', views.set_correct, name='set_correct'),
    path('question/<int:id>/is_correct/', views.is_correct, name='is_correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 