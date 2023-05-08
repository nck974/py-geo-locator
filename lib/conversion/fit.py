import os
import re

from fit2gpx import Converter


def convert_fit_file_to_gpx(folder: str, filename: str) -> None:
    """
    Convert a file from fit to gpx using the external library fit2gpx
    """
    conv = Converter()
    gpx = conv.fit_to_gpx(
        f_in=os.path.join(folder, filename),
        f_out=os.path.join(folder, re.sub(r'\.fit$', '.gpx', filename))
    )


def convert_all_fit_files_to_gpx(folder: str) -> None:
    """
    This function converts all data from fit to gpx using the external library fit2gpx
    """
    directory = os.fsencode(folder)

    for i, file in enumerate(os.listdir(directory)):

        filename = os.fsdecode(file)

        if not filename.endswith('.fit'):
            continue

        # Give feedback that it is not stuck
        if i % 200 == 0:
            print(f'File {i} -> {filename}')

        convert_fit_file_to_gpx(folder, filename)
