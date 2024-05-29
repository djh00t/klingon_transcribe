import boto3

s3_client = boto3.client('s3')

def parse_s3_url(s3_url):
    """Parse S3 URL to bucket and key."""
    assert s3_url.startswith("s3://")
    bucket, key = s3_url[5:].split("/", 1)
    return bucket, key

def read(s3_url):
    """Read audio file from S3 URL."""
    bucket, key = parse_s3_url(s3_url)
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()

def write(s3_url, data):
    """Write data to S3 URL."""
    bucket, key = parse_s3_url(s3_url)
    s3_client.put_object(Bucket=bucket, Key=key, Body=data)
