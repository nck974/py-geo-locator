"""
Localize a set of photos using the closes trackpoint from a track
"""
import os
import time

from lib.gps.bulk import read_all_gps_data_in_folder
from lib.localize import add_gps_data_to_photos

GPS_DATA_FOLDER = 'gps_data'
OUTPUT = 'dest_photos'
INPUT = 'src_photos'

if __name__ == '__main__':
    start_time = time.time()

    # Create output folder
    output = os.path.join('.',OUTPUT)
    os.makedirs(output, exist_ok=True)

    # Get gps tracks
    gps_tracks = read_all_gps_data_in_folder(GPS_DATA_FOLDER)

    # Analyze photos
    add_gps_data_to_photos(INPUT, OUTPUT, gps_tracks)

    print(f"--- {time.time() - start_time} seconds ---")
