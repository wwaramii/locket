from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_document(document: str, key: str) -> bytes:
    """
    Encrypts a document using the provided key.
    
    Parameters:
    - document (str): The plaintext document to be encrypted.
    - key (str): The encryption key.
    
    Returns:
    - bytes: The IV prepended to the ciphertext.
    """
    # Ensure the key is 32 bytes long (256 bits)
    key_bytes = key.encode('utf-8')[:32].ljust(32, b'\0')
    
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    
    # Initialize AES cipher in CBC mode with the generated IV
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    
    # Create an encryptor object
    encryptor = cipher.encryptor()
    
    # Pad the plaintext document to be a multiple of the block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(document.encode('utf-8')) + padder.finalize()
    
    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Prepend the IV to the ciphertext
    encrypted_data = iv + ciphertext
    
    return encrypted_data


def decrypt_document(encrypted_data: bytes, key: str) -> str:
    """
    Decrypts an encrypted document using the provided key.
    
    Parameters:
    - encrypted_data (bytes): The IV prepended to the ciphertext.
    - key (str): The encryption key.
    
    Returns:
    - str: The decrypted plaintext document.
    """
    # Ensure the key is 32 bytes long (256 bits)
    key_bytes = key.encode('utf-8')[:32].ljust(32, b'\0')
    
    # Extract the IV from the beginning of the encrypted data
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    # Initialize AES cipher in CBC mode with the extracted IV
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    
    # Create a decryptor object
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    # Return the decrypted plaintext document
    return data.decode('utf-8')

