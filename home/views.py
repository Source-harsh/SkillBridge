#project collaboration

from django.db.models import Q  
from argon2 import hash_password
from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .forms import SkillSearchForm

from home import models

# Create your views here.
def index(request):
    return render(request,"index.html")

def quiz(request):
    return render(request,"quiz.html")

@login_required
def query(request):
    if request.method == 'POST':
        sender_username = request.POST['sender_username']
        message_content = request.POST['message']
        
        # Retrieve the sender (user) object based on the username
        sender = User.objects.get(username=sender_username)
        
        # Create and save the message
        Message.objects.create(sender=sender, receiver=request.user, content=message_content)
        
    messages = Message.objects.filter(receiver=request.user)  # Assuming the user is the receiver
    return render(request, 'query.html', {'messages': messages})

def resource(request):
    return render(request,"resource.html")


def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! You are now signed in.")
            return redirect('index')  # Redirect to the main page
        else:
            # Invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        skill_name = request.POST['skill_name']
        skill_level = request.POST['skill_level']
        time_available = request.POST['time_available']
        email = request.POST['email']  # Get email from the form

        # Hash the password before storing it
        hashed_password = make_password(password)

        # Create a new user profile
        user_profile = UserProfile(
            username=username,
            password=hashed_password,
            skill_name=skill_name,
            skill_level=skill_level,
            time_available=time_available,
            email=email  # Save the email
        )
        user_profile.save()

        # Create a new user in the User model (with email, if necessary)
        user = User.objects.create_user(username=username, password=password, email=email)  # Create the user
        login(request, user)  # Log the user in

        return redirect('index')  # Redirect to a dashboard or home page after successful signup

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('index')


@login_required
def modify_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        # Add skill logic (for demonstration, this might involve saving in another model)
        skill = request.POST.get('skill')
        level = request.POST.get('level')
        password = request.POST.get('password')

        if password:
            request.user.set_password(password)
            request.user.save()

        # Redirect to index after saving
        return redirect('index')

    return render(request, 'modify_profile.html')


@login_required
def accept_request(request, request_id):
    collaboration_request = get_object_or_404(CollaborationRequest, id=request_id, to_user=request.user)
    collaboration_request.status = "Accepted"
    collaboration_request.save()
    return redirect('project_collaboration')

# Reject collaboration request
@login_required
def reject_request(request, request_id):
    collaboration_request = get_object_or_404(CollaborationRequest, id=request_id, to_user=request.user)
    collaboration_request.status = "Declined"
    collaboration_request.save()
    return redirect('project_collaboration')

@login_required
def project_collaboration(request):
    if request.method == 'POST':
        # Get the skill requested by the user
        skill_name = request.POST.get('skill_name')

        # Query users with the specified skill
        users_with_skill = UserProfile.objects.filter(skill_name=skill_name)

        return render(request, 'project_collab.html', {
            'users_with_skill': users_with_skill,
            'skill_name': skill_name
        })

    return render(request, 'project_collab.html', {})
