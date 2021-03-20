# FileCrypter

A simple way of password protecting your files using AES-GCM.

## Process

Currently, the code works like this:

1. Read file as binary bytes
2. Convert content into base64 bytes, decode to utf8, encode to bytes
3. Create encryption with four different parts: salt, key, text, and auth tag
4. Convert tuple into utf8, and then add space between each part
5. Encode into bytes and then encode into baes64
6. Overwrite the file and append .encrypted at the end.

You might be able to use the base64 bytes directly, but I'm not sure. I haven't tried it yet. For some reason, it feels like too much work at 3:56 am.

## Usage

Easy to use! Just have the file you want to encrypt in the same directory.

**Uses Python3.**

```
python crypt.py filetoencrypt.jpg
```

`filetoencrypt.jpg.encrypted` will replace `filetoencrypt.jpg`.
