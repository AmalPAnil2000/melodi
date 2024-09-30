from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth import logout
from .form import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
from .form import UserForm,SocialLinksForm,ProfilePhotoForm

# Create your views here.


# Sign-up

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('login')  # Redirect to the home page after sign-up
    else:
        form = SignUpForm()
    return render(request, 'authendication/sign_up.html', {'form': form})

# login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'authendication/login.html', {'form': form})

# log out

def logout_view(request):
    logout(request)
    return redirect('index')


# index

def index(request):
    user = request.user  # Get the logged-in user
    context = {'user': user}
    return render(request, 'index.html', context)


# Show 

def show(request):
    return render(request, 'show.html')


# footer
def footer(request):
    return render(request, 'footer.html')


# generate
from django.shortcuts import render
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure Gemini API with your API key
genai.configure(api_key="AIzaSyAEpxEaoSLL6Z6gBM3Ha0edMAECjW6h61g")

@login_required
def generate_view(request):
    lyrics = None
    saved_lyrics = Lyrics.objects.filter(user=request.user).order_by('-created_at')  # Fetch only the user's lyrics

    if request.method == "POST":
        keyword = request.POST['keyword']
        genre = request.POST['genre']
        min_length = int(request.POST['min_length'])  # Get the minimum length from the form
        max_length = int(request.POST['max_length'])  # Get the maximum length from the form

        # Create user input with genre, keyword, and length
        user_input = f"Create a {genre} lyric based on the keyword: {keyword}, with a length between {min_length} and {max_length} words."

        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            # Apply custom safety settings
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            # Generate content using the model
            response = model.generate_content([user_input], safety_settings=safety_settings)

            if hasattr(response, 'safety_ratings') and response.safety_ratings:
                lyrics = "The generated content was flagged for safety concerns. Please try different keywords."
            else:
                generated_lyrics = response.text  # Fetch the generated lyrics

                # Use your split_lyrics function to separate the sections
                sections = split_lyrics(generated_lyrics)

                # Combine the sections into a single lyrics string
                lyrics = f"""
                Verse 1:\n{sections['verse1'].strip()}\n\n
                Chorus:\n{sections['chorus'].strip()}\n\n
                Verse 2:\n{sections['verse2'].strip()}\n\n
                Bridge:\n{sections['bridge'].strip()}\n\n
                Outro:\n{sections['outro'].strip()}
                """

                # Save the generated lyrics to the database
                Lyrics.objects.create(
                    user=request.user,
                    keyword=keyword,
                    genre=genre,
                    verse1=sections['verse1'].strip(),
                    chorus=sections['chorus'].strip(),
                    verse2=sections['verse2'].strip(),
                    bridge=sections['bridge'].strip(),
                    outro=sections['outro'].strip()
                )

        except Exception as e:
            lyrics = f"An error occurred: {str(e)}"

    return render(request, 'generate.html', {'lyrics': lyrics, 'saved_lyrics': saved_lyrics})



def split_lyrics(full_lyrics):
    sections = {
        'verse1': '',
        'chorus': '',
        'verse2': '',
        'bridge': '',
        'outro': ''
    }
    
    # Split by new line
    lines = full_lyrics.strip().split('\n')

    # Assuming specific markers for sections in the generated text
    section = None
    for line in lines:
        if "Verse 1" in line:
            section = 'verse1'
        elif "Chorus" in line:
            section = 'chorus'
        elif "Verse 2" in line:
            section = 'verse2'
        elif "Bridge" in line:
            section = 'bridge'
        elif "Outro" in line:
            section = 'outro'
        
        if section:
            sections[section] += line + '\n'

    return sections


@login_required
def delete_lyric(request, lyric_id):
    lyric = get_object_or_404(Lyrics, id=lyric_id, user=request.user)
    lyric.delete()
    return redirect('generate_lyrics')


# profile

