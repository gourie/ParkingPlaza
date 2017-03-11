__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

import uuid
import hashlib

class securepasswordforstorage:
    """
    Hash passwords with SHA256 for secure storage in DB/config file
    """
    def hash_password(self, password):
        # uuid is used to generate a random number
        nonce = uuid.uuid4().hex
        return hashlib.sha256(nonce.encode() + password.encode()).hexdigest() + ':' + nonce

    def check_password(self, hashed_password, user_password):
        password, nonce = hashed_password.split(':')
        return password == hashlib.sha256(nonce.encode() + user_password.encode()).hexdigest()