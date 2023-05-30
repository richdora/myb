from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Now

@login_required
def create_view(request, username):
    if request.method == "POST":
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        timestamp = request.POST.get('timestamp')
        now = Now(owner=request.user, latitude=lat, longitude=lon, timestamp=timestamp)
        now.save()
        return redirect('now:index')  # replace with the actual name of the page you want to redirect to after saving
    else:
        return render(request, 'now/create_now.html')  # replace 'now/create.html' with your actual template path



def now_list(request, username):
    nows = Now.objects.filter(owner=request.user).order_by('-timestamp')
    return render(request, 'myapp/now_list.html', {'nows': nows})
