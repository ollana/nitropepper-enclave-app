#!/bin/sh
echo "Starting init"
#vsock-proxy 8000 kms.us-west-2.amazonaws.com 443 &
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r .[0].EnclaveID)

if [ -z $ENCLAVE_ID ]
then
  echo "Starting deleting existing enclave image"
  sudo nitro-cli terminate-enclave --enclave-id $ENCLAVE_ID || echo "failed to delete enclave $ENCLAVE_ID"
fi

echo "Starting building docker image"
docker build . -t nitropepper

echo "Starting building enclave image"
nitro-cli build-enclave --docker-uri nitropepper:latest --output-file nitropepper.eif

echo "Starting running enclave"
sudo nitro-cli run-enclave --cpu-count 2 --memory 3072 --eif-path nitropepper.eif --enclave-cid 6 --debug-mode

echo "Starting describe enclave"
nitro-cli describe-enclaves
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r .[0].EnclaveID)

echo "Starting console enclave $ENCLAVE_ID"
nitro-cli console --enclave-id $ENCLAVE_ID
