from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Memo, Tag
from .forms import MemoForm
from django.urls import reverse
import json

from django.contrib.auth import get_user_model
User = get_user_model()


def memo_list(request, owner_name, tag_name=None):
    owner = get_object_or_404(User, username=owner_name)
    all_tags = Tag.objects.filter(memo__owner=owner).distinct()

    if tag_name:
        selected_tag = get_object_or_404(Tag, name=tag_name)
        memos = Memo.objects.filter(owner=owner, tags=selected_tag).order_by('-created_at')
    else:
        selected_tag = None
        memos = Memo.objects.filter(owner=owner).order_by('-created_at')

    context = {
        'owner': owner,
        'all_tags': all_tags,
        'selected_tag': selected_tag,
        'memos': memos,
    }
    return render(request, 'memo/memo_list.html', context)








@login_required
def memo_create(request, owner_name):
    all_tags = Tag.objects.all().values_list('name', flat=True)
    tags_json = json.dumps(list(all_tags))

    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.owner = request.user
            memo.save()


            # Add this line to assign the tags to the memo instance
            tags = form.cleaned_data['tags']
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag.name)
                tag_objects.append(tag_obj)

            memo.tags.set(tag_objects)
            memo.save()

            return redirect(reverse('memo:memo_list', kwargs={'owner_name': owner_name}))

    else:
        form = MemoForm()
    return render(request, 'memo/memo_create.html', {'form': form,  'all_tags': all_tags, 'tags_json': tags_json,})



@login_required
def memo_update(request, owner_name, pk):
    memo = Memo.objects.get(id=pk, owner=request.user)
    if request.method == 'POST':
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            form.save_m2m()  # This saves the tags.
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