from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SellItem
from .forms import SellItemForm

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def sell_create(request, owner_name):
    owner = get_object_or_404(User, username=owner_name)
    if request.method == 'POST':
        form = SellItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = owner
            item.save()
            return redirect('sell:sell_list', owner_name=owner.username)
    else:
        form = SellItemForm()
    return render(request, 'sell/sell_create.html', {'form': form, 'owner': owner})

@login_required
def sell_update(request, owner_name, pk):
    owner = get_object_or_404(User, username=owner_name)
    item = get_object_or_404(SellItem, pk=pk, owner=owner)
    if request.method == 'POST':
        form = SellItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sell:sell_list', owner_name=owner.username)
    else:
        form = SellItemForm(instance=item)
    return render(request, 'sell/sell_update.html', {'form': form, 'owner': owner})

@login_required
def sell_delete(request, owner_name, pk):
    owner = get_object_or_404(User, username=owner_name)
    item = get_object_or_404(SellItem, pk=pk, owner=owner)
    if request.method == 'POST':
        item.delete()
        return redirect('sell:sell_list', owner_name=owner.username)
    return render(request, 'sell/sell_delete.html', {'item': item, 'owner': owner})


def sell_list(request, owner_name):
    owner = get_object_or_404(User, username=owner_name)
    items = SellItem.objects.filter(owner=owner).order_by('-created_date')
    return render(request, 'sell/sell_list.html', {'items': items, 'owner': owner})

