=item modify_raw_location_metadata

This library adds the location to the exif data of a raw file using Image::ExifTool.

Examle of usage:
perl .\modify_raw_location_metadata.pl --input "src_photos_test/IMG_5560.CR2" --output "dest_photos/IMG_5560.CR2" 
--lat_deg "43.0" --lat_min "8.0" --lat_sec "56.2" --lat_sign "1" --lon_deg "4.0" --lon_min "48.0" 
--lon_sec "59.3" --lon_sign "1"

=cut

use strict;
use Getopt::Long;
use Image::ExifTool;


my $input;
my $output;
my $lat_deg;
my $lat_min;
my $lat_sec;
my $lat_sign;
my $lon_deg;
my $lon_min;
my $lon_sec;
my $lon_sign;

GetOptions(
    "input=s"       => \$input,
    "output=s"      => \$output,
    "lat_deg=s"     => \$lat_deg,
    "lat_min=s"     => \$lat_min,
    "lat_sec=s"     => \$lat_sec,
    "lat_sign=s"    => \$lat_sign,
    "lon_deg=s"     => \$lon_deg,
    "lon_min=s"     => \$lon_min,
    "lon_sec=s"     => \$lon_sec,
    "lon_sign=s"    => \$lon_sign,
);

if (
    !defined($lat_deg) or
    !defined($lat_min) or
    !defined($lat_sec) or
    !defined($lat_sign) or
    !defined($lon_deg) or
    !defined($lon_min) or
    !defined($lon_sec) or
    !defined($lon_sec) or
    !defined($lon_sign) or
    !defined($input) or
    !defined($output)
    ){
    print("Missing parameters...\n");
    exit();
}

if ($input eq $output){
    print('The input can not be the same as the output to prevent overwriting files...');
    exit();
}


# START
my ($lat_str, $lat_dir, $lon_str, $lon_dir) = get_coordinates_string(
        $lat_deg, $lat_min, $lat_sec, $lat_sign, $lon_deg,
        $lon_min, $lon_sec, $lon_sign);

add_gps_data($input, $output, $lat_str, $lat_dir, $lon_str, $lon_dir);
# END


=item get_coordinates_string()

Format string to be written in the exif data

=cut

sub get_coordinates_string{

    my ($lat_deg, $lat_min, $lat_sec, $lat_sign, $lon_deg, $lon_min, $lon_sec, $lon_sign) = @_;

    my $lon_dir_short = $lon_sign == 1 ? 'E' : 'W';
    my $lon_dir_long = $lon_sign == 1 ? 'East' : 'West';
    my $lat_dir_short = $lat_sign == 1 ? 'N' : 'S';
    my $lat_dir_long = $lat_sign == 1 ? 'North' : 'South';

    my $latitude = "$lat_deg deg $lat_min' $lat_sec\"$lat_dir_short";
    my $longitude = "$lon_deg deg $lon_min' $lon_sec\"$lon_dir_short";


    print("$longitude --- $lon_dir_long\n");
    print("$latitude --- $lat_dir_long\n");

    return ($latitude, $lat_dir_long, $longitude, $lon_dir_long);
}

=item add_gps_data()

Insert the latitude and longitude valures in the exif data of an image

=cut

sub add_gps_data {
    
    my ($input, $output, $lat_str, $lat_dir, $lon_str, $lon_dir) = @_;

    my $exifTool = new Image::ExifTool;
    my $info = $exifTool->ImageInfo($input);

    my $tag_longitude = 'GPSLongitude';

    my $tag_latitude = 'GPSLatitude';

    my $longitude_ref_tag = 'GPSLongitudeRef';

    my $latitude_ref_tag = 'GPSLatitudeRef';


    $exifTool->SetNewValue($tag_longitude, $lon_str);
    $exifTool->SetNewValue($tag_latitude, $lat_str);

    $exifTool->SetNewValue($latitude_ref_tag, $lat_dir);
    $exifTool->SetNewValue($longitude_ref_tag, $lon_dir);

    print("Saving file to $output\n");
    my $result = $exifTool->WriteInfo($input, $output);
    if ($result != 1){
        print( $exifTool->GetValue('Warning') ."\n" );
        print( $exifTool->GetValue('Error') ."\n" );
    }
}