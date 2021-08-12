from storages.backends.s3boto3 import S3StaticStorage


class StaticStorage(S3StaticStorage):
    bucket_name = 'nimcat-statics'
