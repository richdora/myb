from django.shortcuts import render, redirect,  get_object_or_404
from .models import Photo
from .forms import PhotoUploadForm
from .utils import compress_image, create_thumbnail, get_lat_lon
from django.contrib.auth.decorators import login_required
import json
from .models import Tag


from django.contrib.auth import get_user_model
CustomUser = get_user_model()



@login_required
def photo_create(request, username):
    all_tags = Tag.objects.all().values_list('name', flat=True)
    tags_json = json.dumps(list(all_tags))

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

            # Add this line to assign the tags to the photo instance
            tags = form.cleaned_data['tags']
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag.name)
                tag_objects.append(tag_obj)

            photo.tags.set(tag_objects)
            photo.save()


            return redirect('photo_list', username=username)
    else:
        form = PhotoUploadForm()
    return render(request, 'photo/photo_create.html', {'form': form, 'all_tags': all_tags, 'tags_json': tags_json})


@login_required
def photo_list(request, username, tag_name=None):
    owner = get_object_or_404(CustomUser, username=username)
    all_tags = Tag.objects.filter(photo__user=owner).distinct()

    if tag_name:
        selected_tag = get_object_or_404(Tag, name=tag_name)
        photos = Photo.objects.filter(user=owner, tags=selected_tag)
    else:
        selected_tag = None
        photos = Photo.objects.filter(user=owner)

    return render(request, 'photo/photo_list.html', {'owner': owner, 'all_tags': all_tags, 'selected_tag': selected_tag, 'photos': photos})


@login_required
def photo_delete(request, username, photo_id):
    user = get_object_or_404(CustomUser, username=username)
    photo = get_object_or_404(Photo, pk=photo_id)

    if request.user == photo.user and photo.user == user:
        photo.image.delete(save=True)
        photo.delete()
        return redirect('photo_list', username=username)  # Pass the username argument
    else:
        return redirect('photo_list', username=username)  # Pass the username argument


