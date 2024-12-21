# qa/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/reply/', views.reply_to_question, name='reply_to_question'),
]
