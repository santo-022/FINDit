from django.urls import path
from . import views
urlpatterns = [
    path(
        'claim/<int:match_id>/',
        views.send_claim_request,
        name='send_claim_request'
    ),

    path(
        'verify-match/<int:match_id>/',
        views.verify_match,
        name='verify_match'
    ),

    path(
        'review-claim/<int:claim_id>/',
        views.review_claim,
        name='review_claim'
    ),

    path(
        'my-matches/',
        views.match_list,
        name='match_list'
    ),

    path(
        'staff/matches/',
        views.staff_match_list,
        name='staff_match_list'
    ),

    path(
        'staff/claims/',
        views.staff_claim_list,
        name='staff_claim_list'
    ),
    path(
        'notifications/',
        views.notification_list,
        name='notification_list'
    ),
]


