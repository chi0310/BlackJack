import os


class ENV:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', None)
    if SECRET_KEY is None:
        raise RuntimeError('JWT_SECRET_KEY not found')

    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
