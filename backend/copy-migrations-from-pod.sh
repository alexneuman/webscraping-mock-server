#!/bin/bash

# CONFIGURATION
NAMESPACE="backend"
POD_NAME=$(kubectl get pod -n $NAMESPACE -l app=backend -o jsonpath='{.items[0].metadata.name}')
REMOTE_MIGRATIONS_DIR="/app/alembic/versions"
LOCAL_MIGRATIONS_DIR="./alembic/versions"

echo "Copying Alembic migration files from pod $POD_NAME..."

# Create local versions directory if needed
mkdir -p "$LOCAL_MIGRATIONS_DIR"

# Copy the entire versions folder from the pod
kubectl cp "$NAMESPACE/$POD_NAME:$REMOTE_MIGRATIONS_DIR" "$LOCAL_MIGRATIONS_DIR"

echo "Done. Migration files copied to $LOCAL_MIGRATIONS_DIR"
