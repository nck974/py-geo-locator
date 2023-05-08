import os
from lib.gps.utils import get_closest_trackpoint
from lib.photo.edit_location import edit_location_exif_data_raw
from lib.photo.metadata import get_photo_capture_time

from lib.model.track import GpsTrack


def _is_valid_file(filename: str) -> bool:
    """
    Check if the file has one of the accepted formats
    """
    if any([
        filename.endswith('.cr2'),
        filename.endswith('.CR2'),
        filename.endswith('.jpg'),
        filename.endswith('.png'),
    ]):
        return True
    
    return False


def add_gps_data_to_photos(photos_folder: str, output: str, gps_tracks: list[GpsTrack]):

    directory = os.fsencode(os.path.join('.', photos_folder))
    
    print(f'Files in directory: {len(os.listdir(directory))}')

    for i, file in enumerate(os.listdir(directory)):
       
        filename = os.fsdecode(file)
        print(f'File {i} -> {filename}')
        
        if not _is_valid_file(filename):
            print(f'{filename} is not an image file and will be skipped')
            continue
        
        file_path = os.path.join(directory, file)

        capture_time = get_photo_capture_time(file_path)
        # Skip files without capture time as they can not be allocated
        if capture_time is None:
            continue

        for gps_track in gps_tracks:
            # Check if capture time is between track limits
            if capture_time > gps_track.min_time and capture_time < gps_track.max_time:
                closest_trackpoint = get_closest_trackpoint(gps_track.trackpoints, capture_time)
                
                print(f'--> [SUCCESS] Photo {filename} is in gps track "{gps_track.filename}"')
                print(f'----> Time taken: "{capture_time}"')
                print(f'----> Longitude {closest_trackpoint.longitude}')
                print(f'----> Latitude {closest_trackpoint.latitude}')
                print(f'------> Google "{closest_trackpoint.latitude},{closest_trackpoint.longitude}"')

                # if filename.endswith('.cr2') or filename.endswith('.CR2'):
                edit_location_exif_data_raw(file_path.decode(encoding='utf8'), output, closest_trackpoint)
                # else:
                    # _edit_location_exif_data(file_path, closest_trackpoint)