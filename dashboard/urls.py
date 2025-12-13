from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static
from . import views
from .views import delete_message
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.home,name="home"),
    path('chat/', views.chat_page, name='chat_page'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('notes/', views.notes,name="notes"),
    path('delete_note/<int:pk>', views.delete_note,name="delete_note"),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(),name="notes_detail"),


    path('homework/', views.homework,name="homework"),
    path('update_homework/<int:pk>', views.update_homework,name="update_homework"),
    path('delete_homework/<int:pk>', views.delete_homework,name="delete_homework"),


    path('youtube/', views.youtube,name="youtube"),

    path('todo/', views.todo,name="todo"),
    path('update_todo/<int:pk>', views.update_todo,name="update_todo"),
    path('delete_todo/<int:pk>', views.delete_todo,name="delete_todo"),


    path('books/', views.books,name="books"),
    
    path('listen/', views.listen, name='listen'),
    path('uploadpdf/', views.listen, name='uploadpdf'),
    path('audioplay/', views.listen, name='audioplay'), 

    path('wiki/', views.wiki,name="wiki"),

    path("conversion/", views.conversion_home, name="conversion"),
    path("language-translation/", views.language_translation, name="language_translation"),
    path("math-conversion/", views.math_conversion, name="math_conversion"),
    path("unit-conversion/", views.unit_conversion, name="unit_conversion"),

    path('profile/', views.profile, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='dashboard/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='dashboard/password_change_done.html'), name='password_change_done'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)