from FieldElement import FieldElement
from Point import Point
from PrivateKey import PrivateKey
'''
a = FieldElement(0, 223)
b = FieldElement(7, 223)
x = FieldElement(15, 223)
y = FieldElement(86, 223)

p = Point(x, y, a, b)
print(7 * p)
'''

## Broadcast transaction ##

# create 1 TxIn and 2 TxOuts
# 1 of the TxOuts should be back to your address
# the other TxOut should be to this address
target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'

from helper import decode_base58, SIGHASH_ALL, little_endian_to_int, hash256
from Script import Script, p2pkh_script
from PrivateKey import PrivateKey
from Tx import Tx, TxIn, TxOut

#secret = little_endian_to_int(hash256(b'Destino secret'))
#private_key = PrivateKey(secret)
#print (private_key.point.address(testnet = True))
# mvHGDGX1N2XsAcCimeP1zdxVSXYSy41M95

#secret = little_endian_to_int(hash256(b'Alexandre secret'))
#private_key = PrivateKey(secret)
#print (private_key.point.address(testnet = True))
# mnnkSB94QTYaGFYVGgeLgN64jVLtLQfqYL

prev_tx = bytes.fromhex('75a1c4bc671f55f626dda1074c7725991e6f68b8fcefcfca7b64405ca3b45f1c')
prev_index = 1
target_address = 'mvHGDGX1N2XsAcCimeP1zdxVSXYSy41M95'#'miKegze5FQNCnGw6PKyqUbYUeBa4x2hFeM'
target_amount = 0.001
change_address = 'mnnkSB94QTYaGFYVGgeLgN64jVLtLQfqYL'#'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'
change_amount = 0.0009
secret = 8675309
priv = PrivateKey(secret=secret)
tx_ins = []
tx_ins.append(TxIn(prev_tx, prev_index))
tx_outs = []
h160 = decode_base58(target_address)
script_pubkey = p2pkh_script(h160)
target_satoshis = int(target_amount*100000000)
tx_outs.append(TxOut(target_satoshis, script_pubkey))
h160 = decode_base58(change_address)
script_pubkey = p2pkh_script(h160)
change_satoshis = int(change_amount*100000000)
tx_outs.append(TxOut(change_satoshis, script_pubkey))
tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
print(tx_obj.sign_input(0, priv))
print(tx_obj.serialize().hex())
