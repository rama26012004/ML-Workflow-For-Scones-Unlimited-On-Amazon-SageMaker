

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

runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    image_dict = event['body'] 

    if isinstance(image_dict, str):
        image_dict = json.loads(image_dict)

    # Decode the base64 image
    image_bytes = base64.b64decode(image_dict['image_data'])

    # Invoke SageMaker endpoint
    response = runtime.invoke_endpoint(
        EndpointName='image-classification-2025-07-16-22-29-35-676',  # Change this!
        ContentType='application/x-image',
        Body=image_bytes
    )

    result = json.loads(response['Body'].read().decode())

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }



#----------------------------------- filterConfidence Lambda function code--------------------------------------------
import json

THRESHOLD = 0.93

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event

        # If body is a list (i.e., just the raw inferences), use it directly
        if isinstance(body, list):
            inferences = body
        else:
            inferences = body.get("inferences")

        if inferences is None:
            raise ValueError("Event body does not contain 'inferences'")

        meets_threshold = any(float(score) > THRESHOLD for score in inferences)

        if meets_threshold:
            return {
                'statusCode': 200,
                'body': json.dumps({'inferences': inferences})
            }
        else:
            raise ValueError("THRESHOLD_CONFIDENCE_NOT_MET")

    except Exception as e:
        raise e
