from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import CreateTopicForm, CreateQuestionForm, CreateAnswerForm
from .models import Topic, Question, Answer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def index(request):
    user = request.user
    if request.GET.get('search'):
        followed_topics = Topic.objects.filter(title__icontains=request.GET.get('search')).filter(followers=user)
    else:
        followed_topics = Topic.objects.filter(followers=user)
    questions = Question.objects.filter(topic__in=followed_topics).order_by('-created_at')
    qs_user_likes_subquery = questions.filter(
        liked_by__id=user.id).values('id')
    qs_user_dislikes_subquery = questions.filter(
        disliked_by__id=user.id).values('id')
    questions_with_top_answers = {}

    for question in questions:
        top_answers = Answer.objects.filter(question=question).annotate(
            likes_count=Count('liked_by'),
            dislikes_count=Count('disliked_by')
        ).order_by('dislikes_count', '-likes_count')
        ans_user_likes_subquery = top_answers.filter(
            liked_by__id=user.id).values('id')
        ans_user_dislikes_subquery = top_answers.filter(
            disliked_by__id=user.id).values('id')
        for answer in top_answers:
            answer.liked = ans_user_likes_subquery.filter(
                id=answer.id).exists()
            answer.disliked = ans_user_dislikes_subquery.filter(
                id=answer.id).exists()
        questions_with_top_answers[question.id] = top_answers[:2]
        question.liked = qs_user_likes_subquery.filter(id=question.id).exists()
        question.disliked = qs_user_dislikes_subquery.filter(
            id=question.id).exists()

    context = {
        'questions': questions,
        'answers': questions_with_top_answers
    }
    return render(request, 'index.html', context)


@login_required
def create_topic(request):
    if request.method == 'POST':
        form = CreateTopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            messages.success(request, 'Topic created successfully')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreateTopicForm()
    return render(request, 'topic/create-topic.html', {'form': form})


@login_required
def all_topics(request):
    topics = Topic.objects.all()
    return render(request, 'topic/view-all-topics.html', {'topics': topics})


@login_required
def topic_detail(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    is_followed = topic.followers.filter(id=request.user.id).exists()
    followers = topic.followers.count()
    questions = topic.question_set.prefetch_related('liked_by', 'disliked_by').annotate(
        liked_count=Count('liked_by'),
        disliked_count=Count('disliked_by')
    ).order_by('-liked_count', 'disliked_count')
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'topic': topic,
        'followers': followers,
        'is_followed': is_followed,
        'page_obj': page_obj,
    }

    return render(request, 'topic/topic-detail.html', context)


@login_required
def create_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Question Posted Successfully')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreateQuestionForm()
    return render(request, 'topic/create-question.html', {'form': form})


@login_required
def create_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = CreateAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            messages.success(request, 'Question Answered Successfully')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CreateAnswerForm()
    context = {'form': form, 'question': question}
    return render(request, 'topic/create-answer.html', context)


@login_required
def follow_topic(request, topic_id):
    if request.method == 'POST':
        topic = Topic.objects.get(pk=topic_id)
        topic.followers.add(request.user)
        messages.success(request, 'Topic followed successfully')
    return redirect(index)


@login_required
def question_detail(request, question_id):
    user = request.user
    question = Question.objects.get(pk=question_id)
    question.liked = question.liked_by.filter(id=user.id).exists()
    question.disliked = question.disliked_by.filter(id=user.id).exists()
        
    answers = question.answer_set.all()
    for answer in answers:
        answer.liked = answer.liked_by.filter(id=user.id).exists()
        answer.disliked = answer.disliked_by.filter(id=user.id).exists()
        
    context = {
        'question': question,
        'answers': answers
    }
    return render(request, 'topic/question-detail.html', context)


@login_required
def like_question(request, question_id):
    user = request.user
    question = Question.objects.get(pk=question_id)
    if not question.liked_by.filter(id=user.id).exists():
        question.liked_by.add(user)
    if question.disliked_by.filter(id=user.id).exists():
        question.disliked_by.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_question(request, question_id):
    user = request.user
    question = Question.objects.get(pk=question_id)
    if question.liked_by.filter(id=user.id).exists():
        question.liked_by.remove(user)
    if not question.disliked_by.filter(id=user.id).exists():
        question.disliked_by.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def like_answer(request, answer_id):
    user = request.user
    answer = Answer.objects.get(pk=answer_id)
    if not answer.liked_by.filter(id=user.id).exists():
        answer.liked_by.add(user)
    if answer.disliked_by.filter(id=user.id).exists():
        answer.disliked_by.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_answer(request, answer_id):
    user = request.user
    answer = Answer.objects.get(pk=answer_id)
    if answer.liked_by.filter(id=user.id).exists():
        answer.liked_by.remove(user)
    if not answer.disliked_by.filter(id=user.id).exists():
        answer.disliked_by.add(user)
    return redirect(request.META.get('HTTP_REFERER'))
