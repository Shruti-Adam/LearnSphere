from django import forms
from django.forms import widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'



class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Search: ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class TextForm(forms.ModelForm):
    class Meta:
        model=TexttoAudio
        fields="__all__"


LANGUAGE_CHOICES = [("en", "English"), ("mr", "Marathi"), ("hi", "Hindi")]
MATH_CONVERSIONS = [("binary", "Decimal to Binary"), ("hex", "Decimal to Hexadecimal"), ("simplify", "Simplify Expression"), ("solve", "Solve Equation")]
UNIT_CONVERSIONS = [("length", "Length (m ↔ ft)"), ("weight", "Weight (kg ↔ lb)"), ("temperature", "Temperature (C ↔ F)")]

class LanguageTranslationForm(forms.Form):
    text = forms.CharField(label="Enter Text", widget=forms.Textarea)
    source_lang = forms.ChoiceField(choices=LANGUAGE_CHOICES, label="From Language")
    target_lang = forms.ChoiceField(choices=LANGUAGE_CHOICES, label="To Language")

class MathConversionForm(forms.Form):
    input_value = forms.CharField(label="Enter Number/Expression")
    conversion_type = forms.ChoiceField(choices=MATH_CONVERSIONS, label="Conversion Type")

class UnitConversionForm(forms.Form):
    input_value = forms.FloatField(label="Enter Value")
    conversion_type = forms.ChoiceField(choices=UNIT_CONVERSIONS, label="Conversion Type")
    

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']