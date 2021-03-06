import hashlib

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def decode_base58(s):
    num = 0
    for c in s:  # <1>
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')  # <2>
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, 
          hash256(combined[:-4])[:4]))
    return combined[1:-4]  # <3>

def encode_base58(s):
    # determine how many 0 bytes (b'\x00') s starts with
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    # convert to big endian integer
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result        

def encode_base58_checksum(s):
    return encode_base58(s + hash256(s)[:4])

def hash256(s):
    # two rounds of sha256
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


# sha256 followed by ripemd160
def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()    

def int_to_little_endian(n, length):
    # endian_to_little_endian takes an integer and returns the little-endian byte sequence of length
    return n.to_bytes(length, 'little')

def little_endian_to_int(b):
    # little_endian_to_int takes byte sequence as a little-endian number. 
    # Returns an integer
    return int.from_bytes(b, 'little')  

def read_varint(s):
    # read_varint reads a variable integer from a stream
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else is just the integer
        return i      

def encode_varint(i):
    '''encodes an integer as a varint'''
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError('integer too large: {}'.format(i))