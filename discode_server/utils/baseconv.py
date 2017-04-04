import string


class BaseConverter(object):
    decode_mapping = {}

    def __init__(self, digits):
        self.digits = digits
        self.length = len(digits)

    def from_decimal(self, i):
        if i < 0:
            i, neg = -i, 1
        else:
            neg = 0
        enc = ''
        while i >= self.length:
            i, mod = divmod(i, self.length)
            enc = self.digits[mod] + enc
        enc = self.digits[i] + enc
        if neg:
            enc = '-' + enc
        return enc

    def to_decimal(self, s):
        if self.decode_mapping:
            new = ''
            for digit in s:
                if digit in self.decode_mapping:
                    new += self.decode_mapping[digit]
                else:
                    new += digit
            s = new
        if str(s)[0] == '-':
            s, neg = str(s)[1:], 1
        else:
            neg = 0
        decoded = 0
        multi = 1
        while len(s) > 0:
            decoded += multi * self.digits.index(s[-1:])
            multi = multi * self.length
            s = s[:-1]
        if neg:
            decoded = -decoded
        return decoded


base62 = BaseConverter(string.digits + string.ascii_uppercase)
