#!/usr/bin/python3
import argparse
import boto3

# No need to modify here (unless stuff doesn't work)
BUCKET = ""
IMAGE = ""

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help = 'path to your image')
ap.add_argument('-b', '--bucket', required=True, help = 'your bucket name')
args = ap.parse_args()
if (args.image != None):
    IMAGE = args.image 
if (args.bucket != None):
    BUCKET = args.bucket 

# Create an s3 client 's3' 
s3 = boto3.resource('s3')

# Use s3 client to send this image to the s3 bucket
s3.meta.client.upload_file(IMAGE, BUCKET, IMAGE)
print("Image: " + IMAGE + " has been sent to bucket: " + BUCKET)