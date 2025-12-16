from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views   # ✅ SAFE IMPORT (IMPORTANT)

urlpatterns = [

    # ================= HOME =================
    path('', views.home, name="home"),

    # ================= CHAT =================
    path('chat/', views.chat_page, name='chat_page'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path(
        'delete_message/<int:message_id>/',
        views.delete_message,
        name='delete_message'
    ),

    # ================= NOTES =================
    path('notes/', views.notes, name="notes"),
    path('notes_detail/<int:pk>/', views.NotesDetailView.as_view(), name="notes_detail"),

    # ================= HOMEWORK =================
    path('homework/', views.homework, name="homework"),

    # ================= TODO =================
    path('todo/', views.todo, name="todo"),

    # ================= YOUTUBE =================
    path('youtube/', views.youtube, name="youtube"),

    # ================= BOOKS =================
    path('books/', views.books, name="books"),

    # ================= PDF TO AUDIO =================
    path('listen/', views.listen, name='listen'),
    path('uploadpdf/', views.listen, name='uploadpdf'),
    path('audioplay/', views.listen, name='audioplay'),

    # ================= WIKI =================
    path('wiki/', views.wiki, name="wiki"),

    # ================= CONVERSIONS =================
    path("language-translation/", views.language_translation, name="language_translation"),
    path("math-conversion/", views.math_conversion, name="math_conversion"),
    path("unit-conversion/", views.unit_conversion, name="unit_conversion"),

    # ================= AUTH & PROFILE =================
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='dashboard/password_change.html'
        ),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='dashboard/password_change_done.html'
        ),
        name='password_change_done'
    ),
]

# ================= MEDIA =================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
