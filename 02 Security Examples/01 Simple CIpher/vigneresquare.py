class vignere_cipher:
    """ vignere_cipher

    Handles encryption of upper, lower, numeric, and symbols within their own ranges (e.g. upper->upper)
    """
    def __init__(self):
        self.key = ""
        self.key_length = 0
        self.offsets = list()

    def set_key(self, key) -> bool:
        self.key = key
        self.key_length = len(self.key)
        for character in self.key:
            self.offsets.append(int(ord(character)))
        return True

    def encrypt(self, message) -> str:
        if self.key_length == 0:
            return message

        output_list = list()
        wrap = 0
        bias = 0

        for i in range(len(message)):
            offset = self.offsets[i%self.key_length]
            ordinal_value = ord(message[i])
            if ordinal_value >= 65 and ordinal_value <= 90:
                bias = 65
                wrap = 26
            elif ordinal_value >= 97 and ordinal_value <= 122:
                bias = 97
                wrap = 26
            elif ordinal_value >= 48 and ordinal_value <= 57:
                bias = 48
                wrap = 10
            elif ordinal_value >= 32 and ordinal_value <= 47:
                bias = 32
                wrap = 15
            else:
                bias = 0
                wrap = ordinal_value+1

            zero_biased = ordinal_value - bias
            wrapped = (zero_biased + offset) % wrap
            rebiased = wrapped + bias

            output_list.append(chr(rebiased))

        encrypted = "".join(output_list)
        return encrypted


    def decrypt(self, message) -> str:
        if self.key_length == 0:
            return message

        output_list = list()
        wrap = 0
        bias = 0

        for i in range(len(message)):
            offset = self.offsets[i % self.key_length]
            ordinal_value = ord(message[i])
            if ordinal_value >= 65 and ordinal_value <= 90:
                bias = 65
                wrap = 26
            elif ordinal_value >= 97 and ordinal_value <= 122:
                bias = 97
                wrap = 26
            elif ordinal_value >= 48 and ordinal_value <= 57:
                bias = 48
                wrap = 10
            elif ordinal_value >= 32 and ordinal_value <= 47:
                bias = 32
                wrap = 15
            else:
                bias = 0
                wrap = ordinal_value + 1

            zero_biased = ordinal_value - bias
            wrapped = (zero_biased - offset) % wrap
            rebiased = wrapped + bias

            output_list.append(chr(rebiased))

        decrypted = "".join(output_list)
        return decrypted


if __name__ == "__main__":
    crypto = vignere_cipher()

    message = "Toast is the best type of bread, for it demonstrates the application of many scientific processes"
    key = "ABCDE"
    crypto.set_key(key)
    encrypted = crypto.encrypt(message)
    decrypted = crypto.decrypt(encrypted)

    print(f"{message} encrypted with a shift of {key} is: {encrypted}")
    print(f"{encrypted} decrypted with a shift of {key} is: {decrypted}")

    message = "ABCDE12345abcde !\"#$%"
    key = "Networks and Security is the best module ever!"
    crypto.set_key(key)
    encrypted = crypto.encrypt(message)
    decrypted = crypto.decrypt(encrypted)

    print(f"{message} encrypted with a shift of {key} is: {encrypted}")
    print(f"{encrypted} decrypted with a shift of {key} is: {decrypted}")