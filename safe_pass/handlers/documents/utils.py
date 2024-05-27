import random
import string


def generate_password(length: int = 8) -> str:
    """
    Generate a safe password containing letters, numbers, and symbols.

    :param length: Length of the generated password. Default is 8 characters.
    :return: Generated password as a string.
    """
    if length < 4:
        raise ValueError("Password length should be at least 4 to ensure it contains letters, numbers, and symbols.")

    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Ensure the password contains at least one letter, one digit, and one symbol
    password = [
        *[random.choice(letters) for _ in range(random.randint(length // 3, length // 2))],
        *[random.choice(digits) for _ in range(random.randint(length // 3, length // 2))],
        *[random.choice(symbols) for _ in range(random.randint(length // 3, length // 2))],
    ]
    # Shuffle the password list to ensure randomness
    random.shuffle(password)

    # Join the list into a string and return it
    return ''.join(password)[:length]
