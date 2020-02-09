from io import BytesIO
import unittest
import time
from random import randint
from helper import (
    hash256,
    encode_varint,
    int_to_little_endian,
    little_endian_to_int,
    read_varint,
)
NETWORK_MAGIC = b'\xf9\xbe\xb4\xd9'
TESTNET_NETWORK_MAGIC = b'\x0b\x11\x09\x07'

class NetworkEnvelope:
    """Class docstrings go here."""
    def __init__(self, command, payload, testnet = False):
        self.command = command
        self.payload = payload
        self.magic = TESTNET_NETWORK_MAGIC if testnet else NETWORK_MAGIC

    def __repr__(self):
        return '{}:{}:{}'.format(self.magic, self.command.decode('ascii'), self.payload.hex())
    
    def serialize(self):
        '''Returns the byte serialization of the entire network message'''
        # add the network magic
        result = self.magic
        # command 12 bytes
        # fill with 0's
        result += self.command + b'\x00' * (12 - len(self.command))
        # payload length 4 bytes, little endian
        result += int_to_little_endian(len(self.payload), 4)
        # checksum 4 bytes, first four of hash256 of payload
        result += hash256(self.payload)[:4]
        # payload
        result += self.payload
        return result
    
    @classmethod
    def parse(cls, stream, testnet = False):
        magic = stream.read(4) # 
        #print('Magic: {}'.format(magic))
        if magic == b'': # if magic is empty
            raise IOError('Connection reset!') # network problem
        expected_magic = TESTNET_NETWORK_MAGIC if testnet else NETWORK_MAGIC
        if magic != expected_magic:
            raise SyntaxError('magic is not right {} vs {}'.format(magic.hex(), expected_magic.hex()))
        
        command = stream.read(12) # 12 bytes, human-readable
        command = command.strip(b'\x00')
        
        payload_length = little_endian_to_int(stream.read(4)) # 4 payload length, 4 bytes, little endian
        
        checksum = stream.read(4) # payload checksum, first 4 bytes of hash of the payload
        payload = stream.read(payload_length) # read payload
        calculated_checksum = hash256(payload)[:4]
        if calculated_checksum != checksum:
            raise IOError('checksum does not match')
        return cls(command, payload, testnet=testnet)


class VersionMessage:
    """Class docstrings go here."""
    command = b'version'
    def __init__(self, 
        version = 70015, 
        services = 0, 
        timestamp = None, 
        receiver_services = 0,
        receiver_ip = b'\x00\x00\x00\x00', 
        receiver_port = 8333,
        sender_services = 0,
        sender_ip=b'\x00\x00\x00\x00',
        sender_port = 8333,
        nonce = None,
        user_agent = b'/programmingbitcoin:0.1/',
        latest_block = 0,
        relay = False):
        self.version = version
        self.services = services
        if timestamp is None:
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.receiver_services = receiver_services
        self.sender_services = sender_services
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        if nonce is None:
            self.nonce = int_to_little_endian(randint(0, 2**64), 8)
        else:
            self.nonce = nonce
        self.user_agent = user_agent
        self.latest_block = latest_block
        self.relay = relay

    def serialize(self):
        '''Serialize this message to send over the network'''
        # version is 4 bytes little endian
        result = int_to_little_endian(self.version, 4)
        # services is 8 bytes little endian
        result += int_to_little_endian(self.services, 8)
        # timestamp is 8 bytes little endian
        result += int_to_little_endian(self.timestamp, 8)
        # receiver services is 8 bytes little endian
        result += int_to_little_endian(self.receiver_services, 8)
        # IPV4 is 10 00 bytes and 2 ff bytes then receiver ip
        result += b'\x00' * 10 + b'\xff\xff' + self.receiver_ip
        # receiver port is 2 bytes, big endian
        result += self.receiver_port.to_bytes(2, 'big')
        # sender services is 8 bytes little endian
        result += int_to_little_endian(self.sender_services, 8)
        # IPV4 is 10 00 bytes and 2 ff bytes then sender ip
        result += b'\x00' * 10 + b'\xff\xff' + self.sender_ip
        # sender port is 2 bytes, big endian
        result += self.sender_port.to_bytes(2, 'big')
        # nonce should be 8 bytes
        result += self.nonce
        # useragent is a variable string, so varint first
        result += encode_varint(len(self.user_agent))
        # latest block is 4 bytes little endian
        result += self.user_agent
        # relay is 00 if false, 01 if true
        result += int_to_little_endian(self.latest_block, 4)

        result += b'\x01' if self.relay else b'\x00'
        return result
        
import socket

class NetworkEnvelopeTest(unittest.TestCase):

    def _test_parse(self):

        version = VersionMessage()

        envelope = NetworkEnvelope(version.command, version.serialize())
        msg = envelope.serialize()#bytes.fromhex('f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001')
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        self.assertEqual(envelope.command, b'version')
        self.assertEqual(envelope.payload, msg[24:])

        msg = bytes.fromhex('f9beb4d976657261636b000000000000000000005df6e0e2')
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        self.assertEqual(envelope.command, b'verack')
        self.assertEqual(envelope.payload, b'')

        msg = bytes.fromhex('f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001')
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        self.assertEqual(envelope.command, b'version')
        self.assertEqual(envelope.payload, msg[24:])

    def test1(self):
        print('Testing network envelop')
        host = 'testnet.programmingbitcoin.com'
        port = 18333
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((host, port))
        stream = skt.makefile('rb', None)
        version = VersionMessage()
        envelope = NetworkEnvelope(version.command, version.serialize())
        #print(envelope.serialize() )
        #print(envelope)
        #print(envelope.serialize().decode("ascii") )
        skt.sendall(envelope.serialize())
        while(True): # emulate a assync transfer of messages
            new_message = NetworkEnvelope.parse(stream)
            print(new_message)

    def _test_serialize(self):
        msg = bytes.fromhex('f9beb4d976657261636b000000000000000000005df6e0e2')
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        self.assertEqual(envelope.serialize(), msg)
        msg = bytes.fromhex('f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001')
        stream = BytesIO(msg)
        envelope = NetworkEnvelope.parse(stream)
        self.assertEqual(envelope.serialize(), msg)            
        
if __name__ == '__main__':
    unittest.main()


