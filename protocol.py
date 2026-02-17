import random

class OneTimePadProtocol:
    def __init__(self, n, L, d):
        self.n = n  #total of pads 
        self.L = L  #length of a pad
        self.d = d  #max undelivered messages (pad gap)
        self.pad_sequence = [random.getrandbits(L) for _ in range(n)]

        #pads distribution
        self.parties = {
            "Alice": [i for i in range(2, n, 2)],
            "Charlie": [i for i in range(1, n, 2)],
            "Bob": [i for i in range(n, 0, -2)],
            "Ellen": [i for i in range(n-1, 0, -2)],
        }
        self.last_used_pad = {party: -1 for party in self.parties}
    
    #encryption func
    def xor_encrypt(self, message, pad):
        return message ^ pad
    

    #decryption func
    def xor_decrypt(self, ciphertext, pad):
        return ciphertext ^ pad

    def send_message(self, sender, message):
        if not self.parties[sender]:
            raise ValueError(f"No available pads for {sender}")
        pad_index = self.parties[sender].pop(0)
        self.last_used_pad[sender] = pad_index
        ciphertext = self.xor_encrypt(message, self.pad_sequence[pad_index])
        return ciphertext, pad_index

    def get_message(self, ciphertext, pad_index):
        pad = self.pad_sequence[pad_index]
        return self.xor_decrypt(ciphertext, pad)

    def enforce_constraints(self, sender):
        for party in self.parties:
            if party != sender and self.last_used_pad[sender] - self.last_used_pad[party] > self.d:
                raise ValueError("Secrecy condition violated")