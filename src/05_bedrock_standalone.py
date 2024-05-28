#!/usr/bin/env python3

import boto3
import json

client = boto3.client(service_name="bedrock-runtime")

question = "What is AWS re:Inforce?"

prompt = question

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

# Take-aways:
# - Amazon Bedrock Large Language Models (LLMs) generate natural language.
# - An LLM can answer questions about data it has been trained against.