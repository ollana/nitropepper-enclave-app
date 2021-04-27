#!/bin/sh
echo "Starting building enclave image"
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r .[0].EnclaveID)

if [ -z "$ENCLAVE_ID" ]
then
  sudo nitro-cli terminate-enclave --enclave-id $ENCLAVE_ID || echo "failed to delete enclave $ENCLAVE_ID"
fi

docker build . -t nitropepper
nitro-cli build-enclave --docker-uri nitropepper:latest --output-file nitropepper.eif

sudo nitro-cli run-enclave --cpu-count 2 --memory 3072 --eif-path nitropepper.eif --enclave-cid 6 --debug-mode
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r .[0].EnclaveID)
nitro-cli console --enclave-id $ENCLAVE_ID
