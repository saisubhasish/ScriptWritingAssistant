import json
import boto3
import botocore.config
from datetime import datetime


def analyze_script_suggestion_using_bedrock(script_content:str)->str:
    ANALYZE_SCRIPT_PROMPT = f"""<s>[INST] Human: You are an intelligent script reviewer responsible to analyze the structure and
                                content of the script: {script_content}. Then do provide a precize suggestion for improvements.
                                Assistant:[/INST]
                                """
    body={
        "prompt":ANALYZE_SCRIPT_PROMPT,
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
        suggestions = response_data['generation']
        return suggestions
    
    except Exception as e:
        print(f"Error in generating the suggestion: {e}")
        return ""

def save_suggestions_to_s3(s3_key, s3_bucket, generated_suggestion):
    s3=boto3.client('s3')

    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generated_suggestion)
        print('Code saved to s3')

    except Exception as e:
        print(f"Error in saving the suggestion: {e}")

def lambda_handler(event, context):
    # TODO implement
    event = json.loads(event['body'])
    scriptcontent = event['script_content']

    generated_suggestion = analyze_script_suggestion_using_bedrock(script_content=scriptcontent)

    if generated_suggestion:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket='awsbedrockscriptwritingassistant'
        save_suggestions_to_s3(s3_key, s3_bucket, generated_suggestion)

    else:
        print('No suggestion was generated')

    return {
        'statusCode': 200,
        'body': json.dumps(generated_suggestion)
    }