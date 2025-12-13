from django import contrib
from django.core.checks import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from collections import defaultdict
from django.contrib.auth import login, authenticate
from django.forms.widgets import FileInput
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from .forms import UserRegistrationForm
import os
from django.utils.timezone import now
import time
from django.conf import settings
import threading
from gtts import gTTS
import json
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import pyttsx3
from .models import TexttoAudio
from django.core.files.storage import FileSystemStorage
from .forms import TextForm
import asyncio
from googletrans import Translator
from sympy import symbols, Eq, solve, simplify
from pint import UnitRegistry
from django.http import JsonResponse
from .forms import LanguageTranslationForm, MathConversionForm, UnitConversionForm, UserUpdateForm, ProfileUpdateForm







# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')


# Check if user is an admin (teacher)
def is_admin(user):
    return user.is_staff

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.contrib.auth.models import User

@login_required
def chat_page(request):
    return render(request, 'dashboard/chat.html')

@login_required
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        sender = request.user
        chat_message = ChatMessage.objects.create(sender=sender, message=message_text)
        return JsonResponse({
            'status': 'Message Sent',
            'id': chat_message.id,
            'message': chat_message.message,
            'sender': sender.username,
            'timestamp': localtime(chat_message.timestamp).strftime('%I:%M %p'),
            'date': localtime(chat_message.timestamp).strftime('%A, %B %d, %Y')
        })
    return JsonResponse({'status': 'Error'}, status=400)

@login_required
def get_messages(request):
    messages = ChatMessage.objects.all().order_by('timestamp')
    
    grouped_messages = defaultdict(list)
    for msg in messages:
        date_key = localtime(msg.timestamp).strftime('%A, %B %d, %Y')  # Group messages by date
        grouped_messages[date_key].append({
            'id': msg.id,
            'sender': msg.sender.username,
            'message': msg.message,
            'timestamp': localtime(msg.timestamp).strftime('%I:%M %p'),
            'is_owner': msg.sender == request.user  # Check if user owns the message
        })

    return JsonResponse({'grouped_messages': dict(grouped_messages)})

def delete_message(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(ChatMessage, id=message_id)
        
        # Allow only the sender to delete their own message
        if message.sender == request.user:
            message.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



@login_required
def notes(request):
    if request.method == "POST":
        if request.user.is_staff:  # Only teachers can create notes
            form = NotesForm(request.POST)
            if form.is_valid():
                notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
                notes.save()
                messages.success(request, f"Notes Added by {request.user.username} Successfully!")
            else:
                messages.error(request, "Invalid form submission.")
        else:
            messages.warning(request, "You are not allowed to create notes.")
        return redirect('notes')

    # All users (students & teachers) can view notes
    form = NotesForm()
    notes = Notes.objects.all()  # Show all notes
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk):
    note = get_object_or_404(Notes, id=pk)

    if not request.user.is_staff:  # If user is not an admin/teacher
        messages.error(request, "Students are not allowed to delete notes.")
        return redirect("notes")

    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes




    

@login_required
def homework(request):
    if request.method == "POST":
        if not request.user.is_staff:  # Only teachers can add homework
            messages.error(request, "You are not allowed to add homework.")
            return redirect("homework")

        form = HomeworkForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished', False) == 'on'
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f'Homework added by {request.user.username}!')
            return redirect("homework")

    form = HomeworkForm()
    homework_list = Homework.objects.all()  # Show all homework for students & teachers
    context = {
        "homeworks": homework_list,
        "form": form,
    }
    return render(request, "dashboard/homework.html", context)


def update_homework(request, pk):
    homework = get_object_or_404(Homework, id=pk)

    if not request.user.is_staff:  # Only teachers can update To-Do
        messages.warning(request, "Students are not allowed to update Homework status.")  
        return redirect("homework")

    homework.is_finished = not homework.is_finished  # Toggle status
    homework.save()

    status_message = "completed" if homework.is_finished else "marked as pending"
    messages.success(request, f"Home-Work '{homework.subject}' has been {status_message} successfully.")

    return redirect("homework")


def delete_homework(request, pk):
    homework = get_object_or_404(Homework, id=pk)

    if not request.user.is_staff:  # Only teachers can delete homework
        messages.error(request, "You are not allowed to delete homework.")
        return redirect("homework")

    homework.delete()
    messages.success(request, "Homework deleted successfully.")
    return redirect("homework")


@login_required
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '').strip()  # Get text input safely
        if text:  # If text is not empty
            youtube_url = f"https://www.youtube.com/results?search_query={text}"
            return redirect(youtube_url)  # Redirect to YouTube search results
    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, "dashboard/youtube.html", context)



@login_required
def todo(request):
    if request.method == "POST":
        if not request.user.is_staff:  # Only teachers can add To-Do
            messages.error(request, "Students are not allowed to add To-Dos.")
            return redirect("todo")

        form = TodoForm(request.POST)
        if form.is_valid():
            finished = request.POST.get("is_finished", False) == "on"
            todos = Todo(
                user=request.user,
                title=request.POST["title"],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f"To-Do added by {request.user.username}!")
            return redirect("todo")

    form = TodoForm()
    todos = Todo.objects.all()
    context = {
        "form": form,
        "todos": todos,
    }
    return render(request, "dashboard/todo.html", context)

