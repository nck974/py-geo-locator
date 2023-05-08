import os
from datetime import datetime

from lxml import etree

from lib.model.track import GpsTrack, GpsTrackpoint


_XML_NAMESPACE = {
    "tcd": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
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
                './/tcd:Time',
                namespaces=_XML_NAMESPACE
            ).text
            trackpoint_lat_deg = trackpoint.find(
                './/tcd:Position/tcd:LatitudeDegrees',
                namespaces=_XML_NAMESPACE
            ).text
            trackpoint_lon_deg = trackpoint.find(
                './/tcd:Position/tcd:LongitudeDegrees',
                namespaces=_XML_NAMESPACE
            ).text
        except AttributeError:
            continue

        # Time comes with timezone included
        trackpoint_time = datetime.strptime(trackpoint_time, '%Y-%m-%dT%H:%M:%S%z')
        gps_trackpoints.append(
            GpsTrackpoint(
                longitude=trackpoint_lon_deg,
                latitude=trackpoint_lat_deg,
                time=trackpoint_time,
            )
        )
        track_times.add(trackpoint_time)
    return gps_trackpoints, track_times


def read_tcx_track(folder: str, file: bytes) -> GpsTrack|None:
    """
    Read a single GPS track
    """
    filename = os.fsdecode(file)
    if not filename.endswith('.tcx'):
        return None

    file_path = os.path.join(folder, filename)

    # Get all trackpoints
    root: etree._ElementTree = etree.parse(file_path, parser=None)
    trackpoints: list[etree._Element] = root.xpath(
        ".//tcd:Track/tcd:Trackpoint",
        namespaces=_XML_NAMESPACE)

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
