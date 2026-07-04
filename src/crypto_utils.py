import os
import base64

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def generate_key(password: str, salt: bytes) -> bytes:
    password_bytes = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    salt = os.urandom(16)
    key = generate_key(password, salt)
    fernet = Fernet(key)

    with open(input_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    with open(output_path, "wb") as file:
        file.write(salt + encrypted_data)


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    with open(input_path, "rb") as file:
        data = file.read()

    salt = data[:16]
    encrypted_data = data[16:]

    key = generate_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        raise ValueError("Wrong password or corrupted file.")

    with open(output_path, "wb") as file:
        file.write(decrypted_data)