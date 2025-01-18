from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile, Timetable

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']  # Allow user to update only the email.

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']  # Allow the user to update profile picture.

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['class_name', 'instructor', 'start_time', 'end_time', 'description']