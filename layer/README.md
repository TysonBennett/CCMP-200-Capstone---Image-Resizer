# Pillow Lambda Layer

## Purpose
Packages the Pillow image library as a Lambda layer, since Lambda doesn't include it.

## Files
- `build-layer.sh` - builds Pillow for Lambda (Linux x86_64, Python 3.12) and publishes it as a layer

## Prerequisites
- AWS account with access to CloudShell
- Region set to `us-east-1`

## Steps
1. Open AWS CloudShell in `us-east-1`.
2. Actions → Upload file → select `build-layer.sh`.
3. Run:
   ```bash
   sed -i 's/\r$//' build-layer.sh
   chmod +x build-layer.sh
   ./build-layer.sh
   ```

## Verify
The script prints a layer ARN ending in `:1`, and `pillow-layer` appears under Lambda → Layers.

## Troubleshooting
- `$'\r': command not found` - run the `sed` line above to remove Windows line endings.
- `AccessDenied` on publish - your IAM user needs Lambda layer permissions.