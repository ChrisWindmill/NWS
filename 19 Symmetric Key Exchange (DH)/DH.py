import random


class diffie_hellman:
    """ Diffie-Hellman key generation

        (g^a mod p)^b mod p = g^(ab) mod p = (g^b mod p)^a mod p
    """
    def __init__(self, modulus, base, private_key = None):
        self.p = modulus
        self.g = base

        if not private_key:
            self.private_key = random.randint(1000, 5000)
        else:
            self.private_key = int(private_key)
        self.symmetric_key = 0

    def calculate_partial_key(self):
        return (self.g ** self.private_key) % self.p

    def calculate_full_key(self, partial_key):
        self.symmetric_key = (partial_key ** self.private_key) % self.p
        return self.symmetric_key


if __name__ == "__main__":
    Alice = diffie_hellman(250, 12)
    Bob = diffie_hellman(250, 12)

    print(f"Alice generates private key: {Alice.private_key}")
    print(f"Bob   generates private key: {Bob.private_key}")

    PartialKeyA = Alice.calculate_partial_key()
    PartialKeyB = Bob.calculate_partial_key()

    print(f"Alice sends Bob {PartialKeyA}")
    print(f"Bob sends Alice {PartialKeyB}")

    KeyA = Alice.calculate_full_key(PartialKeyB)
    KeyB = Bob.calculate_full_key(PartialKeyA)

    print(f"Alice sees key\t: {KeyA}")
    print(f"Bob   sees key\t: {KeyB}")

