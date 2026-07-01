from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hasher(password:str):
    return pwd_context.hash(password)

def verifier(plain,hashed):
    return pwd_context.verify(plain,hashed)