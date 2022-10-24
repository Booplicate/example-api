"""
Module implements encoding/hashing/encryption for the services
"""

from passlib.hash import bcrypt
from base64 import (
    b64encode,
    b64decode
)


def hash_string(string: str) -> str:
    """
    Hashes a string using brypt and encodes it
    """
    raw_hash = bcrypt.hash(string)
    raw_hash_bytes = raw_hash.encode("utf-8")
    hash_bytes = b64encode(raw_hash_bytes)

    return hash_bytes.hex()

def verify_string(string: str, hashed_string: str) -> bool:
    """
    Verifies a string against a hash
    """
    hash_bytes = bytes.fromhex(hashed_string)
    raw_hash_bytes = b64decode(hash_bytes)
    raw_hash = raw_hash_bytes.decode("utf-8")

    return bcrypt.verify(string, raw_hash)
