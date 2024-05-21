import hashlib
import base64

def generate_key(pack_identifier: str,
                 user_id: str,
                 secret_phrase:str,
                 length: int = 32) -> str:
    """
    use the pack_identifier, user_id and secret_phrase to generate a key for encryption processes.
    """      
    hash_digest = hashlib.sha256((user_id + pack_identifier + secret_phrase).encode()).digest()
    base64_encoded = base64.urlsafe_b64encode(hash_digest).decode('utf-8')

    return base64_encoded[:length]
