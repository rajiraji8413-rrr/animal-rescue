
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('animal_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your account was created successfully!'
            )
            return redirect('animal_list')
    else:
        form = UserCreationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )
