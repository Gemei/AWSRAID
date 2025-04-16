from datetime import datetime
import os, shutil

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def create_bucket_dirs(bucket):
    try:
        os.mkdir(bucket)
    except:
        pass

def delete_bucket_dirs(bucket):
    try:
        shutil.rmtree(bucket)
    except:
        pass