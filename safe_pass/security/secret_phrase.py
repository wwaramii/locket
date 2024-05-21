import secrets
import string

def generate_secret_phrase(length:int = 8):
    """
    this will generate a 8 or 16 character secret phrase.
    """
    if length not in [8, 16]:
        raise ValueError("Secret phrase length should be 8 or 16.")
    
    return ''.join([secrets.choice(string.ascii_letters + string.digits) for _ in range(length)])

