from identification import public, private

import boto3
import os
import sys

if len(sys.argv) != 3:
    print ('Run the script with target folder and S3 bucket type as arguments.')
    print ('E.G: python3 photo_s3_uploader.py "Folder name" "Bucket type"')
    sys.exit()

folder_pattern = sys.argv[1]
bucket_type = sys.argv[2].lower()

if bucket_type != 'personal' and bucket_type != 'photoshoots':
    print ('Second argument must be either "personal" or "photoshoots"')
    sys.exit()

if bucket_type == "photoshoots":
    bucket_name = "f6rnando-photoshoots"
else:
    bucket_name = "f6rnando-personal"

s3_client = boto3.client('s3',
                        aws_access_key_id = public,
                        aws_secret_access_key = private)

os.chdir("~/Pictures")

for folder in os.listdir():
    if folder_pattern in folder:
        folder_name = folder.replace(" ", "_").replace("'", "") + "/"
        os.chdir(folder)
        for file in os.listdir():
            if '.CR2' in file or '.tif' in file:
                file_key = folder_name + str(file)
                print ("Uploading " + file + " to folder " + folder_name + " in " + bucket_name + " S3 Bucket: " + file_key + "...")
                # s3_client.upload_file(file, bucket_name, file_key)
        os.chdir("..")

print ("Upload finished. You can go to the AWS Console to check your files.")
