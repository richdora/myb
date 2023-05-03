from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from itertools import chain
from photo.models import Photo
from .models import PrivateMessage
from .forms import PrivateMessageForm
from django.contrib. auth import get_user_model
from django.contrib.auth.models import User
from .models import CustomUser
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


User = get_user_model()

def index_redirect(request):
    if request.user.is_authenticated:
        return redirect('index', username=request.user.username)
    else:
        return redirect('login')


def index(request, username):
    owner = get_object_or_404(User, username=username)
    latest_photo = Photo.objects.filter(user=owner).order_by('-created_date').first()

    return render(request, 'myapp/index.html', {'latest_photo': latest_photo, 'owner': owner,})



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index', username=username)  # pass the username argument here
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})



def is_not_authenticated(user):
    return not user.is_authenticated


@user_passes_test(is_not_authenticated, login_url='index_redirect')
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:  # Check if the user is an admin
                    return redirect('admin:index')  # Redirect admin users to the Django admin page
                return redirect('index', username=user.username)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = CustomAuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('home')  # redirect to the login view instead of 'index'

def landing(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/index.html')
    else:
        return render(request, 'myapp/login.html')


@login_required
def view_messages(request, recipient_username):
    recipient = User.objects.get(username=recipient_username)
    sent_messages = PrivateMessage.objects.filter(sender=request.user, recipient=recipient)
    received_messages = PrivateMessage.objects.filter(sender=recipient, recipient=request.user)

    # If you want to mark messages as read when the user views them
    received_messages.update(read=True)

    messages = sorted(chain(sent_messages, received_messages), key=lambda message: message.timestamp)

    return render(request, 'myapp/view_messages.html', {'messages': messages, 'recipient': recipient})


@login_required
def received_messages(request):
    user = request.user
    messages = user.received_messages.order_by('-timestamp')
    return render(request, 'myapp/received_messages.html', {'messages': messages})


def message_sent(request, owner_username):
    return render(request, 'myapp/message_sent.html', {'owner_username': owner_username})


@login_required
def sent_messages(request):
    sent_messages = PrivateMessage.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'myapp/sent_messages.html', {'sent_messages': sent_messages})


def home(request):
    if request.user.is_authenticated:
        return redirect('index', username=request.user.username)
    else:
        return redirect('login')


@login_required
def create_and_send_message(request, owner_username):
    owner = User.objects.get(username=owner_username)
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = owner
            message.save()
            return redirect('message_sent', owner_username=owner_username)
    else:
        form = PrivateMessageForm()
    return render(request, 'myapp/create_and_send_message.html', {'form': form, 'owner': owner})


def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'myapp/user_profile.html', {'profile_user': user})


def user_search(request):
    query = request.GET.get("q")
    users = None

    if query:
        users = CustomUser.objects.filter(Q(username__icontains=query))

    return render(request, "myapp/user_search.html", {"users": users})

