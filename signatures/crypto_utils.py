from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    """Gera um par de chaves RSA e retorna as chaves em formato PEM."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return public_key_pem.decode('utf-8'), private_key_pem.decode('utf-8')

def sign_message(message_bytes, private_key_pem):
    """Assina uma mensagem usando a chave privada e retorna a assinatura."""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    
    signature = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    return signature

def verify_signature(message_bytes, signature, public_key_pem):
    """Verifica uma assinatura usando a chave pública."""
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
        backend=default_backend()
    )
    
    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False

def get_public_key(user):
    """Retorna a chave pública de um usuário do banco de dados."""
    return user.public_key

def get_private_key(user):
    """Retorna a chave privada de um usuário do banco de dados."""
    return user.private_key
