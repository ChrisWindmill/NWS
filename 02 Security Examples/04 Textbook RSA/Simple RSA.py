import random
import hashlib


class RSA:
    """Implements the Textbook RSA public private key encryption/decryption

    Choose two large primes p and q.
    Let n=p⋅q.
    Choose e such that gcd(e,φ(n))=1 (where φ(n)=(p−1)⋅(q−1)).
    Find d such that e⋅d≡1modφ(n).

    In other words, d is the modular inverse of e, (d≡e−1modφ(n)).
    (e,n) is the public key, (d,n) the private one.

    To encrypt a message m, compute c≡memodn.
    To decrypt a ciphertext c, compute m≡cdmodn.

     Uses default exponent 65537 and default key size 2048, does not pad the messages, no side channel attack mitigation
     """
    def __init__(self, key_length=65537, exponent=2048):
        self.e = exponent
        t = 0
        p = q = 2

        # Find appropriate primes for p and q
        while RSA.gcd(self.e, t) != 1:
            p = RSA.get_random_prime(key_length // 2)
            q = RSA.get_random_prime(key_length // 2)
            t = RSA.lcm(p - 1, q - 1)

        # Find n and d values
        self.n = p * q
        self.d = RSA.multiplicative_inverse(self.e, t)

    def getPrivateKey(self):
        return self.n, self.d

    def getPublicKey(self):
        return self.n, self.e

    @staticmethod
    def get_random_prime(bit_length):
        """ Get a random prime with a given length using two layered approach to prime (note: does not guarantee this is
            a prime value, just that it is likely)
        """

        # Generate a value and determine if it is likely a prime
        while True:
            potential_prime = RSA.get_lowlevel_prime(bit_length)
            if RSA.miller_rabin_primality_check(potential_prime):
                return potential_prime

    def encrypt(self, data, e=None, n=None):
        if not e:
            e = self.e

        if not n:
            n = self.n
        """ converts a string to bytes in utf-8 format, then encodes this as an integer using big endian ordering. This
        uses the PUBLIC key for sending to this user
        """
        binary_data = data.encode("utf-8")
        int_data = int.from_bytes(binary_data, byteorder="big")
        return pow(int_data, e, n)

    def decrypt(self, encrypted_int_data, d=None, n=None):
        if not d:
            d = self.d

        if not n:
            n = self.n
        """ converts encrypted integer data back into a string, stripping leading 0s from the result - these 0s occur as
        we produce a fixed length output, in real RSA we would pad the data to avoid this issue. This uses the PRIVATE
        key for decoding messages to this user
        """
        int_data = pow(encrypted_int_data, d, n)
        bytes_data = int.to_bytes(int_data, int_data.bit_length(), byteorder="big").decode("utf-8")
        stripped_data = bytes_data.lstrip("\x00")

        return stripped_data

    def generate_signature(self, message_digest, d=None, n=None):
        if not d:
            d = self.d

        if not n:
            n = self.n
        """Use RSA private key to generate Digital Signature for given message digest (Hash). Note uses PRIVATE key to
        generate so others can decrypt our signature using the PUBLIC key
        https://www.ibm.com/docs/en/ibm-mq/7.5?topic=concepts-message-digests
        """
        int_data = int.from_bytes(message_digest, byteorder="big")
        return pow(int_data, d, n)

    def verify_signature(self, digital_signature, e=None, n=None):
        if not e:
            e = self.e

        if not n:
            n = self.n
        """Use RSA PUBLIC key to decrypt given Digital Signature - used by others to verify our signature"""
        int_data = pow(digital_signature, e, n)
        bytes_data = int.to_bytes(int_data, int_data.bit_length(), byteorder="big")
        bytes_data = bytes_data.hex().lstrip("0")
        bytes_data = bytes.fromhex(bytes_data)
        #stripped_data = bytes_data.decode("utf-8").lstrip("\x00")
        #bytes_data = stripped_data.encode()
        return bytes_data

    @staticmethod
    def generate_n_bit_odd(n):
        try:
            n = int(n)
        except ValueError:
            return False

        if n <= 1:
            return False

        return random.randrange(2 ** (n - 1) + 1, 2 ** n, 2)

    @staticmethod
    def get_lowlevel_prime(n):
        """Generate a prime candidate not divisible by first 500 primes"""
        first_500_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571]
        while True:
            # Obtain a random odd number of an appropriate length (note: length defines how much data we can encode)
            candidate = RSA.generate_n_bit_odd(n)

            # Test divisibility by pre-generated primes - if this is divisible by a prime, the number isn't prime
            is_prime = True
            for divisor in first_500_primes:
                if candidate % divisor == 0 and divisor ** 2 <= candidate:
                    is_prime = False
                    break

            if is_prime:
                return candidate

    @staticmethod
    def miller_rabin_primality_check(n, k=20):
        """Miller-Rabin Primality Test with a specified number of testing rounds

        https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
        """
        # For a given odd integer n > 3, write n as (2^s)*d+1,
        # where s and d are positive integers and d is odd.
        # Value to be tested must be at least 4 (2, 3 are automatically considered primes
        if n <= 3:
            return False

        # Even numbers are by definition not prime other than 2
        if n % 2 == 0:
            return False

        # we aim to write: n = 2^s * (d+1), starts with 2^0 * ((n-1)+1) = 1*n
        s, d = 0, n - 1

        # find powers of 2 - a bit shift right is equivalent to dividing by 2
        while d % 2 == 0:
            d >>= 1
            s += 1

        for i in range(0, k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for j in range(0, s):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                # value is a multiple of values as we didn't encounter a break from the loop
                return False

        # Value is likely a prime
        return True

    @staticmethod
    def gcd(a, b):
        """ Finds the greatest common denominator of a and b

        """
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a, b):
        """ Finds the lowest common multiple of a and b
        """
        return a // RSA.gcd(a, b) * b

    @staticmethod
    def extended_euclidian_gcd(a, b):
        """ https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
         gcd(a,b) = a*s + b*t
        """
        old_s, s = 1, 0
        old_t, t = 0, 1

        while b:
            quotient = a//b
            s, old_s = old_s - quotient*s, s
            t, old_t = old_t - quotient*t, t
            a, b = b, a % b     # Finds the GCD as per gcd method

        return a, old_s, old_t

    @staticmethod
    def multiplicative_inverse(e, m):
        g, x, y = RSA.extended_euclidian_gcd(e, m)

        # multiplicative inverse may not exist
        if g != 1:
            return -1

        # e*x + m*y = 1 => e*x = 1 (mod m)
        if x < 0:
            x = x + m
        return x


# ---- Test RSA class ----
if __name__ == "__main__":
    # Generate our two actors: Alice and Bob
    alice = RSA(512, 3)
    bob = RSA(512, 7)

    #Get each other's keys: this would normally be from a certificate or similar mechanism
    bob_modulus, bob_exponent = bob.getPublicKey()
    alice_modulus, alice_exponent = alice.getPublicKey()

    # Generate the message and the md5 hash of the message, digest is a bytes object
    message = "Textbook RSA in Python, it\'s really fun!"
    md5hash = hashlib.md5(message.encode()).digest()


    print("\n\nTest set 1: RSA encryption and decryption\n-----------------------------------------")
    # Bob encrypts the message for Alice, using her public key (e, n)
    encrypted_text = bob.encrypt(message, alice_exponent, alice_modulus)
    # Alice decrypts the message using her private key
    decrypted_text = alice.decrypt(encrypted_text)

    print(f"Bob creates the message for Alice: {message}")
    print(f"Bob encrypts the message for Alice: {encrypted_text}")
    print(f"Alice decrypts the message from Bob: {decrypted_text}")
    if message == decrypted_text:
        print("Bob successfully sent Alice an encrypted message!")

    print("\n\nTest set 2: RSA signature generation and verification\n-----------------------------------------")
    digest = hashlib.sha1(message.encode()).digest()
    signature = alice.generate_signature(digest)
    print(f"Alice generates a digest of the message she wants to send using a hash algorithm (SHA1): {digest}")
    print(f"Alice generates a digital signature for this digest using her PRIVATE key: {signature}")

    verified = bob.verify_signature(signature, alice_exponent, alice_modulus)
    print(f"Bob verifies the signature matches the SHA1 hash generated from the message: {verified}")
    if digest == verified:
        print("Bob successfully validated the signature that Alice used to confirm the message was from her")

