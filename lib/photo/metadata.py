
from datetime import datetime, timedelta

from PIL import Image, ExifTags
import pytz


def get_photo_capture_time(filename: str|bytes) -> datetime|None:
    """
    Return when was the photo taken according to the take date.
    """
    img = Image.open(filename)
    exif_data = img.getexif()
    if exif_data is not None or exif_data != {}:
        for key, val in exif_data.items():
            if key in ExifTags.TAGS and ExifTags.TAGS[key] == 'DateTime':
                capture_date = datetime.strptime(val, r'%Y:%m:%d %H:%M:%S')

                # Capture date does not have timezone in the standard
                capture_date = pytz.timezone('Europe/Berlin').localize(
                    capture_date) - timedelta(hours=0)

                return capture_date

    print(f'"{filename}" does not have exif data')
    return None
