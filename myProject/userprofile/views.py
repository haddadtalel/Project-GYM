from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Profile, ProfileForm, ProfilePictureForm, PasswordForm,Timetable, TimetableForm




@login_required
def profile_view(request):
    # Fetch the user's profile
    user = request.user
    profile = Profile.objects.get(user=user)

    # Handle form submissions for updating email, profile picture, and password
    if request.method == 'POST':
        email_form = ProfileForm(request.POST, instance=user)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordForm(request.user, request.POST)

        if 'email_submit' in request.POST:
            # Handle email update
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully!")
                return redirect('profile')

        if 'profile_picture_submit' in request.POST:
            # Handle profile picture update
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                messages.success(request, "Profile picture updated successfully!")
                return redirect('profile')

        if 'password_submit' in request.POST:
            # Handle password change
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
                messages.success(request, "Password updated successfully!")
                return redirect('profile')

    else:
        email_form = ProfileForm(instance=user)
        profile_picture_form = ProfilePictureForm(instance=profile)
        password_form = PasswordForm(request.user)

    return render(request, 'userprofile/profile.html', {
        'user': user,
        'profile': profile,
        'email_form': email_form,
        'profile_picture_form': profile_picture_form,
        'password_form': password_form,
    })
@login_required
def timetable_view(request):
    # Fetch the user's profile and their timetable
    user = request.user
    timetable_entries = Timetable.objects.filter(user=user)

    if request.method == 'POST':
        timetable_form = TimetableForm(request.POST)

        if timetable_form.is_valid():
            # Save the new timetable entry for the user
            new_timetable_entry = timetable_form.save(commit=False)
            new_timetable_entry.user = user
            new_timetable_entry.save()
            messages.success(request, "Timetable entry added successfully!")
            return redirect('timetable')

    else:
        timetable_form = TimetableForm()

    return render(request, 'userprofile/timetable.html', {
        'user': user,
        'timetable_entries': timetable_entries,
        'timetable_form': timetable_form,
    })
