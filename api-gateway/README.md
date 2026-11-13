# API Gateway

## Purpose
Exposes a REST endpoint that starts the Step Functions state machine.

## Files
- `mapping-template.vtl` - wraps the request body into the StartExecution call

## Endpoint
    POST https://<api-id>.execute-api.us-east-1.amazonaws.com/dev/resize
    Content-Type: application/json
    {"bucket": "original-images-tyson", "key": "photo.jpg"}

The response contains an `executionArn`. The workflow runs asynchronously, so
check Step Functions for the result.

## Steps
1. Create the IAM role (see `../iam/README.md`).
2. Create a REST API with a `/resize` resource and a POST method.
3. Integration: AWS service, Step Functions, action `StartExecution`, region
   `us-east-1`, execution role = the role ARN.
4. Add the mapping template, and set request body passthrough to Never.
5. Deploy to a stage named `dev`.

## Verify
Use the Test tab, or send a POST request to the invoke URL. The response should
contain `executionArn`, and a new execution should appear in Step Functions.

## Troubleshooting
- `UnknownOperationException` - the action name isn't `StartExecution`.
- Request goes to the wrong region - the integration region must match the state machine.
- Permission error - check the trust policy and inline policy on the role.
- Invalid ARN when creating the method - the Execution role field needs the IAM
  role ARN, not the role name or the state machine ARN.