@login_required
def profile_view(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        user_profile = Profile(user=user)
        user_profile.save()

    context = {
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

@login_required
def profile_edit(request):
    user = request.user
    try:
        user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        user_profile = Profile(user=user)
        user_profile.save()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfilePhotoForm(request.POST, request.FILES, instance=user_profile)
        social_links_form = SocialLinksForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid() and social_links_form.is_valid():
            user_form.save()
            profile_form.save()
            social_links_form.save()  # Save the social media links form
            return redirect('profile_view')  # Redirect to profile view after updating
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfilePhotoForm(instance=user_profile)
        social_links_form = SocialLinksForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'social_links_form': social_links_form,  # Include the social media form in the context
    }
    return render(request, 'profile_edite.html', context)


# about
def about_view(request):
    return render(request, 'about.html')


# admin
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import LyricsGeneration, Music

def admin_dashboard(request):
    # Get all users
    user_count = User.objects.count()

    # Count of total lyrics generations
    total_generations = LyricsGeneration.objects.aggregate(total=Sum('generation_count'))['total'] or 0

    # Total music count
    total_music_count = Music.objects.count()

    # Get total logins for the last 7 days
    days = []
    login_counts = []
    today = datetime.now().date()
    
    for i in range(7):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        day_login_count = User.objects.filter(last_login__range=(day_start, day_end)).count()
        days.append(day.strftime('%Y-%m-%d'))
        login_counts.append(day_login_count)

    context = {
        'user_count': user_count,
        'total_generations': total_generations,
        'total_music_count': total_music_count,
        'days': days[::-1],  # reverse the order for display
        'login_counts': login_counts[::-1],  # reverse to show oldest first
    }

    return render(request, 'dashboard_admin/dashboard.html', context)



from django.utils.timezone import now
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
def daily_report(request):
    today = now().date()

    # Get the generation count for today
    generation_count = LyricsGeneration.objects.filter(generated_at__date=today).count()

    # Get the login count for today
    login_count = User.objects.filter(last_login__date=today).count()

    # Get the music added count for today
    total_music_count = Music.objects.count()

    # Get all user details who logged in today
    users_logged_in_today = User.objects.filter(last_login__date=today)

    context = {
        'generation_count': generation_count,
        'login_count': login_count,
        'total_music_count': total_music_count,  # Remove extra space here
        'users_logged_in_today': users_logged_in_today,
        'today': today,
    }

    # If the user wants to download the report as a PDF
    if request.GET.get("download") == "pdf":
        return render_to_pdf('dashboard_admin/report_pdf.html', context)

    return render(request, 'dashboard_admin/report.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="daily_report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


from django.contrib import messages
def terminate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} has been terminated.')
        return redirect('user_management')
    
def user_management(request):
    users = User.objects.all()
    
    context = {
        'users': users,
    }
    
    return render(request, 'dashboard_admin/user.html', context)


# music-list
# music-delete
# music add
from .form import MusicForm
def music_list(request):
    query = request.GET.get('q')  # Get the search query from the URL
    if query:
        music_files = Music.objects.filter(
            models.Q(title__icontains=query) | 
            models.Q(artist__icontains=query) | 
            models.Q(category__icontains=query)
        )
    else:
        music_files = Music.objects.all()
    
    return render(request, 'addmusic/music_list.html', {'music_files': music_files})

def add_music(request):
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_music')  # Redirect to the music list page
    else:
        form = MusicForm()

    # Get all music entries to display them
    music_list = Music.objects.all()

    return render(request, 'addmusic/add_music.html', {'form': form, 'music_list': music_list})

def edit_music(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES, instance=music)
        if form.is_valid():
            form.save()
            return redirect('music_list')
    else:
        form = MusicForm(instance=music)

    return render(request, 'addmusic/edite_music.html', {'form': form, 'music': music})

def delete_music(request, pk):
    music = Music.objects.get(pk=pk)
    music.delete()
    return redirect('add_music')


# fav

def add_to_favorites(request, music_id):
    # Add the music ID to the user's session favorites
    favorites = request.session.get('favorites', [])
    if music_id not in favorites:
        favorites.append(music_id)
        request.session['favorites'] = favorites
    return redirect('music_list')

def remove_from_favorites(request, music_id):
    # Remove the music ID from the user's session favorites
    favorites = request.session.get('favorites', [])
    if music_id in favorites:
        favorites.remove(music_id)
        request.session['favorites'] = favorites
    return redirect('favorites_page')

def favorites_page(request):
    favorites_ids = request.session.get('favorites', [])
    favorite_music = Music.objects.filter(id__in=favorites_ids)
    return render(request, 'fav.html', {'favorite_music': favorite_music})