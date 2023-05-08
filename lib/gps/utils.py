from datetime import datetime
from lib.model.track import GpsTrackpoint


def get_closest_trackpoint(
    trackpoints: list[GpsTrackpoint], capture_time: datetime
    ) -> GpsTrackpoint:
    """
    Return the closest trackpoint to the given date
    """
    for trackpoint in trackpoints:
        if capture_time > trackpoint.time:
            continue
        return trackpoint

    raise RuntimeError('No closest point could be found')
