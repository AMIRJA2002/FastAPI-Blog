import jwt
from config import get_settings
import time

settings = get_settings()


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token, f'{settings.SECRET_KEY}', algorithms=['HS256'])
    return decoded_token if decoded_token['exp'] >= time.time() else None
