#!/usr/bin/env python3

import datetime
import boto3

cloudwatch = boto3.client('logs')

endtime = datetime.datetime.now()
starttime = endtime - datetime.timedelta(hours=24)

response = cloudwatch.get_log_events(
    logGroupName='bedrock',   #UPDATE_TO_RUN_YOURSELF
    logStreamName='aws/bedrock/modelinvocations',
    startTime=int(starttime.timestamp() * 1000),
    endTime=int(endtime.timestamp() * 1000),
    limit=3,
    unmask=True
)

for event in response['events']:
    print('-----------Message in Log-------------')
    print(event['message'])

# Take-aways:
# - Amazon Bedrock doesn’t store or log your data in its service logs.
# - By default, Amazon Bedrock CloudWatch model invocation logging is disabled.
# - If you enable Amazon Bedrock CloudWatch model invocation logging, restrict access to those logs accordingly
#   because they contain the prompts and responses, which may contain sensitive information.