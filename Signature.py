class Signature:
        def __init__(self, r, s):
            self.r = r
            self.s = s

        def __repr__(self):
            return 'Signature({:x},{:x})'.format(self.r, self.s)

        def der(self):
            rbin = self.r.to_bytes(32, byteorder='big')
            # remove all null bytes at the beginning
            rbin = rbin.lstrip(b'\x00')
            # if rbin has a high bit, add a \x00
            if rbin[0] & 0x80:
                rbin = b'\x00' + rbin
            result = bytes([2, len(rbin)]) + rbin  # <1>
            sbin = self.s.to_bytes(32, byteorder='big')
            # remove all null bytes at the beginning
            sbin = sbin.lstrip(b'\x00')
            # if sbin has a high bit, add a \x00
            if sbin[0] & 0x80:
                sbin = b'\x00' + sbin
            result += bytes([2, len(sbin)]) + sbin
            return bytes([0x30, len(result)]) + result        