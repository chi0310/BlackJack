import os
from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import jwt

SECRET_KEY = os.getenv('JWT_SECRET_KEY', None)
if SECRET_KEY is None:
    raise RuntimeError('No JWT_SECRET_KEY')
else:
    print(SECRET_KEY)
ALGORITHM = 'HS256'


# ref:
# https://github.com/testdrivenio/fastapi-jwt/blob/main/app/auth/auth_bearer.py
class JWT(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403,
                                    detail='Invalid authentication scheme.')
            payload = self.verify_jwt(credentials.credentials)
            if payload is None:
                raise HTTPException(status_code=403,
                                    detail='Invalid token or expired token.')
            return payload
        else:
            raise HTTPException(status_code=403,
                                detail='invalid authorization code')

    def verify_jwt(self, token: str):
        try:
            payload = jwt.decode(token,
                                 SECRET_KEY, [ALGORITHM],
                                 options={'verify_signature': False})
            exp = payload.get('exp', None)
            if (exp is None or exp <
                    datetime.now(tz=timezone(timedelta(hours=8))).timestamp()):
                payload = None
        except Exception:
            payload = None
        else:
            return payload

    # ref: https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/?h=jwt
    @staticmethod
    def create_access_token(data: dict,
                            expires_data: Union[timedelta,
                                                None] = None) -> str:
        to_encode = data.copy()
        if expires_data:
            expire = datetime.now(tz=timezone(timedelta(hours=8))) + \
                    expires_data
        else:
            expire = datetime.now(tz=timezone(timedelta(hours=8))) + \
                    timedelta(minutes=15)
        import time
        print(time.time())
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
