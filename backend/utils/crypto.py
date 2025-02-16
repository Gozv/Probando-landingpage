from cryptography.fernet import Fernet
from backend import app

def encrypt_data(data):
    cipher = Fernet(app.config['CRYPTO_KEY'])
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data):
    cipher = Fernet(app.config['CRYPTO_KEY'])
    return cipher.decrypt(encrypted_data).decode()