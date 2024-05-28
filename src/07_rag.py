#!/usr/bin/env python3

import boto3
import json

# Get context from Kendra

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

# Assemble prompt from Kendra result

prompt = context + question

# Call Bedrock to get answer based on context retrieved from Kendra    

client = boto3.client(service_name="bedrock-runtime")

response = client.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    body=json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                     "content": [{"type": "text", "text": prompt}],
                }
            ],
        }
    ),
)

print(json.loads(response.get("body").read()).get("content")[0]["text"])

# Take-away:
# - An LLM can answer a question if the context is given alongside the question in the prompt.
#       This is called Retrieval Augmented Generation (RAG).