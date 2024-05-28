#!/usr/bin/env python3

import boto3

kendra = boto3.client('kendra')

kendra_index_id = 'a514c74c-59df-4e8c-a281-a49a68b0b683' #UPDATE_TO_RUN_YOURSELF

question = "What is the Root Runner 3000 and what is its power consumption?"

result = kendra.retrieve(
    IndexId = kendra_index_id, 
    QueryText = question,
    PageSize = 2)

context = ''
for result_item in result["ResultItems"]:
    context += "------CONTEXT-----"
    context += result_item["Content"]

print(context)

# Take-away: 
# - Amazon Kendra can search your data to find relevant context
