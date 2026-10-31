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
]