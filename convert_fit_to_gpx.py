import time
from lib.conversion.fit import convert_all_fit_files_to_gpx

TCX_FOLDER = 'gps_data_fit'

if __name__ == '__main__':
    start_time = time.time()

    convert_all_fit_files_to_gpx(TCX_FOLDER)

    print(f"--- {time.time() - start_time} seconds ---")
