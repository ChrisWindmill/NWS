import hashlib
import random

class rsa_signature:
    """ RSA Digital Signature

    Choose two large prime numbers p and q
    Calculate n=p*q
    Select public key e such that it is not a factor of (p-1)*(q-1)
    Select private key d such that the following equation is true (d*e)mod(p-1)(q-1)=1 or d is inverse of E in modulo (p-1)*(q-1)
    """
    def __init__(self):
        self.publicKey = None
        self.privateKey = None

    def gcd(self, m, n):
        """gcd

         Calculates the greatest common denominator of m and n"""
        if n == 0:          # Handles the division by 0 case
            return m
        else:
            remainder = m % n
            return self.gcd(n, remainder)

    def multiplicative_inverse(self, a, b):
        """
        multiplicative_inverse

        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        https://medium.com/geekculture/euclidean-algorithm-using-python-dc7785bb674a
        """
        r1 = a
        r2 = b
        t = int(0)
        newt = int(1)

        while r2 > 0:
            quotient = r1 // r2

            # Calculate R values
            tempr = r1 - quotient * r2
            r1 = r2
            r2 = tempr

            # Calculate T values
            tempt = t - quotient * newt
            t = newt
            newt = tempt

        if t < 0:
            t = t % a

        return r1, t

    def generate_keys(self, p, q):
        """generate_keys

        Generate public and private keys from p and q"""
        n = p * q
        totient = (p - 1) * (q - 1)

        # Generate encryption key in range 1 < key < Pn
        keys = []

        for i in range(2, totient):
            gcd = self.gcd(totient, i)

            if gcd == 1:
                keys.append(i)

        # select e as a co-prime value of n (gcd = 1)
        print(len(keys))
        e = random.choice(keys)

        # Obtain inverse of encryption key in Z_Pn
        r, d = self.multiplicative_inverse(totient, e)
        if r == 1:
            d = int(d)
            print("decryption key is: ", d)
            self.publicKey = (n,e)
            self.privateKey = (p,q,d)

        else:
            print("Choose a different encryption key - the multiplicative inverse does not exist")

    def encryptPrivate(self, message):
        bytVal = bytes(message, "utf-8")
        intVal = int.from_bytes(bytVal, byteorder="big")

        S = (intVal ** self.privateKey[2]) % (self.privateKey[0] * self.privateKey[1])
        return S

    def decryptPublic(self, message):
        intVal = (message ** self.publicKey[1]) % self.publicKey[0]
        bytVal = intVal.to_bytes((intVal.bit_length() + 7) // 8, byteorder="big")
        stringVal = bytVal.decode("utf-8")
        return stringVal

    def decryptPrivate(self, message):
        intVal = (message ** self.publicKey[1]) % self.publicKey[0]
        bytVal = intVal.to_bytes((intVal.bit_length() + 7) // 8, byteorder="big")
        stringVal = bytVal.decode("utf-8")
        return stringVal


    def encryptPublic(self, message):
        bytVal = bytes(message, "utf-8")
        intVal = int.from_bytes(bytVal, byteorder="big")
        S = (intVal ** self.privateKey[2]) % (self.privateKey[0] * self.privateKey[1])
        return S

if __name__ == "__main__":
    crypto = rsa_signature()
    crypto.generate_keys(823, 953)

    message = "the"
    sigs = []
    wordy = []

    for character in message:
        S = crypto.encryptPrivate(character)
        sigs.append(S)

    print(sigs)

    for val in sigs:
        D = crypto.decryptPublic(val)
        wordy.append(D)

    print(wordy)

    message = "the"
    sigs = []
    wordy = []

    for character in message:
        S = crypto.encryptPublic(character)
        sigs.append(S)

    print(sigs)

    for val in sigs:
        D = crypto.decryptPrivate(val)
        wordy.append(D)

    print(wordy)
   

