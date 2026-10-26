
from django.urls import path
from . import views

urlpatterns = [
    # Animal listing page
    path(
        "",
        views.animal_list,
        name="animal_list",
    ),

    # Animal details page
    path(
        "<int:animal_id>/",
        views.animal_detail,
        name="animal_detail",
    ),

    # Submit an adoption request
    path(
        "<int:animal_id>/adopt/",
        views.adoption_request,
        name="adoption_request",
    ),

    # User's adoption requests
    path(
        "my-requests/",
        views.my_adoption_requests,
        name="my_adoption_requests",
    ),

    # User profile
    path(
        "profile/",
        views.user_profile,
        name="user_profile",
    ),

    # Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    # Admin adoption management page
    path(
        "manage-adoptions/",
        views.manage_adoptions,
        name="manage_adoptions",
    ),

    # Approve or reject an adoption request
    path(
        "manage-request/<int:request_id>/",
        views.manage_adoption_request,
        name="manage_adoption_request",
    ),
]
