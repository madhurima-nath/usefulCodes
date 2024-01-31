# simple script to call bedrock models through boto3 client

import boto3
from langchain_community.llms.bedrock import Bedrock

bedrock_client = boto3.client('bedrock-runtime', region='us-east-1',endpoint_url=f'https://bedrock-runtime.us-east-1.amazonaws.com')

bedrock = Bedrock(client = bedrock_client, model_id = 'anthropic.claude-v2:1')

print(bedrock.invoke('what is 2+2?'))

# this will print '4' as an answer
