from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pw(pw):
    return pwd_context.hash(pw)


def verify_pw(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)
