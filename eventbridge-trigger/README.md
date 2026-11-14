# EventBridge Upload Trigger

## Purpose
Starts the state machine automatically whenever an image is uploaded to the
original bucket, so a thumbnail appears without calling the API.

## Files
- `rule.json` - the event pattern and input transformer (reference copy)

## How it works
1. S3 sends an "Object Created" event to EventBridge for `original-images-tyson`.
2. The rule `image-upload-rule` matches it.
3. An input transformer reshapes the event into `{"bucket": ..., "key": ...}`.
4. The rule starts the `image-resize-workflow` state machine.

Only the original bucket sends events, so writing thumbnails never re-triggers the workflow.

## Steps
1. S3 -> original bucket -> Properties -> Amazon EventBridge -> turn On.
2. EventBridge -> Create rule -> event pattern from `rule.json`.
3. Target: the `image-resize-workflow` state machine, with the input transformer
   from `rule.json` and a newly created execution role.

## Verify
Upload an image to the original bucket. A new execution appears in Step Functions
and a `thumb-` copy appears in the thumbnail bucket.

## Troubleshooting
- No execution - check EventBridge notifications are On for the bucket and the
  bucket name in the pattern matches exactly.
- Execution fails immediately - check the input transformer produces `bucket` and `key`.
- Everything must be in the same region (`us-east-1`).