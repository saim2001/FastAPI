from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(pwd:str):
    hashed_pwd=pwd_context.hash(pwd)
    return hashed_pwd
def verify(plain_pwd,hashed_pwd):
    return pwd_context.verify(plain_pwd,hashed_pwd)