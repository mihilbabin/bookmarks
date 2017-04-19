from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Profile, Relationship
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Success")
                else:
                    return HttpResponse("Disabled")
            else:
                return HttpResponse("Invalid data")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            create_action(new_user, 'has created an account')
            messages.success(request, "Welcome, {} you can log in now".format(new_user.first_name))
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.profile.following.values_list('id', flat=True)
    if following_ids:
        actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    actions = actions[:10]
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard', 'actions': actions})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile successfully edited")
            return redirect('dashboard')
        else:
            messages.error(request, 'Something wrong with form')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'accounts/list.html', {'section': 'people', 'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'accounts/detail.html', {'section': 'people', 'user': user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print(user_id, action)
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Relationship.objects.get_or_create(user_from=request.user.profile, user_to=user.profile)
                create_action(request.user, 'is following', user)
            else:
                Relationship.objects.filter(user_from=request.user.profile, user_to=user.profile).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            pass
    return JsonResponse({'status': 'fail'})
