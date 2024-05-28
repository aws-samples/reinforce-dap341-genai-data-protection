#!/usr/bin/env python3

import boto3
import json

bedrock = boto3.client('bedrock')

bedrock_guardrail_identifier = 'bloap7adyg5v' #UPDATE_TO_RUN_YOURSELF

response = bedrock.get_guardrail(guardrailIdentifier=bedrock_guardrail_identifier)

print('Guardrail name: ' + response['name'])
print('Guardrail sensitive info policy: ' + str(response['sensitiveInformationPolicy']['piiEntities']))
