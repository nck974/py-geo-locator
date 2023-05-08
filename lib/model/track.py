from dataclasses import dataclass
from datetime import datetime

from lib.utils.units import dd_to_dms


@dataclass
class GpsData():
    filename: str

@dataclass
class GpsTrackpoint():
    """
    Representation of a position in time
    """
    longitude: str
    latitude: str
    time: datetime

@dataclass
class GpsTrack():
    """
    Content of a track
    """
    min_time: datetime
    max_time: datetime
    trackpoints: list[GpsTrackpoint]
    filename: str

