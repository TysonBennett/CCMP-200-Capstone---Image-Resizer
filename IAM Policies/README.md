# IAM Policies

Permissions used by the pipeline, following least privilege.

## Files
| File | Attached to | Purpose |
|---|---|---|
| `lambda-s3-access-policy.json` | Lambda execution role of `image-resizer` | Read originals, write thumbnails |

More policies are added here as components are built (Step Functions and API Gateway roles).

## How to attach the Lambda policy
1. Lambda -> `image-resizer` -> Configuration -> Permissions -> click the role name.
2. Add permissions -> Create inline policy -> JSON tab.
3. Paste the contents of `lambda-s3-access-policy.json`.
4. Name it `image-resizer-s3-access` and create it.

## Notes
- The role was created automatically by Lambda and already includes the basic
  execution permissions for writing CloudWatch logs.
- If you use different bucket names, update both `Resource` ARNs.