from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import binascii, os, scrypt, sys

def cmd_help():
    print("Please include the file name argument. Ex) python crypt.py test.txt")

def encrypt_AES_GCM(msg, password):
    kdfSalt = os.urandom(16)
    secretKey = scrypt.hash(password, kdfSalt, N=16384, r=8, p=1, buflen=32)
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (kdfSalt, ciphertext, aesCipher.nonce, authTag)

def convert_to_text(encrypted):
    a = str(len(encrypted[0]))
    aa = b64encode(encrypted[0]).decode()
    b = str(len(encrypted[1]))
    bb = b64encode(encrypted[1]).decode()
    c = str(len(encrypted[2]))
    cc = b64encode(encrypted[2]).decode()
    d = str(len(encrypted[3]))
    dd = b64encode(encrypted[3]).decode()
    return aa + " " + bb + " " + cc + " " + dd

# main function
if (len(sys.argv)!=2):
    cmd_help()
else:
    filename = sys.argv[1]
    print("Filename: ", filename)
    password = input("Encryption pasword: ")
    f = open(filename, "rb")
    content = f.read()
    f.close()
    # print(content)
    if (content == ""):
        print("Nothing to encrypt. Exiting.")
        quit()
    encrypted = encrypt_AES_GCM(str.encode(b64encode(content).decode()), str.encode(password))
    print("encryptedMsg", {
        'aesIV': binascii.hexlify(encrypted[2]),
        'authTag': binascii.hexlify(encrypted[3])
    })
    result = convert_to_text(encrypted)
    result = b64encode(str.encode(result))
    # print("\nresult: ", result)
    # print("\n\ndecrypting...\n==================")
    
    # r1 = str.encode(result)
    # print(r1)
    # r2 = b64decode(r1)
    # print(r2)

    f = open(filename, "wb")
    f.write(result)
    f.close()
    os.rename(filename, filename + ".encrypted")
    

