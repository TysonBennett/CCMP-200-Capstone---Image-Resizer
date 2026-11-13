#!/usr/bin/env bash
set -euo pipefail

REGION="us-east-1"
LAYER_NAME="pillow-layer"
PY_VERSION="3.12"

echo "Cleaning old build..."
rm -rf layer-build
mkdir -p layer-build/python
cd layer-build

echo "Installing Pillow for Lambda (Linux x86_64, Python ${PY_VERSION})..."
pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version "${PY_VERSION}" \
  --only-binary=:all: \
  --target python \
  pillow

echo "Zipping..."
zip -r -q pillow-layer.zip python

echo "Publishing layer to ${REGION}..."
aws lambda publish-layer-version \
  --region "${REGION}" \
  --layer-name "${LAYER_NAME}" \
  --zip-file fileb://pillow-layer.zip \
  --compatible-runtimes "python${PY_VERSION}" \
  --compatible-architectures x86_64 \
  --query "LayerVersionArn" \
  --output text

echo "Done."