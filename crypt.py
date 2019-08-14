import os
import base64
import random
import struct
import hashlib
import sys
import getpass
from Crypto.Cipher import AES
from Crypto import Random


if sys.argv[1] == 'encrypt':
    original_file = sys.argv[2]
    encrypted = sys.argv[3]
    file_size = str(os.path.getsize(original_file)).zfill(16)
elif sys.argv[1] == 'decrypt':
    encrypted = sys.argv[2]
    decrypted = sys.argv[3]
else:
    print('opção invalida')

sk = getpass.getpass('chave secreta: ')
skenc = base64.b64encode(sk.encode())
block_size = 64 * 1024

opt = sys.argv[1]
if opt == 'encrypt':
    iv = os.urandom(16)
    AES_cipher = AES.new(skenc, AES.MODE_CBC, iv)
    with open(original_file, 'rb') as infile:
        with open(encrypted, 'wb') as outfile:

            outfile.write(file_size.encode())
            outfile.write(iv)

            while True:
                chunk = infile.read(block_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(AES_cipher.encrypt(chunk))
elif opt == 'decrypt':
    with open(encrypted, 'rb') as infile:
        original_size = int(infile.read(16))
        iv = infile.read(16)
        AES_cipher = AES.new(skenc, AES.MODE_CBC, iv)

        with open(decrypted, 'wb') as outfile:
            while True:
                chunk = infile.read(block_size)
                if len(chunk) == 0:
                    break
                outfile.write(AES_cipher.decrypt(chunk))

            outfile.truncate(original_size)
else:
    print("opção inválida")