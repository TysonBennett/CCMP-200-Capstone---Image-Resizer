# Image Resizer Lambda

## Purpose
Downloads an image from the source bucket, shrinks it to a 128x128 thumbnail
(keeping aspect ratio), and uploads it to the thumbnail bucket.

## Files
- `lambda_function.py` - the handler
- `requirements.txt` - dependency list (Pillow is provided by the Lambda layer)

## Input and output
Input:
    {"bucket": "original-images-tyson", "key": "photo.jpg"}

Output on success:
    {"status": "resized", "thumbnail": "thumb-photo.jpg"}

Output on failure:
    {"status": "failed", "error": "<message>"}

## Configuration
| Setting | Value |
|---|---|
| Runtime / architecture | Python 3.12 / x86_64 |
| Memory / timeout | 512 MB / 30 s |
| Layer | `pillow-layer` (see `../pillow-layer`) |
| Environment variable | `DESTINATION_BUCKET=thumbnail-images-tyson` |

## Steps
1. Create the function `image-resizer` with the settings above.
2. Attach the `pillow-layer` layer.
3. Paste `lambda_function.py` and click Deploy.
4. Add an inline policy to the execution role allowing `s3:GetObject` on
   `original-images-tyson/*` and `s3:PutObject` on `thumbnail-images-tyson/*`. (see `../IAM Policies/lambda-s3-access-policy`)

## Verify
Run a test event with the input above. The result should show `"status": "resized"`
and `thumb-photo.jpg` should appear in the thumbnail bucket.

## Troubleshooting
- `No module named PIL` - the layer isn't attached, or the function isn't x86_64.
- `"status": "failed"` with AccessDenied - check the S3 inline policy and bucket names.
- `KeyError: 'DEST_BUCKET'` - the environment variable isn't set.