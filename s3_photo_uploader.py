from secrets import public, private

import boto3
import os
import sys

def get_valid_arguments() :
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print ('ERROR - Wrong arguments quantity.')
        print ('Run the script with target folder and S3 bucket type as arguments.')
        print ('E.G: python3 photo_s3_uploader.py "Folder name" "Bucket type"')
        sys.exit()
    return sys.argv[1], sys.argv[2].lower();

def get_bucket_name(bucket_type) :
    if bucket_type != 'personal' and bucket_type != 'photoshoots':
        print ('Second argument must be either "personal" or "photoshoots"')
        sys.exit()
    return "f6rnando-photoshoots" if bucket_type == "photoshoots" else "f6rnando-personal"

def get_s3_client() :
    return boto3.client('s3',
                        aws_access_key_id = public,
                        aws_secret_access_key = private)
def is_video_upload() :
    return len(sys.argv) == 4 and sys.argv[3] == "video"

def go_to_location() :
    if is_video_upload():
        os.chdir(os.path.expanduser("~") + "/Movies")
    else :
        os.chdir(os.path.expanduser("~") + "/Pictures")

def get_s3_file_key(folder_name, file) :
    file_key = folder_name + str(file)
    return "Videos/" + file_key if is_video_upload() else file_key

def upload_files_to_s3(folder_pattern, s3_client, bucket_name) :
    for folder in os.listdir():
        if folder_pattern in folder:
            folder_name = folder.replace(" ", "_").replace("'", "") + "/"
            os.chdir(folder)
            for file in os.listdir():
                if '.CR2' in file or '.tif' in file or '.MP4':
                    file_key = get_s3_file_key(folder_name, file)
                    print ("Uploading " + file + " to folder " + folder_name + " in " + bucket_name + " - S3 Bucket: " + file_key + "...")
                    s3_client.upload_file(file, bucket_name, file_key)
            os.chdir("..")

def main() :
    folder_pattern, bucket_type = get_valid_arguments()
    bucket_name = get_bucket_name(bucket_type)
    s3_client = get_s3_client()
    go_to_location()
    upload_files_to_s3(folder_pattern, s3_client, bucket_name)
    print ("Upload finished. You can go to the AWS Console to check your files.")

main()
