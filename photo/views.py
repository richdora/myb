from django.shortcuts import render, redirect,  get_object_or_404
from .models import Photo
from .forms import PhotoUploadForm
from .utils import compress_image, create_thumbnail, get_lat_lon
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import exifread

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def photo_create(request, username):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()

            # Compress the uploaded image
            compress_image(photo.image)

            # Create a thumbnail for the uploaded image
            photo.thumbnail = create_thumbnail(photo.image)
            photo.save()

            # Get the latitude and longitude from the image
            image_path = photo.image.path
            lat, lon = get_lat_lon(image_path)
            photo.latitude = lat
            photo.longitude = lon
            photo.save()

            return redirect('photo_list', username=username)
    else:
        form = PhotoUploadForm()
    return render(request, 'photo/photo_create.html', {'form': form})



def photo_list(request, username):
    owner = get_object_or_404(User, username=username)
    photos = Photo.objects.filter(user=owner).order_by('-created_date')
    return render(request, 'photo/photo_list.html', {'photos': photos, 'owner': owner, })



@login_required
def photo_delete(request, username, photo_id):
    user = get_object_or_404(User, username=username)
    photo = get_object_or_404(Photo, pk=photo_id)

    if request.user == photo.user and photo.user == user:
        photo.image.delete(save=True)
        photo.delete()
        return redirect('photo_list', username=username)  # Pass the username argument
    else:
        return redirect('photo_list', username=username)  # Pass the username argument
