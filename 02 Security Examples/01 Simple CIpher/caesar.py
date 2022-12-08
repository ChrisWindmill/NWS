class caesar_cipher:
    """ caesar_cipher

    Handles encryption of upper, lower, numeric, and symbols within their own ranges (e.g. upper->upper)
    """
    def __init__(self):
        self.offset = 0

    def set_key(self, key) -> bool:
        try:
            value = int(key)
        except ValueError:
            return False
        self.offset = value
        return True

    def encrypt(self, message) -> str:
        output_list = list()
        wrap = 0
        bias = 0

        for character in message:
            ordinal_value = ord(character)
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
            wrapped = (zero_biased + self.offset) % wrap
            rebiased = wrapped + bias

            output_list.append(chr(rebiased))

        encrypted = "".join(output_list)
        return encrypted


    def decrypt(self, message) -> str:
        output_list = list()
        wrap = 0
        bias = 0

        for character in message:
            ordinal_value = ord(character)
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
            wrapped = (zero_biased - self.offset) % wrap
            rebiased = wrapped + bias

            output_list.append(chr(rebiased))

        decrypted = "".join(output_list)
        return decrypted


if __name__ == "__main__":
    crypto = caesar_cipher()

    message = "Toast is the best type of bread, for it demonstrates the application of many scientific processes"
    key = 5
    crypto.set_key(key)
    encrypted = crypto.encrypt(message)
    decrypted = crypto.decrypt(encrypted)

    print(f"{message} encrypted with a shift of {key} is: {encrypted}")
    print(f"{encrypted} decrypted with a shift of {key} is: {decrypted}")

    message = "ABCDE12345abcde !\"#$%"
    key = 5
    crypto.set_key(key)
    encrypted = crypto.encrypt(message)
    decrypted = crypto.decrypt(encrypted)

    print(f"{message} encrypted with a shift of {key} is: {encrypted}")
    print(f"{encrypted} decrypted with a shift of {key} is: {decrypted}")