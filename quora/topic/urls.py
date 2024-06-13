from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.all_topics, name='all-topics'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic-detail'),
    path('topic/<int:topic_id>/follow', views.follow_topic, name='follow-topic'),
    path('topic/', views.create_topic, name='create-topic'),
    path('question/', views.create_question, name='create-question'),
    path('question/<int:question_id>/', views.question_detail, name='question-detail'),
    path('question/<int:question_id>/answer', views.create_answer, name='create-answer'),
    path('question/<int:question_id>/like', views.like_question, name='like-question'),
    path('question/<int:question_id>/dislike', views.dislike_question, name='dislike-question'),
    path('answer/<int:answer_id>/like', views.like_answer, name='like-answer'),
    path('answer/<int:answer_id>/dislike', views.dislike_answer, name='dislike-answer'),

]
