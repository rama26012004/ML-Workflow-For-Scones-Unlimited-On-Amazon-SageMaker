

#-----------------------------serializeImageData Lambda Funtion Code--------------------------------------------

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the image from S3
    s3.download_file(bucket, key, '/tmp/image.png')

    # Read and encode the image data
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Return the data to Step Function
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }




#--------------------------------------------Predict Image Lambda function code-----------------------------------------------

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the image from S3
    s3.download_file(bucket, key, '/tmp/image.png')

    # Read and encode the image data
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Return the data to Step Function
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
#----------------------------------- filterConfidence Lambda function code--------------------------------------------
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the image from S3
    s3.download_file(bucket, key, '/tmp/image.png')

    # Read and encode the image data
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Return the data to Step Function
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
