from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ScheduledMatch, Note

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    interested_sport = forms.CharField(max_length=100)
    experience_level = forms.ChoiceField(choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'full_name',
            'location',
            'dob',
            'interested_sport',
            'experience_level',
            'profile_picture'
        ]


class ScheduleMatchForm(forms.ModelForm):
    class Meta:
        model = ScheduledMatch
        fields = [
            'sport',
            'title',
            'date',
            'time',
            'location',
            'players_needed',
            'cash_prize',
            'chat_link',
            'contact_number',
            'match_image'
        ]

class NoteForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Note
        fields = ['match_name', 'sport', 'date', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'placeholder': 'Write your match notes...'}),
            'match_name': forms.TextInput(attrs={'placeholder': 'Match name / opponent'}),
            'sport': forms.TextInput(attrs={'placeholder': 'Sport (e.g. Cricket, Football)'}),
        }
