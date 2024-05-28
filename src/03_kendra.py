#!/usr/bin/env python3

import boto3

kendra = boto3.client('kendra')

kendra_index_id = 'a514c74c-59df-4e8c-a281-a49a68b0b683' #UPDATE_TO_RUN_YOURSELF
data_source_id = '496efb3d-b095-47a6-9780-d0a85ddaff2a'  #UPDATE_TO_RUN_YOURSELF

response = kendra.describe_data_source(
    Id = data_source_id,
    IndexId = kendra_index_id
)

#print(response)
print('Data Source Name: ' + response['Name'])
print('Data Source S3 Bucket: ' + response['Configuration']['TemplateConfiguration']['Template']['connectionConfiguration']['repositoryEndpointMetadata']['BucketName'])
print('S3 Bucket Inclusion Prefixes: ' + str(response['Configuration']['TemplateConfiguration']['Template']['additionalProperties']['inclusionPrefixes']))
print('Access Control List: ' + str(response['Configuration']['TemplateConfiguration']['Template']['additionalProperties']['aclConfigurationFilePath']))

# Take-away: 
# - Amazon Kendra can index many data sources, including Amazon S3 buckets
