from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from userauth.models import Profile
from topic.models import Topic, Question, Answer
from .forms import UserProfileForm, UserSignUpForm, UserSignInForm


@login_required
def about(request):
    user = request.user

    profile = Profile.objects.get(user=user)
    followed_topics = Topic.objects.filter(followers=user)
    questions_asked = Question.objects.filter(user=user)
    answers_given = Answer.objects.filter(user=user)

    context = {
        'profile': profile,
        'followed_topics': followed_topics,
        'questions_asked': questions_asked,
        'answers_given': answers_given,
    }
    return render(request, 'userauth/about.html', context)


@login_required
def EditProfile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,
                               instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('edit-profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserProfileForm(
            instance=request.user.profile, user=request.user)

    return render(request, 'userauth/edit-profile.html', {'form': form})


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    questions_answered = Answer.objects.filter(
        user=user).prefetch_related('questions')

    context = {
        'user': user,
        'profile': profile,
        'questions_answered': questions_answered
    }
    return render(request, 'userauth/profile.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('users/sign-in')


def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, age=int(
                form.cleaned_data.get('age')), gender=form.cleaned_data.get('gender'))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data['password1']
            messages.success(request, f'Account created for {username}!')
            new_user = authenticate(username=username,
                                    password=password,)
            login(request, new_user)
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserSignUpForm()
    return render(request, 'sign-up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = UserSignInForm(request, request.POST)
        if form.is_valid():
            print('here')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserSignInForm(request)
    return render(request, 'sign-in.html', {'form': form})
