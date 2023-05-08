import os

from tcx2gpx import tcx2gpx
from lxml.etree import XMLSyntaxError

def _cleanup_heading_spaces(file: str) -> None:
    """
    It seems that some exported files contain heading white spaces which will trigger a 
    XMLSyntaxError exception in lxml when trying to convert them.
    """
    with open(file=file, mode='r', encoding='utf8') as f:
        content = f.read()    
    content = content.strip()
    with open(file=file, mode='w', encoding='utf8') as f:
        f.write(content)


def convert_tcx_file_to_gpx(file: str) -> None:
    """
    Convert a file from tcx to gpx using the external library tcx2gpx
    """ 
    _cleanup_heading_spaces(file)
    gps_object = tcx2gpx.TCX2GPX(tcx_path=file)
    gps_object.convert()


def convert_all_tcx_files_to_gpx(folder: str) -> None:
    """
    This function converts all data from tcx to gpx using the external library tcx2gpx
    """
    directory = os.fsencode(folder)

    for i, file in enumerate(os.listdir(directory)):

        filename = os.fsdecode(file)

        if not filename.endswith('.tcx'):
            continue
 
        # Give feedback that it is not stuck
        if i % 200 == 0:
            print(f'File {i} -> {filename}')

        try:
            convert_tcx_file_to_gpx(os.path.join(folder, filename))
        except (XMLSyntaxError, AttributeError) as e:
            print(f'{filename} could not be converted.')
            raise e
