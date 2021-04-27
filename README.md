based on: 
https://www.sentiatechblog.com/ultra-secure-password-storage-with-nitropepper

server side (running in enclave):
```
git clone https://github.com/ollana/nitropepper-enclave-app.git nitropepper
cd nitropepper
./init_image.sh
```
client side (running on parent instance):
start proxy:
```
vsock-proxy 8000 kms.us-west-2.amazonaws.com 443 &
```
```
git clone https://github.com/ollana/aws-nitro-enclaves-samples
aws-nitro-enclaves-samples/vsock_sample/py/
python3 vsock-sample.py client 6 5000 AQICAHjvbtWpNjYZ8764oSDieh0nlBAeD9vck/+jH5QTI/hgPQEccAul00TiXmNhVzC4Hb47AAAAajBoBgkqhkiG9w0BBwagWzBZAgEAMFQGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQM3Jdxeb1gmbTpuBEqAgEQgCfptMV54Y5t0np/PzIChJhkcWglFeq5rJv0O8QcX1Gp8bnBmusBwPo=
```
