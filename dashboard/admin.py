from django.contrib import admin
from .models import Notes, Homework, Todo, TexttoAudio, Profile  # Import your models

# Register the models
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
admin.site.register(TexttoAudio)
admin.site.register(Profile)