import os
from datetime import datetime

from lxml import etree

from lib.model.track import GpsTrack, GpsTrackpoint


_XML_NAMESPACE = {
    "top": "http://www.topografix.com/GPX/1/1",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}


def _get_trackpoints_from_track(
        trackpoints: list[etree._Element]
    ) -> tuple[list[GpsTrackpoint], set[datetime]]:
    """
    Extract the points and time of the read track
    """
    gps_trackpoints: list[GpsTrackpoint] = []
    track_times: set[datetime] = set()
    for trackpoint in trackpoints:

        try:
            trackpoint_time = trackpoint.find(
                './/top:time',
                namespaces=_XML_NAMESPACE
            ).text
            trackpoint_lat_deg = trackpoint.attrib.get('lat')
            trackpoint_lon_deg = trackpoint.attrib.get('lon')
        except AttributeError:
            print('Attribute not found')
            continue

        # Time comes with timezone included
        trackpoint_time = datetime.strptime(trackpoint_time, r'%Y-%m-%dT%H:%M:%S%z')
        gps_trackpoints.append(
            GpsTrackpoint(
                longitude=trackpoint_lon_deg,
                latitude=trackpoint_lat_deg,
                time=trackpoint_time,
            )
        )
        track_times.add(trackpoint_time)
    return gps_trackpoints, track_times


def read_gpx_track(folder: str, file: bytes) -> GpsTrack|None:
    """
    Read a single GPS track
    """
    filename = os.fsdecode(file)
    if not filename.endswith('.gpx'):
        return None

    file_path = os.path.join(folder, filename)

    # Get all trackpoints
    root: etree._ElementTree = etree.parse(file_path, parser=None)
    trackpoints: list[etree._Element] = root.xpath(
        ".//top:trkseg/top:trkpt",
        namespaces=_XML_NAMESPACE
        )

    # Extract lat, lon and time from each trackpoint
    try:
        gps_trackpoints, track_times = _get_trackpoints_from_track(trackpoints)
    except AttributeError:
        return None

    # If no valid point is found ignore the file
    if len(gps_trackpoints) == 0:
        return None

    return GpsTrack(
        min_time=min(track_times),
        max_time=max(track_times),
        trackpoints=gps_trackpoints,
        filename=filename
    )


def read_all_gps_data(folder: str) -> list[GpsTrack]:
    """
    This function extracts the gps data from a set of .tcx files
    For the namespace check:
    https://stackoverflow.com/questions/22464469/python-xml-xpath-query-using-tag-and-attribute-with-ns
    """
    directory = os.fsencode(folder)

    gps_tracks: list[GpsTrack] = []
    for i, file in enumerate(os.listdir(directory)):

       # Give feedback that it is not stuck
        if i % 200 == 0:
            print(f'File {i} -> {os.fsdecode(file)}')

        gps_track = read_gpx_track(folder, file)

        if gps_track is not None:
            # print(f'Max: {gps_track.max_time}, Min: {gps_track.min_time}, File: {gps_track.filename}')
            gps_tracks.append(gps_track)

    return gps_tracks
