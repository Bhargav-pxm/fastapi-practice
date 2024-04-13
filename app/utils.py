from passlib.context import CryptContext

# * This FILE contains UTILITY FUNCTIONS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#! This function is used to hash the plain password and save in DB
def hashing(password: str):
    return pwd_context.hash(password)


#! This function is used to verify the plain password and hashed password are same or not
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
