import os
from PIL import Image, ExifTags



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


def create_thumbnail(image):
    with Image.open(image.path) as img:
        # Get the orientation tag from the image's EXIF data
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())

        # Rotate the image to its correct orientation
        if orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)

        # Create the thumbnail
        img.thumbnail((128, 128))

        # Save the thumbnail
        thumb_name, thumb_extension = os.path.splitext(image.path)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return ""  # Unrecognized file type

        # Save thumbnail to disk
        img.save(thumb_filename, FTYPE)

    return thumb_filename


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


