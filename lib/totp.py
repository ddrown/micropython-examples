from hashlib import sha1
import struct

# https://en.wikipedia.org/wiki/Base32
def b32decode(encoded):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    alphabet_map = {char: i for i, char in enumerate(alphabet)}
    b32_string = encoded.upper().rstrip("=")
    decoded_bytes = bytearray()

    # Process the Base32 string 8 characters (40 bits) at a time.
    for i in range(0, len(b32_string), 8):
        chunk = b32_string[i:i+8]
        bits = 0
        for char in chunk:
            bits = (bits << 5) | alphabet_map[char]
        total_bits = len(chunk) * 5
        for byte_i in range(0, 8):
            byteshift = total_bits - (byte_i * 8 + 8)
            if byteshift < 0:
                break
            decoded_bytes.append((bits >> byteshift) & 0xFF)
    return bytes(decoded_bytes)

def hmac_sha1_key(key):
    if len(key) > 64:
        return sha1(key).digest()
    if len(key) < 64:
        return key + b'\0' * (64 - len(key))
    return key

# https://en.wikipedia.org/wiki/HMAC
def hmac_sha1(key, data):
    block_key = hmac_sha1_key(key)
    o_key_pad = bytes([b ^ 0x5c for b in block_key])
    i_key_pad = bytes([b ^ 0x36 for b in block_key])
    return sha1(o_key_pad + sha1(i_key_pad + data).digest()).digest()

def zdigits(binary, digits):
    output = str(binary)[-digits:]
    return "0" * (6 - len(output)) + output

def totp(key, time_now, time_step=30, digits=6):
    key = b32decode(key)
    counter = struct.pack('>Q', time_now // time_step)
    mac = hmac_sha1(key, counter)
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return zdigits(binary, digits)
