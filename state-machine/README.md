# Step Functions State Machine

## Purpose
Orchestrates the image processing workflow: invoke the resize Lambda, check
the result, then succeed or fail.

## Files
- `image-resize.asl.json` - the state machine definition (JSONata query language)

## Workflow
1. **ResizeImage** (Task) - invokes the `image-resizer` Lambda with the bucket and key.
2. **CheckResizeResult** (Choice) - routes on the Lambda's `status` field.
3. **ResizeSucceeded** (Succeed) - status was `resized`.
4. **ResizeFailed** (Fail) - status was anything else, or the Lambda raised an error.

## Input
    {"bucket": "original-images-tyson", "key": "photo.jpg"}

## Steps
1. Step Functions -> Create state machine -> Code view.
2. Paste `image-resize.asl.json`, replacing `ACCOUNT_ID` with your account ID.
3. Name it `image-resize-workflow`, type Standard.
4. Create a new execution role, and set logging to ALL.

## Verify
- Start an execution with the input above: it ends in Succeeded and the thumbnail is in the thumbnail bucket.
- Use a key that doesn't exist: it ends in Failed with error `ResizeError`.

## Troubleshooting
- Lambda permission error - the execution role needs `lambda:InvokeFunction` on the function.
- JSONata errors - check `"QueryLanguage": "JSONata"` is at the top and `Arguments`/`Output` are used.