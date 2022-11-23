class nws_encryption:
    def __init__(self):
        self._enabled = False
        self._method = None
        self._alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!£$%^&*()-+={}[]:;@'<,>.?/\\# "
        self._caesarkey = None
        self._vignerekey = None

    def toggle_enable(self):
        self._enabled = not self._enabled
        return self._enabled

    def set_caesar_key(self, key):
        try:
            self._caesarkey = int(key)
        except TypeError:
            self._caesarkey = 0
            return None
        return self._caesarkey

    def set_vigenere_key(self, key):
        try:
            self._vigenerekey = str(key)
        except TypeError:
            self._vignerekey = "Derby"
            return None
        return self._caesarkey

    def set_method(self, method):
        if method.lower() == "caesar":
            self._method = "caesar"
        elif method.lower() == "vigenere":
            self._method = "vigenere"
        else:
            self._method = None

    def encrypt(self, message) -> str:
        if self._enabled:
            if self._method == "caesar":
                return self._caesarcipherencrypt(message)
            elif self._method == "vigenere":
                return self._vigeneresquareencrypt(message)
        return message

    def decrypt(self, message) -> str:
        if self._enabled:
            if self._method == "caesar":
                return self._caesarcipherdecrypt(message)
            elif self._method == "vigenere":
                return self._vigeneresquaredecrypt(message)
        return message

    def _caesarcipherencrypt(self, message) -> str:
        try:
            message = str(message)
        except TypeError:
            return ""

        # perform caesar cipher here

    def _vigeneresquareencrypt(self, message) -> str:
        try:
            message = str(message)
        except TypeError:
            return ""

        # perform vigenere square here

    def _caesarcipherdecrypt(self, message) -> str:
        try:
            message = str(message)
        except TypeError:
            return ""

        # perform caesar cipher here

    def _vigeneresquaredecrypt(self, message) -> str:
        try:
            message = str(message)
        except TypeError:
            return ""

        # perform vigenere square here



