from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Match, ClaimRequest, Verification, Notification


@login_required
@require_POST
def send_claim_request(request, match_id):

    match = get_object_or_404(Match, id=match_id)

    if match.lost_item.reported_by_id != request.user.id:
        messages.error(request, 'You cannot claim this item.')
        return redirect('home')

    if match.status == 'REJECTED':
        messages.error(request, 'This match was rejected.')
        return redirect('home')

    if match.match_score < 90 and match.status != 'CONFIRMED':
        messages.error(request, 'This match needs staff verification first.')
        return redirect('home')

    existing_claim = ClaimRequest.objects.filter(
        match=match,
        student=request.user,
        status__in=['PENDING', 'APPROVED']
    ).exists()

    if existing_claim:
        messages.warning(request, 'You already have a claim request.')
        return redirect('home')

    comment = request.POST.get('comment', '').strip()

    ClaimRequest.objects.create(
        match=match,
        student=request.user,
        comment=comment
    )

    messages.success(request, 'Claim request submitted successfully!')
    return redirect('home')


@login_required
@require_POST
def verify_match(request, match_id):

    if not request.user.is_staff_member:
        messages.error(request, 'Only staff can verify matches.')
        return redirect('home')

    match = get_object_or_404(Match, id=match_id)

    if not (75 < match.match_score < 90):
        messages.error(request, 'This match does not require manual verification.')
        return redirect('home')

    decision = request.POST.get('decision')

    if decision == 'APPROVE':
        match.status = 'CONFIRMED'
        match.save(update_fields=['status'])

        messages.success(request, 'Match approved.')

    elif decision == 'REJECT':
        match.status = 'REJECTED'
        match.save(update_fields=['status'])

        messages.success(request, 'Match rejected.')

    else:
        messages.error(request, 'Invalid decision.')

    return redirect('home')


@login_required
@require_POST
def review_claim(request, claim_id):

    if not request.user.is_staff_member:
        messages.error(request, 'Only staff can review claims.')
        return redirect('home')

    claim = get_object_or_404(ClaimRequest, id=claim_id)

    if claim.status != 'PENDING':
        messages.warning(request, 'This claim has already been reviewed.')
        return redirect('home')

    decision = request.POST.get('decision')
    remarks = request.POST.get('remarks', '').strip()

    if decision not in ['APPROVE', 'REJECT']:
        messages.error(request, 'Invalid decision.')
        return redirect('home')

    if decision == 'APPROVE':
        claim.status = 'APPROVED'
    else:
        claim.status = 'REJECTED'

    claim.save(update_fields=['status'])

    Verification.objects.create(
        claim=claim,
        staff=request.user,
        decision=decision + 'ED' if decision == 'APPROVE' else 'REJECTED',
        remarks=remarks
    )

    Notification.objects.create(
        recipient=claim.student,
        message=f'Your claim request has been {claim.status.lower()}.'
    )

    messages.success(request, 'Claim review completed.')

    return redirect('home')
