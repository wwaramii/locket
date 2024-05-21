import hashlib
import base64

def generate_identifier(user_id: str, 
                        secret_phrase: str,
                        length: int = 16) -> str:
    """
    will generate a identifier using the user_id and secret_phrase based on length.
    this will be used to identify document packs.
    """
    if length < 8:
        raise ValueError("Length must be more than or equal 8.")
        
    hash_digest = hashlib.sha256((user_id + secret_phrase).encode()).digest()
    base64_encoded = base64.urlsafe_b64encode(hash_digest).decode('utf-8')

    return base64_encoded[:length]
