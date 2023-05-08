"""
Module to read all gps data in a folder
"""
import os
import re

from lib.gps.gpx import read_gpx_track
from lib.gps.tcx import read_tcx_track

from lib.model.track import GpsTrack


def read_all_gps_data_in_folder(folder: str) -> list[GpsTrack]:
    """
    This function extracts the gps data from a set of .tcx files
    For the namespace check:
    https://stackoverflow.com/questions/22464469/python-xml-xpath-query-using-tag-and-attribute-with-ns
    """
    directory = os.fsencode(folder)

    gps_tracks: list[GpsTrack] = []
    for i, file in enumerate(os.listdir(directory)):
        
        filename = os.fsdecode(file)
       # Give feedback that it is not stuck
        if i % 200 == 0:
            print(f'File {i} -> {filename}')

        if filename.endswith('.gpx'):
            gps_track = read_gpx_track(folder, file)
        elif filename.endswith('.tcx'):
            gps_track = read_tcx_track(folder, file)
        else:
            if re.search('.gitignore', filename) is None:
                print(f'The file {filename} does not match any known gps format.')
            continue

        if gps_track is not None:
            gps_tracks.append(gps_track)

    return gps_tracks
