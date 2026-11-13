import logging              # Used for logging successes and failures
import os                   # Used for interacting with environment variables
import boto3                # Used to interact with AWS services
from PIL import Image       # Used for managing images with Python pillow library

# Configure logging to show info level messages and above
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create S3 client
s3 = boto3.client('s3')

# Configure thumbnail size
THUMBNAIL_SIZE = (128, 128)

def lambda_handler(event, context):
    # Grab bucket and key from the event
    bucket, key = event['bucket'], event['key']

    # Create local paths for source and destination files
    name = os.path.basename(key)
    src = f"/tmp/{name}"
    dst = f"/tmp/thumb-{name}"

    # Download file, create thumbnail, and upload thumbnail
    try:
        s3.download_file(bucket, key, src)

        with Image.open(src) as img:
            img.thumbnail(THUMBNAIL_SIZE)
            img.save(dst)

        s3.upload_file(dst, os.environ["DESTINATION_BUCKET"], f"thumbnails/{name}")

        # Log success
        logger.info(f"Successfully resized {key}")
        return {"status": "resized", "thumbnail": f"thumb-{name}"}

    #  If anything goes wrong, log the error and return a failure message
    except Exception as e:
        logger.error(e)
        return {"status": "failed", "error": str(e)}
