#!/usr/bin/env python3

import boto3

s3 = boto3.client('s3')

# create code to list objects in an s3 bucket and print the name of each object

response = s3.list_objects_v2(Bucket='ecorobopotato') #UPDATE_TO_RUN_YOURSELF
for obj in response['Contents']:
    print(obj['Key'])   

# create code to get the encryption of an s3 bucket and print the encryption type
response = s3.get_bucket_encryption(Bucket='ecorobopotato')
print('Server-side ecryption type: ' + response['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'])

# Take-aways: 
# - We have proprietary data in an S3 bucket
# - Data should be encrypted @ rest