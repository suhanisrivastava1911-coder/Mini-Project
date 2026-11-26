"""AES-based encryption for sensitive profile data (e.g. phone, notes, financial records)."""
import base64
import hashlib
from cryptography.fernet import Fernet
from backend.app.config import Config


def _get_fernet_instance():
    key_src = Config.AES_ENCRYPTION_KEY.encode("utf-8")
    # Derive a valid 32-byte URL-safe base64 key
    digest = hashlib.sha256(key_src).digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return Fernet(fernet_key)


def encrypt_data(plain_text: str) -> str:
    """Encrypt a string and return a safe ascii string."""
    if not plain_text:
        return ""
    try:
        f = _get_fernet_instance()
        encrypted = f.encrypt(plain_text.encode("utf-8"))
        return encrypted.decode("ascii")
    except Exception:
        return plain_text


def decrypt_data(cipher_text: str) -> str:
    """Decrypt an encrypted string."""
    if not cipher_text:
        return ""
    try:
        f = _get_fernet_instance()
        decrypted = f.decrypt(cipher_text.encode("ascii"))
        return decrypted.decode("utf-8")
    except Exception:
        return cipher_text
