from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Memo
from .forms import MemoForm
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def memo_list(request, owner_name):
    owner = get_object_or_404(User, username=owner_name)
    memos = Memo.objects.filter(owner=owner).order_by('-created_at')
    return render(request, 'memo/memo_list.html', {'memos': memos, 'owner': owner,})


@login_required
def memo_create(request, owner_name):
    if request.method == 'POST':
        print("Form submitted")
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.owner = request.user
            memo.save()
            return redirect(reverse('memo:memo_list', kwargs={'owner_name': owner_name}))
        else:
            print("Form errors:", form.errors)  # Add this line
    else:
        form = MemoForm()
    return render(request, 'memo/memo_create.html', {'form': form})


@login_required
def memo_update(request, owner_name, pk):
    memo = Memo.objects.get(id=pk, owner=request.user)
    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect(reverse('memo:memo_list', kwargs={'owner_name': owner_name}))
    else:
        form = MemoForm(instance=memo)
    return render(request, 'memo/memo_update.html', {'form': form})


@login_required
def memo_delete(request, owner_name, pk):
    memo = Memo.objects.get(id=pk)
    if request.user == memo.owner:
        memo.delete()
    return redirect(reverse('memo:memo_list', kwargs={'owner_name': owner_name}))


def memo_view(request, owner_name, pk):
    memo = get_object_or_404(Memo, pk=pk)
    return render(request, 'memo/memo_view.html', {'memo': memo})