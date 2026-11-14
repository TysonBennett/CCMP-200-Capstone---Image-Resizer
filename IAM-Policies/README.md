# IAM Roles and Policies

Permissions used by the pipeline, following least privilege. The project uses
four roles. The API Gateway role is created by hand from the policy files in
this folder. The other three are created automatically by the AWS console, and
the Lambda role gets an extra inline policy from this folder.

## Roles at a glance

| Role | Used by | Created | Permissions |
|---|---|---|---|
| `<LAMBDA_ROLE_NAME>` | `image-resizer` Lambda | Automatically with the function | CloudWatch Logs (default) + inline policy `image-resizer-s3-access` |
| `image-resize-workflow-role` | `image-resize-workflow` state machine | Automatically with the state machine | Invoke the Lambda, deliver logs to CloudWatch |
| `apigw-start-stepfunctions` | `image-resizer-api` | Manually | Start the state machine |
| `<EVENTBRIDGE_ROLE_NAME>` | `image-upload-rule` (EventBridge rule) | Automatically with the rule target | Start the state machine |

## Policy files
| File | Attached to | Purpose |
|---|---|---|
| `lambda-s3-access-policy.json` | Lambda execution role (inline policy `image-resizer-s3-access`) | Read originals, write thumbnails |
| `api-gateway-trust-policy.json` | `apigw-start-stepfunctions` (trust relationship) | Lets API Gateway assume the role |
| `api-gateway-start-execution-policy.json` | `apigw-start-stepfunctions` (inline policy `start-image-resize-execution`) | Allows starting the state machine |

## How to attach the Lambda policy
1. Lambda -> `image-resizer` -> Configuration -> Permissions -> click the role name.
2. Add permissions -> Create inline policy -> JSON tab.
3. Paste the contents of `lambda-s3-access-policy.json`.
4. Name it `image-resizer-s3-access` and create it.

## How to create the API Gateway role
1. IAM -> Roles -> Create role -> Custom trust policy.
2. Paste `api-gateway-trust-policy.json`, skip managed permissions, and name the role `apigw-start-stepfunctions`.
3. Open the role -> Add permissions -> Create inline policy -> JSON.
4. Paste `api-gateway-start-execution-policy.json` (replace `ACCOUNT_ID`), and name it `start-image-resize-execution`.

## Automatically created roles
- **Lambda role** (`image-resizer-role`): created with the function. It includes
  the basic execution permissions for writing CloudWatch logs. The S3 access
  policy above is added on top of it.
- **Step Functions role** (`image-resize-workflow-role`): created with the state
  machine ("Create new role"). It allows invoking the resize Lambda and delivering
  logs to CloudWatch (logging is set to ALL).
- **EventBridge role** (`Amazon_EventBridge_Invoke_Step_Functions`): created with the rule target
  ("Create a new role for this specific resource"). It allows
  `states:StartExecution` on the state machine.

## Notes
- Replace `ACCOUNT_ID` in the policy files with your own 12-digit account ID.
- If you use different bucket names, update both `Resource` ARNs in
  `lambda-s3-access-policy.json`.