import json
import boto3
import botocore.config
from datetime import datetime


def generate_finalize_script_using_bedrock(improved_script_content:str, suggestion:str)->str:
    FINALIZE_SCRIPT_PROMPT = f"""<s>[INST] Human: You are an intelligent script writer. Responsible to writer finalyze script by 
                                analyzing your previous suggestion and improved script written by human. Now analyze the 
                                structure and content of the improved script: {improved_script_content} and your previous 
                                suggestion {suggestion}. Then provide only finalize script without any unnecessary talk.
                                Assistant:[/INST]"""
    body={
        "prompt":FINALIZE_SCRIPT_PROMPT,
        "max_tokens":200,
        "temperature":0.5,
        "top_p":0.9,
        "top_k":50
    }   

    try:
        bedrock=boto3.client("bedrock-runtime", region_name="us-east-1",
                             config=botocore.config.Config(
                                read_timeout=300,
                                retries={'max_attempts': 3}))
        response = bedrock.invoke_model(body=json.dumps(body),modelId="mistral.mistral-small-2402-v1:0")

        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        print(response_data)
        finalize_script = response_data['outputs'][0]['text']
        return finalize_script
    
    except Exception as e:
        print(f"Error in generating the script: {e}")
        return ""

def save_finalized_script_to_s3(s3_key, s3_bucket, finalized_script):
    s3=boto3.client('s3')

    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=finalized_script)
        print('Code saved to s3')

    except Exception as e:
        print(f"Error in saving the script: {e}")

def lambda_handler(event, context):
    # TODO implement
    event = json.loads(event['body'])
    improvedscriptcontent = event['improved_script_content']
    suggestion = event['suggestion']

    generated_finalized_script = generate_finalize_script_using_bedrock(improved_script_content=improvedscriptcontent, suggestion=suggestion)

    if generated_finalized_script:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket='awsbedrockscriptwritingassistant'
        save_finalized_script_to_s3(s3_key, s3_bucket, generated_finalized_script)

    else:
        print('No script was generated')

    return {
        'statusCode': 200,
        'body': json.dumps(generated_finalized_script)
    }