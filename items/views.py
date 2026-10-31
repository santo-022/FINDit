from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
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

            return redirect('home')

    else:
        form = ItemForm()

    return render(request, 'items/report_item.html', {
        'form': form,
        'item_type': item_type,
    })