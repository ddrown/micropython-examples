# starting point: https://github.com/susam/mintotp, converted to micropython
from lib.totp import totp

key = "ZYTYYE5FOAGW5ML7LRWUL4WTZLNJAMZS"

#for j in ['GE======', 'GEZA====', 'GEZDG===', 'GEZDGNA=', 'GEZDGNBV', 'GEZDGNBVGY======', 'GEZDGNBVGY3Q====', 'GEZDGNBVGY3TQ===']:
#    print(b32decode(j))
# expected: b"\xce'\x8c\x13\xa5p\rn\xb1\x7f\\mE\xf2\xd3\xca\xda\x9032"
#print(b32decode(key))
# expected: b"base32 encoding"
#print(b32decode("MJQXGZJTGIQGK3TDN5SGS3TH"))
# expected: b"\x13\r\x91Of\x81o';$\x03h<xHR\xe9\xfel\x91"
# print(hmac_sha1(b"\xce'\x8c\x13\xa5p\rn\xb1\x7f\\mE\xf2\xd3\xca\xda\x9032", b'\x00\x00\x00\x00\x00\x00\x00*'))
# expected: b'\xde|\x9b\x85\xb8\xb7\x8a\xa6\xbc\x8az6\xf7\n\x90p\x1c\x9d\xb4\xd9'
# print(hmac_sha1(b"key", b"The quick brown fox jumps over the lazy dog"))

# expected: 626854
print(totp(key, 1260))

for i in range(0, 10):
    print(totp(key, i*30, 30, 6))