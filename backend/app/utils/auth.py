from flask import request, current_app
from functools import wraps
from http import HTTPStatus
from .. import Config
import jwt
import datetime

JWT_SECRET_KEY = Config.JWT_SECRET

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-token')
        if not token:
            return {'errno': 403, 'message': '缺少 Token'}, HTTPStatus.OK
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return {'errno': 403, 'message': 'Token 过期'}, HTTPStatus.OK
        except jwt.InvalidTokenError:
            return {'errno': 403, 'message': '无效的 Token'}, HTTPStatus.OK

        return f(user_id, *args, **kwargs)
    return decorated

def generate_token(user_id):
    """生成 JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 过期时间：7天
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token