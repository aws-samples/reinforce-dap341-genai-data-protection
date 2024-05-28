#!/usr/bin/env python3

import datetime
import boto3

cloudtrail = boto3.client('cloudtrail')

endtime = datetime.datetime.now()
starttime = endtime - datetime.timedelta(hours=168) # 1 week back

print(endtime)
print(starttime)

response = cloudtrail.lookup_events(
    StartTime = starttime,
    EndTime = endtime,
    MaxResults = 3,
    LookupAttributes=[
        {
            'AttributeKey': 'EventName',
            'AttributeValue': 'InvokeModel' #Bedrock
        }
    ]
)

for event in response['Events']:
    print('-------------------EVENT-------------------')
    print('Event Name: ' + event['EventName'])
    print('Event Source: ' + event['EventSource'])
    print('Event Id: ' + event['EventId'])
    print('Event Time: ' + str(event['EventTime']))

# Take-away:
# - Cloudtrail events show service usage and can be used to audit usage and configuration changes.