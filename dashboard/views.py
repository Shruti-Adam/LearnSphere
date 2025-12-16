from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import localtime, now
from django.views import generic
from collections import defaultdict
import os, time, asyncio

from .forms import (
    NotesForm, HomeworkForm, TodoForm, DashboardForm,
    UserRegistrationForm, LanguageTranslationForm,
    MathConversionForm, UnitConversionForm,
    UserUpdateForm, ProfileUpdateForm
)
from .models import Notes, Homework, Todo, ChatMessage, TexttoAudio, Profile


# ================= HOME =================
def home(request):
    return render(request, 'dashboard/home.html')


# ================= CHAT =================
@login_required
def chat_page(request):
    return render(request, 'dashboard/chat.html')


@login_required
def send_message(request):
    if request.method == 'POST':
        msg = ChatMessage.objects.create(
            sender=request.user,
            message=request.POST.get('message')
        )
        return JsonResponse({
            'id': msg.id,
            'message': msg.message,
            'sender': msg.sender.username,
            'time': localtime(msg.timestamp).strftime('%I:%M %p')
        })


@login_required
def get_messages(request):
    messages_qs = ChatMessage.objects.all().order_by('timestamp')
    grouped = defaultdict(list)

    for m in messages_qs:
        date = localtime(m.timestamp).strftime('%d %B %Y')
        grouped[date].append({
            'id': m.id,
            'sender': m.sender.username,
            'message': m.message,
            'time': localtime(m.timestamp).strftime('%I:%M %p'),
            'is_owner': m.sender == request.user
        })

    return JsonResponse({'messages': grouped})


# ================= NOTES =================
@login_required
def notes(request):
    if request.method == "POST" and request.user.is_staff:
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully")
        return redirect('notes')

    return render(request, 'dashboard/notes.html', {
        'notes': Notes.objects.all(),
        'form': NotesForm()
    })


class NotesDetailView(generic.DetailView):
    model = Notes


# ================= HOMEWORK =================
@login_required
def homework(request):
    if request.method == "POST" and request.user.is_staff:
        form = HomeworkForm(request.POST)
        if form.is_valid():
            hw = form.save(commit=False)
            hw.user = request.user
            hw.save()
            messages.success(request, "Homework added")
        return redirect("homework")

    return render(request, "dashboard/homework.html", {
        "homeworks": Homework.objects.all(),
        "form": HomeworkForm()
    })


# ================= TODO =================
@login_required
def todo(request):
    if request.method == "POST" and request.user.is_staff:
        form = TodoForm(request.POST)
        if form.is_valid():
            td = form.save(commit=False)
            td.user = request.user
            td.save()
            messages.success(request, "Todo added")
        return redirect("todo")

    return render(request, "dashboard/todo.html", {
        "todos": Todo.objects.all(),
        "form": TodoForm()
    })


# ================= YOUTUBE =================
@login_required
def youtube(request):
    if request.method == "POST":
        text = request.POST.get('text')
        return redirect(f"https://www.youtube.com/results?search_query={text}")
    return render(request, "dashboard/youtube.html", {"form": DashboardForm()})


# ================= BOOKS =================
def books(request):
    import requests

    if request.method == "POST":
        text = request.POST['text']
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
        data = requests.get(url).json()

        results = []
        for i in range(5):
            info = data['items'][i]['volumeInfo']
            results.append({
                'title': info.get('title'),
                'thumbnail': info.get('imageLinks', {}).get('thumbnail'),
                'preview': info.get('previewLink')
            })

        return render(request, 'dashboard/books.html', {'results': results})

    return render(request, 'dashboard/books.html')


# ================= PDF TO AUDIO =================
@login_required
def listen(request):
    import pdfplumber
    from gtts import gTTS
    from django.conf import settings

    if request.method == "POST" and request.FILES.get("pdf_file"):
        obj = TexttoAudio.objects.create(pdf=request.FILES['pdf_file'])
        text = ""

        with pdfplumber.open(obj.pdf.path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()

        filename = f"audio_{int(time.time())}.mp3"
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)

        gTTS(text).save(audio_path)

        return render(request, 'dashboard/audioplay.html', {
            'audio': settings.MEDIA_URL + filename
        })

    return render(request, 'dashboard/uploadpdf.html')


# ================= WIKI =================
def wiki(request):
    if request.method == "POST":
        q = request.POST.get('text')
        return redirect(f"https://www.google.com/search?q=site:wikipedia.org+{q}")
    return render(request, "dashboard/wiki.html")


# ================= LANGUAGE TRANSLATION =================
def language_translation(request):
    result = ""
    if request.method == "POST":
        from googletrans import Translator

        form = LanguageTranslationForm(request.POST)
        if form.is_valid():
            translator = Translator()
            result = translator.translate(
                form.cleaned_data['text'],
                src=form.cleaned_data['source_lang'],
                dest=form.cleaned_data['target_lang']
            ).text
    else:
        form = LanguageTranslationForm()

    return render(request, "dashboard/language_translation.html", {
        "form": form,
        "result": result
    })


# ================= MATH & UNIT =================
def math_conversion(request):
    from sympy import symbols, Eq, solve, simplify

    result = ""
    if request.method == "POST":
        form = MathConversionForm(request.POST)
        if form.is_valid():
            val = form.cleaned_data['input_value']
            result = simplify(val)

    return render(request, "dashboard/math_conversion.html", {
        "form": MathConversionForm(),
        "result": result
    })


def unit_conversion(request):
    result = ""
    if request.method == "POST":
        form = UnitConversionForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data['input_value'] * 3.28

    return render(request, "dashboard/unit_conversion.html", {
        "form": UnitConversionForm(),
        "result": result
    })


# ================= PROFILE =================
@login_required
def profile(request):
    Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "dashboard/profile.html", {
        "u_form": u_form,
        "p_form": p_form
    })


# ================= AUTH =================
def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "dashboard/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials")

    return render(request, "login.html")

from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)

    # Allow only the sender to delete their own message
    if message.sender != request.user:
        return JsonResponse(
            {'error': 'Permission denied'},
            status=403
        )

    message.delete()
    return JsonResponse({'status': 'deleted'})

