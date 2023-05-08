import time

from lib.conversion.tcx import convert_all_tcx_files_to_gpx

TCX_FOLDER = 'gps_data_tcx'

if __name__ == '__main__':
    start_time = time.time()

    convert_all_tcx_files_to_gpx(TCX_FOLDER)

    print(f"--- {time.time() - start_time} seconds ---")
