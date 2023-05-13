from django.shortcuts import render, redirect,  get_object_or_404
from .models import Photo
from .forms import PhotoUploadForm
from .utils import compress_image, create_thumbnail
from django.contrib.auth.decorators import login_required
import json
from .models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from django.contrib.auth import get_user_model
CustomUser = get_user_model()


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)



def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)




def get_lat_lon(exif_data):
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = get_geotagging(exif_data).get('GPSLatitude')
        print('gps_latitude')
        print(gps_latitude)
        gps_latitude_ref = get_geotagging(exif_data).get('GPSLatitudeRef')
        print('gps_latitude_ref')
        print(gps_latitude_ref)
        gps_longitude = get_geotagging(exif_data).get('GPSLongitude')
        gps_longitude_ref = get_geotagging(exif_data).get('GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = get_decimal_from_dms(gps_latitude, gps_latitude_ref)
            lon = get_decimal_from_dms(gps_longitude, gps_longitude_ref)

    return lat, lon


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

            exif = get_exif(photo.image)
            try:
                geotags = get_geotagging(exif)
                location = get_coordinates(geotags)
                photo.latitude = location[0]
                photo.longitude = location[1]
                photo.save()
            except:
                pass

            # Add this line to assign the tags to the photo instance
            tags = form.cleaned_data['tags']
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag.name)
                tag_objects.append(tag_obj)

            photo.tags.set(tag_objects)
            photo.save()

            return redirect('photo:photo_list', username=username)
    else:
        form = PhotoUploadForm()
    return render(request, 'photo/photo_create.html', {'form': form, 'all_tags': all_tags, 'tags_json': tags_json})




@login_required
def photo_list(request, username, tag_name=None):
    owner = get_object_or_404(CustomUser, username=username)
    all_tags = Tag.objects.filter(photo__user=owner).distinct()

    if tag_name:
        selected_tag = get_object_or_404(Tag, name=tag_name)
        photos = Photo.objects.filter(user=owner, tags=selected_tag).order_by('-created_date')
    else:
        selected_tag = None
        photos = Photo.objects.filter(user=owner).order_by('-created_date')

    # Create a Paginator object
    paginator = Paginator(photos, 5)  # Show 10 photos per page

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    context = {
        'owner': owner,
        'all_tags': all_tags,
        'selected_tag': selected_tag,
        'photos': photos,
    }

    return render(request, 'photo/photo_list.html', context)

@login_required
def photo_delete(request, username, photo_id):
    user = get_object_or_404(CustomUser, username=username)
    photo = get_object_or_404(Photo, pk=photo_id)

    if request.user == photo.user and photo.user == user:
        photo.image.delete(save=True)
        photo.delete()
        return redirect('photo:photo_list', username=username)  # Pass the username argument
    else:
        return redirect('photo:photo_list', username=username)  # Pass the username argument


