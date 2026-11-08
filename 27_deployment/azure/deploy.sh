#!/usr/bin/env bash
# One-time setup: deploy the hello-service container to Azure Container Apps.
# Needs the Azure CLI (az login first). Read every line before you run it:
# these commands create billable Azure resources.
set -euo pipefail

RG=rg-python-pro            # resource group: a folder for related Azure resources
LOCATION=germanywestcentral
ACR=pythonpro$RANDOM        # container registry names must be globally unique
ENVIRONMENT=python-pro-env
APP=hello-service

# 1. A resource group and a private container registry
az group create --name "$RG" --location "$LOCATION"
az acr create --resource-group "$RG" --name "$ACR" --sku Basic

# 2. Build the image IN Azure (no local Docker needed) and store it in the registry
az acr build --registry "$ACR" --image "$APP:1.0.0" --build-arg APP_VERSION=1.0.0 ..

# 3. A Container Apps environment (shared networking + logging for your apps)
az containerapp env create --name "$ENVIRONMENT" --resource-group "$RG" --location "$LOCATION"

# 4. The app itself: HTTPS ingress, scale 0-3 replicas, config via env vars,
#    the database password as a SECRET (not a plain env var)
az containerapp create \
  --name "$APP" --resource-group "$RG" --environment "$ENVIRONMENT" \
  --image "$ACR.azurecr.io/$APP:1.0.0" --registry-server "$ACR.azurecr.io" \
  --target-port 8000 --ingress external \
  --min-replicas 0 --max-replicas 3 \
  --secrets db-url="postgresql+psycopg://user:CHANGE_ME@host:5432/shop" \
  --env-vars APP_ENV=prod APP_VERSION=1.0.0 APP_DATABASE_URL=secretref:db-url

# 5. The public URL
az containerapp show --name "$APP" --resource-group "$RG" \
  --query properties.configuration.ingress.fqdn --output tsv

# Clean up everything when you're done experimenting:
#   az group delete --name "$RG" --yes --no-wait
