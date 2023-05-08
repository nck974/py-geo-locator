# py-geo-locator

This program takes as input a set of images and gps tracks. If the image was taken during a track the closest position in the track will be saved in the EXIF data of the image. This library is written in python, excluding the library that writes the metadata into the EXIF file which is in perl (the available python libraries did not work so well with RAW photos).

## Prerequisites

1. Perl is installed.
1. Python >3.10 is installed.

## Installation

1. Pull the project
1. Install perl library `cpan -i Image::ExifTool`:
1. Install python requirements `pip install -r requirements.txt`.

## Usage

1. Place your gps tracks in `gps_data` folder.
1. Place your photos in `src_photos` folder.
1. Execute `geolocalize_photos.py`.
1. The photos that could be geolocalized will be placed in `dest_photos`.

## Fit data

Strava seems to store some old imported data as `.fit.gz`. First you can use `7zip` in windows or something similar in other OS to extract all `.gz` to `.fit`.

To convert them to gpx just copy the `.fit` files in the folder `gps_data_fit` and run `python .\convert_fit_to_gpx.py`.

Conversion is done by the external library [fit2gpx](https://pypi.org/project/fit2gpx/).

## TCX data

Strava seems to store some old imported data as `.tcx.gz`. First you can use `7zip` in windows or something similar in other OS to extract all `.gz` to `.tcx`.

To convert them to gpx just copy the `.tcx` files in the folder `gps_data_tcx` and run `python .\convert_tcx_to_gpx.py`.

Conversion is done by the external library [tcx2gpx](https://pypi.org/project/tcx2gpx/).

## Limitations

1. Currently only jpg, png, and canon RAW data is supported. Although I guess it should also work with other formats is the file suffix is accepted, feel free to send a PR to add additional formats.
1. Some old photos did not have timezones in the EXIF data which may make it harder to match the correct gps data, `lib\photo\metadata.py` contains a function to play with the timezone and find the correct point for that old data.
