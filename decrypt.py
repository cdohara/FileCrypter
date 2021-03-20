from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import binascii, os, scrypt, sys

def cmd_help():
    print("Please include the file name argument. Ex) python crypt.py test.txt")

def decrypt_AES_GCM(encryptedMsg, password):
    (kdfSalt, ciphertext, nonce, authTag) = encryptedMsg
    secretKey = scrypt.hash(password, kdfSalt, N=16384, r=8, p=1, buflen=32)
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

def convert_to_tuple(encrypted_string):
    encrypted = encrypted_string.split()
    for i in range(len(encrypted)):
        encrypted[i] = b64decode(str.encode(encrypted[i]))
    return encrypted


# main function
if (len(sys.argv)!=2):
    cmd_help()
else:
    filename = sys.argv[1]
    print("Filename: ", filename)
    print(filename[-10:])
    if (".encrypted"!=filename[-10:]):
        print("This file does not seem encrypted. Exiting...")
        quit()
    password = input("Decryption pasword: ")
    f = open(filename, "rb")
    content = f.read()
    encrypted = convert_to_tuple(b64decode(content).decode("utf-8"))
    print("encryptedMsg", {
        'aesIV': binascii.hexlify(encrypted[2]),
        'authTag': binascii.hexlify(encrypted[3])
    })
    decrypted = decrypt_AES_GCM(encrypted, password)
    r1 = decrypted.decode()
    r2 = r1.encode()
    r3 = b64decode(r2)

    f = open(filename, "wb")
    f.write(r3)
    f.close()
    os.rename(filename, filename[0:-10])
    
