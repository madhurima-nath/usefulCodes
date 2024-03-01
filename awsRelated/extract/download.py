import boto3

def get_aws_client(profile_name: str) -> boto3.Session:
    session = boto3.Session(profile_name=profile_name)
    return session

def download_file(
        session: boto3.Session, bucket: str, object_name: str, output_path: str
) -> None:
    with open(output_path, "wb") as binary_file:
        s3_client = session.client("s3")
        s3_client.download_fileobj(bucket, object_name, binary_file)

def upload_file(
        session: boto3.Session, bucket:str, object_name: str, output_path: str
) -> None:
    s3_client = session.client("s3")
    s3_client.upload_file(output_path, bucket, object_name)