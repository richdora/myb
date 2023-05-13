import os
from PIL import Image
from django.conf import settings


def compress_image(image, max_file_size=10 * 1024 * 1024):  # 10 MB
    img = Image.open(image.path)

    # Check if the image file size is greater than the maximum allowed file size
    if os.path.getsize(image.path) > max_file_size:

        # Calculate the scale factor needed to reduce the file size
        scale_factor = (max_file_size / os.path.getsize(image.path)) ** 0.5

        # Calculate new dimensions while preserving the aspect ratio
        new_width = int(img.size[0] * scale_factor)
        new_height = int(img.size[1] * scale_factor)

        # Resize the image and save it with reduced quality to further reduce the file size
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(image.path, quality=85, optimize=True)



def create_thumbnail(image, size=(150, 150)):
    img = Image.open(image.path)
    img.thumbnail(size)

    # Create the 'thumbnails' directory if it doesn't exist
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'thumbnails'), exist_ok=True)

    thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', os.path.basename(image.path))
    img.save(thumbnail_path)

    thumbnail_url = os.path.join('thumbnails', os.path.basename(image.path))
    print(f"Thumbnail URL: {thumbnail_url}")

    return os.path.join('thumbnails', os.path.basename(image.path))


import exifread


def get_lat_lon(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)

        try:
            lat = tags['GPS GPSLatitude']
            lon = tags['GPS GPSLongitude']

            lat = [float(x.num) / float(x.den) for x in lat.values]
            lon = [float(x.num) / float(x.den) for x in lon.values]

            latref = tags['GPS GPSLatitudeRef'].values
            lonref = tags['GPS GPSLongitudeRef'].values

            lat = lat[0] + lat[1] / 60 + lat[2] / 3600
            lon = lon[0] + lon[1] / 60 + lon[2] / 3600

            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon

            return lat, lon
        except KeyError:
            return None, None


