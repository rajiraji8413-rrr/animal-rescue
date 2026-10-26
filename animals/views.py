
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Animal, Species, Breed, Location, AdoptionRequest
from .forms import AdoptionRequestForm, ProfileForm
from .email_utils import send_adoption_email


def animal_list(request):
    animals = Animal.objects.select_related(
        'species', 'breed', 'location'
    ).all()

    search_query = request.GET.get('q', '').strip()
    selected_species = request.GET.get('species', '')
    selected_breed = request.GET.get('breed', '')
    selected_gender = request.GET.get('gender', '')
    selected_location = request.GET.get('location', '')
    selected_status = request.GET.get('status', '')

    if search_query:
        animals = animals.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(species__name__icontains=search_query)
            | Q(breed__name__icontains=search_query)
            | Q(location__name__icontains=search_query)
        )

    if selected_species:
        animals = animals.filter(species_id=selected_species)

    if selected_breed:
        animals = animals.filter(breed_id=selected_breed)

    if selected_gender:
        animals = animals.filter(gender=selected_gender)

    if selected_location:
        animals = animals.filter(location_id=selected_location)

    if selected_status:
        animals = animals.filter(status=selected_status)

    animals = animals.order_by('id')

    paginator = Paginator(animals, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'animals': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'species_list': Species.objects.all(),
        'breeds': Breed.objects.all(),
        'locations': Location.objects.all(),
        'selected_species': selected_species,
        'selected_breed': selected_breed,
        'selected_gender': selected_gender,
        'selected_location': selected_location,
        'selected_status': selected_status,
    }

    return render(request, 'animals/animal_list.html', context)


def animal_detail(request, animal_id):
    animal = get_object_or_404(
        Animal.objects.select_related(
            'species', 'breed', 'location'
        ),
        id=animal_id
    )

    return render(
        request,
        'animals/animal_detail.html',
        {'animal': animal}
    )


@login_required
def adoption_request(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    if animal.status != 'Available':
        messages.error(
            request,
            'This animal is not currently available for adoption.'
        )
        return redirect('animal_detail', animal_id=animal.id)

    existing_request = AdoptionRequest.objects.filter(
        animal=animal,
        applicant=request.user,
        status='Pending'
    ).exists()

    if existing_request:
        messages.warning(
            request,
            'You already have a pending adoption request for this animal.'
        )
        return redirect('animal_detail', animal_id=animal.id)

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)

        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.animal = animal
            adoption.applicant = request.user
            adoption.save()

            messages.success(
                request,
                'Your adoption request was submitted successfully.'
            )

            return redirect('my_adoption_requests')
    else:
        form = AdoptionRequestForm()

    return render(
        request,
        'animals/adoption_request.html',
        {
            'animal': animal,
            'form': form,
        }
    )


@login_required
def my_adoption_requests(request):
    requests_list = AdoptionRequest.objects.filter(
        applicant=request.user
    ).select_related('animal').order_by('-created_at')

    selected_status = request.GET.get('status', '').strip()
    valid_statuses = ['Pending', 'Approved', 'Rejected']

    if selected_status in valid_statuses:
        requests_list = requests_list.filter(status=selected_status)
    else:
        selected_status = ''

    context = {
        'adoption_requests': requests_list,
        'selected_status': selected_status,
    }

    return render(
        request,
        'animals/my_adoption_requests.html',
        context
    )


@login_required
def user_profile(request):
    profile_user = request.user

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            instance=profile_user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your profile was updated successfully.'
            )

            return redirect('user_profile')
    else:
        form = ProfileForm(instance=profile_user)

    adoption_requests = AdoptionRequest.objects.filter(
        applicant=profile_user
    )

    context = {
        'profile_user': profile_user,
        'form': form,
        'total_requests': adoption_requests.count(),
        'pending_requests': adoption_requests.filter(
            status='Pending'
        ).count(),
        'approved_requests': adoption_requests.filter(
            status='Approved'
        ).count(),
        'rejected_requests': adoption_requests.filter(
            status='Rejected'
        ).count(),
    }

    return render(
        request,
        'animals/user_profile.html',
        context
    )


@login_required
def dashboard(request):
    recent_requests = AdoptionRequest.objects.select_related(
        'animal', 'applicant'
    ).order_by('-created_at')[:5]

    context = {
        'total_animals': Animal.objects.count(),
        'available_animals': Animal.objects.filter(
            status='Available'
        ).count(),
        'adopted_animals': Animal.objects.filter(
            status='Adopted'
        ).count(),
        'pending_requests': AdoptionRequest.objects.filter(
            status='Pending'
        ).count(),
        'recent_requests': recent_requests,
    }

    return render(request, 'animals/dashboard.html', context)


@staff_member_required
@require_POST
def manage_adoption_request(request, request_id):
    print("MANAGE ADOPTION REQUEST VIEW CALLED")
    adoption = get_object_or_404(
        AdoptionRequest.objects.select_related(
            'animal', 'applicant'
        ),
        id=request_id
    )

    action = request.POST.get('action')

    if adoption.status != 'Pending':
        messages.warning(
            request,
            'This adoption request has already been processed.'
        )
        return redirect('manage_adoptions')

    if action == 'approve':
        adoption.status = 'Approved'
        adoption.save()

        adoption.animal.status = 'Adopted'
        adoption.animal.save()

        email_subject = 'Animal Rescue - Adoption Request Approved'
        email_message = (
            f"Hello {adoption.applicant.username},\n\n"
            f"Good news! Your adoption request for "
            f"{adoption.animal.name} has been approved.\n\n"
            "Thank you for choosing to adopt and give an animal "
            "a loving home.\n\n"
            "Regards,\nAnimal Rescue Team"
        )

        messages.success(
            request,
            'Adoption request approved successfully.'
        )

    elif action == 'reject':
        adoption.status = 'Rejected'
        adoption.save()

        email_subject = 'Animal Rescue - Adoption Request Update'
        email_message = (
            f"Hello {adoption.applicant.username},\n\n"
            f"Your adoption request for {adoption.animal.name} "
            "has been rejected at this time.\n\n"
            "Thank you for your interest in Animal Rescue.\n\n"
            "Regards,\nAnimal Rescue Team"
        )

        messages.success(
            request,
            'Adoption request rejected successfully.'
        )

    else:
        messages.error(request, 'Invalid action.')
        return redirect('manage_adoptions')

    recipient_email = adoption.applicant.email

    if recipient_email:
        success, details = send_adoption_email(
            recipient_email,
            email_subject,
            email_message
        )

        if success:
            messages.success(
                request,
                'Mailtrap accepted the email notification.'
            )
        else:
            print(f"Adoption email error: {details}")
            messages.warning(
                request,
                'The adoption status was updated, but the email '
                'could not be sent. Check the terminal for details.'
            )
    else:
        messages.warning(
            request,
            'The adoption status was updated, but the applicant '
            'has no email address in their account.'
        )

    return redirect('manage_adoptions')


@staff_member_required
def manage_adoptions(request):
    adoption_requests = AdoptionRequest.objects.select_related(
        'animal',
        'applicant',
        'animal__species',
    ).order_by('-created_at')

    selected_status = request.GET.get('status', '').strip()
    valid_statuses = ['Pending', 'Approved', 'Rejected']

    if selected_status in valid_statuses:
        adoption_requests = adoption_requests.filter(status=selected_status)
    else:
        selected_status = ''

    context = {
        'adoption_requests': adoption_requests,
        'selected_status': selected_status,
    }

    return render(
        request,
        'animals/manage_adoptions.html',
        context
    )