@login_required
def update_todo(request, pk):
    todo = get_object_or_404(Todo, id=pk)

    if not request.user.is_staff:  # Only teachers can update To-Do
        messages.warning(request, "Students are not allowed to update To-Dos.")  
        return redirect("todo")

    todo.is_finished = not todo.is_finished  # Toggle status
    todo.save()

    status_message = "completed" if todo.is_finished else "marked as pending"
    messages.success(request, f"To-Do '{todo.title}' has been {status_message} successfully.")

    return redirect("todo")



@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, id=pk)

    if not request.user.is_staff:  # Only teachers can delete To-Do
        messages.error(request, "You are not allowed to delete To-Dos.")
        return redirect("todo")

    todo.delete()
    messages.success(request, "To-Do deleted successfully.")
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/books.html",context)



import os
import time
import pdfplumber
from gtts import gTTS
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.conf import settings
from .models import TexttoAudio

def generate_audio(text, output_path):
    """Generates a single MP3 file from text using gTTS."""
    tts = gTTS(text, lang='en')
    tts.save(f"{output_path}.mp3")

def listen(request):
    if request.method == "POST" and request.FILES.get("pdf_file"):
        pdf_file = request.FILES["pdf_file"]
        text_to_audio = TexttoAudio.objects.create(pdf=pdf_file)

        try:
            pdfpath = text_to_audio.pdf.path  

            if not os.path.exists(pdfpath):
                messages.warning(request, "OOPS! File not found after upload.")
                return redirect("/")

            # ✅ Extract and clean text
            text = ""
            with pdfplumber.open(pdfpath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text.strip() + " "

            text = text.replace("\n", " ")
            text = " ".join(text.split())

            if not text.strip():
                messages.warning(request, "OOPS! Sorry, your PDF file has no readable text.")
                return redirect("/")

            # ✅ Generate a unique audio filename
            unique_filename = f"audio_{int(time.time())}"
            output_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

            # ✅ Generate audio synchronously
            generate_audio(text, output_path)

            # ✅ Construct file paths
            audio_file_url = f"{settings.MEDIA_URL}{unique_filename}.mp3"
            pdf_file_url = f"{settings.MEDIA_URL}{text_to_audio.pdf.name}"  # ✅ Corrected PDF path

            return render(request, 'dashboard/audioplay.html', {
                'audio_file': audio_file_url,
                'pdf_file': pdf_file_url,
                'extracted_lines': text.split('. '),  # ✅ Split text into lines for highlighting
                'timestamp': now().timestamp()
            })

        except Exception as e:
            messages.warning(request, f"OOPS! Error: {e}")
            return redirect("/")

    return render(request, 'dashboard/uploadpdf.html')



def wiki(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip().replace(" ", "+")  # Format query for URL
        form = DashboardForm(request.POST)

        if text:
            google_url = f"https://www.google.com/search?q=site:en.wikipedia.org+{text}"
            return redirect(google_url)  # Redirects user to Google Search for Wikipedia results

    else:
        form = DashboardForm()

    return render(request, "dashboard/wiki.html", {'form': form})
    


ureg = UnitRegistry()
def conversion_home(request):
    return render(request, "dashboard/conversion.html")

async def async_translate(text, src, dest):
    translator = Translator()
    translation = await translator.translate(text, src=src, dest=dest)
    return translation.text

def language_translation(request):
    result = ""
    if request.method == "POST":
        form = LanguageTranslationForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            source = form.cleaned_data["source_lang"]
            target = form.cleaned_data["target_lang"]
            result = asyncio.run(async_translate(text, source, target))  # Fix: Use asyncio.run()

    else:
        form = LanguageTranslationForm()

    return render(request, "dashboard/language_translation.html", {"form": form, "result": result})


def math_conversion(request):
    result = ""
    if request.method == "POST":
        form = MathConversionForm(request.POST)
        if form.is_valid():
            input_value = form.cleaned_data["input_value"]
            conversion_type = form.cleaned_data["conversion_type"]

            if conversion_type == "binary":
                result = bin(int(input_value))[2:]
            elif conversion_type == "hex":
                result = hex(int(input_value))[2:]
            elif conversion_type == "simplify":
                result = str(simplify(input_value))
            elif conversion_type == "solve":
                x = symbols("x")
                equation = Eq(eval(input_value.replace("=", "-(") + ")"), 0)
                result = solve(equation, x)
    else:
        form = MathConversionForm()

    return render(request, "dashboard/math_conversion.html", {"form": form, "result": result})

def unit_conversion(request):
    result = ""
    if request.method == "POST":
        form = UnitConversionForm(request.POST)
        if form.is_valid():
            input_value = form.cleaned_data["input_value"]
            conversion_type = form.cleaned_data["conversion_type"]

            if conversion_type == "length":
                result = f"{input_value} meters = {input_value * 3.28084} feet"
            elif conversion_type == "weight":
                result = f"{input_value} kg = {input_value * 2.20462} pounds"
            elif conversion_type == "temperature":
                result = f"{input_value}°C = {(input_value * 9/5) + 32}°F"
    else:
        form = UnitConversionForm()

    return render(request, "dashboard/unit_conversion.html", {"form": form, "result": result})


@login_required
def profile(request):
    # Ensure profile exists
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'dashboard/profile.html', context)



def register(request):
    if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request,f"Account Created for {username}!!")
           return redirect("login")
    else:
       form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,"dashboard/register.html",context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')  # Get the next URL if available
            return redirect(next_url) if next_url else redirect('home')  # Redirect to the original page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


from django.contrib.auth.views import LogoutView

class auth_views(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)  # Forces logout on GET request
