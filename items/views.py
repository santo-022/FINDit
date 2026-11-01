from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Item
from .forms import ItemForm
from recovery.models import Match
from recovery.matcher import ItemMatcher


@login_required
def report_item(request, item_type):

    if item_type not in ['LOST', 'FOUND']:
        return redirect('home')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)

            item.itemtype = item_type
            item.reported_by = request.user
            item.status = 'ACTIVE'

            item.save()

            ItemMatcher.find_matches(item)

            messages.success(request, 'Item reported successfully!')
            return redirect('home')

    else:
        form = ItemForm()

    return render(request, 'items/report_item.html', {
        'form': form,
        'item_type': item_type,
    })


@login_required
def student_dashboard(request):

    lost_items = Item.objects.filter(
        reported_by=request.user,
        itemtype='LOST'
    ).order_by('-created_at')

    found_items = Item.objects.filter(
        reported_by=request.user,
        itemtype='FOUND'
    ).order_by('-created_at')

    locked_item_ids = set()

    matches = Match.objects.filter(match_score__gt=75)

    for match in matches:
        locked_item_ids.add(match.lost_item_id)
        locked_item_ids.add(match.found_item_id)

    return render(request, 'items/student_dashboard.html', {
        'lost_items': lost_items,
        'found_items': found_items,
        'locked_item_ids': locked_item_ids,
    })


@login_required
def update_item(request, item_id):

    item = get_object_or_404(
        Item,
        id=item_id,
        reported_by=request.user
    )

    has_match = Match.objects.filter(
        lost_item=item,
        match_score__gt=75
    ).exists() or Match.objects.filter(
        found_item=item,
        match_score__gt=75
    ).exists()

    if has_match:
        messages.error(request, 'You cannot update this item because it is already in the matching process.')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.save()

            ItemMatcher.find_matches(updated_item)

            messages.success(request, 'Item updated successfully!')
            return redirect('student_dashboard')

    else:
        form = ItemForm(instance=item)

    return render(request, 'items/update_item.html', {
        'form': form,
        'item': item,
    })


@login_required
@require_POST
def delete_item(request, item_id):

    item = get_object_or_404(
        Item,
        id=item_id,
        reported_by=request.user
    )

    has_match = Match.objects.filter(
        lost_item=item,
        match_score__gt=75
    ).exists() or Match.objects.filter(
        found_item=item,
        match_score__gt=75
    ).exists()

    if has_match:
        messages.error(request, 'You cannot delete this item because it is already in the matching process.')
    else:
        item.delete()
        messages.success(request, 'Item deleted successfully!')

    return redirect('student_dashboard')
