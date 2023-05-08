import os

from lib.model.track import GpsTrackpoint
from lib.utils.units import dd_to_dms

MODIFY_RAW_SCRIPT = 'modify_raw_location_metadata.pl'

def _get_deg_min_sec_for_exif_tool(
        trackpoint: GpsTrackpoint
    ) -> tuple[dict[str, float], dict[str, float]]:
    """
    Return the parameters required to set the gps coordinates using perl's library
    Image::Exiftool
    """
    latitude_sign, latitude_deg = dd_to_dms(float(trackpoint.latitude))
    longitude_sign, longitude_deg = dd_to_dms(float(trackpoint.longitude))
    lat = {
        'lat_deg': latitude_deg[0],
        'lat_min': latitude_deg[1],
        'lat_sec': latitude_deg[2],
        'lat_sign': -1 if latitude_sign else 1
    }
    lon = {
        'lon_deg': longitude_deg[0],
        'lon_min': longitude_deg[1],
        'lon_sec': longitude_deg[2],
        'lon_sign': -1 if longitude_sign else 1
    }

    return (lon, lat)



def edit_location_exif_data_raw(path: str, output: str, trackpoint: GpsTrackpoint) -> None:
    """
    Edit the image exif data using the perl library Image::Exiftool
    """
    perl_script = os.path.join(
        os.path.dirname(__file__),
        '..', '..', 'tools',
        MODIFY_RAW_SCRIPT
    )

    lat, lon = _get_deg_min_sec_for_exif_tool(trackpoint)
    output = os.path.join(
        output,
        os.path.basename(path)
    )
    cmd = f'perl {perl_script} --input "{path}" --output "{output}"'
    for coord in [lat, lon]:
        for key, value in coord.items():
            cmd = cmd + f' --{key} "{value}"'

    print(f'Executing:\n{cmd}')
    os.system(cmd)