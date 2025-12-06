from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm,ScheduleMatchForm,NoteForm
from .models import Profile, ProfilePhoto, Feedback,ScheduledMatch,Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
import random



# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # find the user with this email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username   # get username from email
        except User.DoesNotExist:
            return render(request, 'main/login.html', {'error': 'No account with this email'})

        # authenticate using username + password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'main/login.html', {'error': 'Invalid email or password'})

    return render(request, 'main/login.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data["full_name"],
                location=form.cleaned_data["location"],
                dob=form.cleaned_data["dob"],
                interested_sport=form.cleaned_data["interested_sport"],
                experience_level=form.cleaned_data["experience_level"],
                profile_picture=form.cleaned_data.get("profile_picture")
            )
            return redirect('login_view')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})

@login_required(login_url='login_view')
def dashboard(request):
    return render(request, 'main/dashboard.html')

def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'main/profile.html', {'profile': profile})

def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
def edit_profile_view(request):
    profile = request.user.profile  # get logged-in user's profile

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        location = request.POST.get("location")
        dob = request.POST.get("dob")
        interested_sport = request.POST.get("interested_sport")
        experience_level = request.POST.get("experience_level")
        profile_picture = request.FILES.get("profile_picture")

        # Update profile fields
        profile.full_name = full_name
        profile.location = location
        profile.dob = dob
        profile.interested_sport = interested_sport
        profile.experience_level = experience_level

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()

        # ⭐ NEW SECTION — Handle extra photos ⭐
        photos = request.FILES.getlist("extra_photos")
        for p in photos:
            img = ProfilePhoto.objects.create(image=p)
            profile.extra_photos.add(img)

        messages.success(request, "Profile updated successfully!")
        return redirect("profile_view")

    return render(request, "main/edit_profile.html", {"profile": profile})

@login_required(login_url='login_view')
def delete_photo_view(request, photo_id):
    photo = get_object_or_404(ProfilePhoto, id=photo_id)

    # Ensure user is deleting their own photo
    if photo not in request.user.profile.extra_photos.all():
        messages.error(request, "You are not allowed to delete this photo.")
        return redirect("profile_view")

    # Remove from ManyToMany relation
    request.user.profile.extra_photos.remove(photo)

    # Delete image file from storage
    photo.image.delete(save=False)

    # Delete the object from database
    photo.delete()

    messages.success(request, "Photo deleted successfully!")
    return redirect('profile_view')

def about_feedback(request):
    all_feedback = Feedback.objects.all().order_by('-created_at')
    avg_rating = Feedback.objects.all().aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)

    return render(request, "main/about_feedback.html", {
        "feedback_list": all_feedback,
        "avg_rating": avg_rating,
    })

def save_feedback(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        feedback_text = request.POST.get("feedback")

        Feedback.objects.create(
            user=request.user,
            rating=rating,
            feedback=feedback_text
        )

        return redirect('about_feedback')


def schedule_match_view(request):
    if request.method == "POST":
        form = ScheduleMatchForm(request.POST, request.FILES)
        if form.is_valid():
            match = form.save(commit=False)
            match.created_by = request.user   # ← store creator
            match.save()
            return redirect('dashboard')
    else:
        form = ScheduleMatchForm()

    return render(request, 'main/schedule_match.html', {'form': form})



def available_matches_view(request):
    matches = ScheduledMatch.objects.exclude(created_by=request.user)
    return render(request, 'main/available_matches.html', {'matches': matches})

def all_matches_view(request):
    created = ScheduledMatch.objects.filter(created_by=request.user)
    joined = request.user.joined_matches.all()

# combine both without duplicates
    matches = (created | joined).distinct().order_by('date', 'time')


    win_count = matches.filter(result='win').count()
    loss_count = matches.filter(result='loss').count()
    draw_count = matches.filter(result='draw').count()

    context = {
        'matches': matches,
        'win_count': win_count,
        'loss_count': loss_count,
        'draw_count': draw_count
    }
    return render(request, 'main/all_matches.html', context)


def join_group(request, match_id):
    match = get_object_or_404(ScheduledMatch, id=match_id)

    # Save user as joined
    match.joined_players.add(request.user)

    # Redirect to WhatsApp group
    return redirect(match.chat_link)


def search_users_view(request):
    query = request.GET.get("q", "")
    sport_filter = request.GET.get("sport", "")
    location_filter = request.GET.get("location", "")
    level_filter = request.GET.get("level", "")

    users = Profile.objects.exclude(user=request.user)

    # Apply search by name
    if query:
        users = users.filter(full_name__icontains=query)

    # Apply filters
    if sport_filter:
        users = users.filter(interested_sport=sport_filter)

    if location_filter:
        users = users.filter(location__icontains=location_filter)

    if level_filter:
        users = users.filter(experience_level=level_filter)

    context = {
        "users": users,
        "query": query,
        "sport_filter": sport_filter,
        "location_filter": location_filter,
        "level_filter": level_filter,
    }
    return render(request, "main/search_grid.html", context)

def view_other_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    profile = user_obj.profile

    return render(request, 'main/view_profile.html', {
        'user_obj': user_obj,
        'profile': profile
    })

def update_status_result(request, match_id):
    match = get_object_or_404(ScheduledMatch, id=match_id)

    # Allow only joined players or creator to update
    if request.user == match.created_by or request.user in match.joined_players.all():

        new_status = request.POST.get("status")
        new_result = request.POST.get("result")

        if new_status:
            match.status = new_status
        
        if new_result:
            match.result = new_result

        match.save()

    return redirect('all_matches')

@login_required
def notes_view(request):
    """
    Show user's notes and handle creation of a new note (POST).
    """
    user = request.user
    form = NoteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.user = user

        # Pick a random color from model choices
        color_choices = [choice[0] for choice in Note.COLOR_CHOICES]
        note.color = random.choice(color_choices)

        note.save()
        messages.success(request, "Note added.")
        return redirect('notes')

    # list of user's notes, newest first
    notes = Note.objects.filter(user=user).order_by('-created_at')
    context = {
        'form': form,
        'notes': notes,
    }
    return render(request, 'main/notes.html', context)


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, "Note deleted.")
        return redirect('notes')
    # If GET request, show a simple confirm page or redirect
    return redirect('notes')
