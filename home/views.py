#project collaboration


from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile,CollaborationRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from .forms import CollaborationRequestForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index.html")

def quiz(request):
    return render(request,"quiz.html")

def query(request):
    return render(request,"query.html")

def resource(request):
    return render(request,"resource.html")

def projectcolab(request):
    return 1



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
        username = request.POST.get('username')
        password = request.POST.get('password')
        skill_name = request.POST.get('skill_name')
        professionalism_level = request.POST.get('professionalism_level')

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Create the user profile with the extra fields
        UserProfile.objects.create(
            user=user,
            skill_name=skill_name,
            professionalism_level=professionalism_level
        )

        # Log the user in
        login(request, user)

        # Redirect to the main page (index)
        return redirect('index')  # Make sure 'home' corresponds to your index URL

    return render(request, 'signup.html')


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('index')

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

# View to show all incoming collaboration requests for the logged-in user

# Page where the user can post a collaboration request
@login_required
def project_collaboration(request):
    if request.method == "POST":
        form = CollaborationRequestForm(request.POST)
        if form.is_valid():
            collaboration_request = form.save(commit=False)
            collaboration_request.from_user = request.user  # Set the user who is making the request
            collaboration_request.to_user = request.user  # For now, this is set to the user making the request
            collaboration_request.save()
            return redirect('project_collaboration')  # Redirect back to the project collaboration page
    else:
        form = CollaborationRequestForm()
    
    # Get the collaboration requests that are pending and sent to this user
    requests = CollaborationRequest.objects.filter(to_user=request.user, status="Pending")
    return render(request, 'project_collab.html', {'form': form, 'requests': requests})

# Accept collaboration request
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
