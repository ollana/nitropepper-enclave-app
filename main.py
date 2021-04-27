"""Enclave NitroPepper application."""

import json
import socket

from kms import NitroKms

ENCLAVE_PORT = 5000

def main():
    """Run the nitro enclave application."""
    # Bind and listen on vsock.
    vsock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM) # pylint:disable=no-member
    vsock.bind((socket.VMADDR_CID_ANY, ENCLAVE_PORT)) # pylint:disable=no-member
    vsock.listen()

    # Initialize a KMS class
    nitro_kms = NitroKms()
    print('Listening...')

    while True:
        conn, _addr = vsock.accept()
        print('Received new connection')
        payload = conn.recv(4096)
        print(str(payload))

        # Load the data provided over vsock
        try:
            parent_app_data = json.loads(payload.decode())
            kms_credentials = parent_app_data['kms_credentials']
            cipher_text = parent_app_data['cipher']
            print("payload decoded: ", str(cipher_text))
            kms_region = "us-west-2"
        except Exception as exc: # pylint:disable=broad-except
            msg = f'Exception ({type(exc)}) while loading data: {str(exc)}'
            content = {
                'success': False,
                'error': msg
            }
            conn.sendall(str.encode(json.dumps(content)))
            conn.close()
            continue

        nitro_kms.set_region(kms_region)
        nitro_kms.set_credentials(kms_credentials)
        plain_text = process_decrypt(nitro_kms, cipher_text)
        print("decrypted: "+str(plain_text))

        conn.sendall(str.encode(str(plain_text)))

        conn.close()
        print('Closed connection')


def process_decrypt(nitro_kms, cipher_text):
    """Decrypt given cipher."""
    try:
        print("process_decrypt: ", str(cipher_text))
        plain_text = nitro_kms.kms_decrypt(
            ciphertext_blob=cipher_text
        )
    except Exception as exc: # pylint:disable=broad-except
        print(str(exc))
        return 'decrypt failed' + str(exc)

    return plain_text



if __name__ == '__main__':
    main()
