import os
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


MAGIC_HEADER = b"FET2"


def generate_key(password: str, salt: bytes) -> bytes:
    password_bytes = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password_bytes))


def hash_access_password(access_password: str, access_salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        access_password.encode(),
        access_salt,
        390000,
    )


def encrypt_file(input_path: str, output_path: str, access_password: str, encryption_password: str) -> None:
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input file does not exist.")

    access_salt = os.urandom(16)
    encryption_salt = os.urandom(16)

    access_hash = hash_access_password(access_password, access_salt)

    key = generate_key(encryption_password, encryption_salt)
    fernet = Fernet(key)

    with open(input_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    output_folder = os.path.dirname(output_path)
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    with open(output_path, "wb") as file:
        file.write(MAGIC_HEADER + access_salt + encryption_salt + access_hash + encrypted_data)

    os.remove(input_path)


def get_decrypted_data(input_path: str, access_password: str, encryption_password: str) -> bytes:
    if not os.path.exists(input_path):
        raise FileNotFoundError("Encrypted file does not exist.")

    with open(input_path, "rb") as file:
        data = file.read()

    if not data.startswith(MAGIC_HEADER):
        raise ValueError("This is not a valid encrypted file from this tool.")

    access_salt = data[4:20]
    encryption_salt = data[20:36]
    stored_access_hash = data[36:68]
    encrypted_data = data[68:]

    entered_access_hash = hash_access_password(access_password, access_salt)

    if entered_access_hash != stored_access_hash:
        raise ValueError("Wrong access password.")

    key = generate_key(encryption_password, encryption_salt)
    fernet = Fernet(key)

    try:
        return fernet.decrypt(encrypted_data)
    except InvalidToken:
        raise ValueError("Wrong encryption password or corrupted file.")


def decrypt_file(input_path: str, output_path: str, access_password: str, encryption_password: str) -> None:
    decrypted_data = get_decrypted_data(input_path, access_password, encryption_password)

    output_folder = os.path.dirname(output_path)
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    with open(output_path, "wb") as file:
        file.write(decrypted_data)

    os.remove(input_path)