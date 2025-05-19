from flask import Blueprint, request, jsonify

from ..models.database import db
from ..models.models import User
from ..utils.auth import require_auth
from ..utils.response import api_response

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    nickname=data.get('nickname')
    username = data.get('username')
    password = data.get('password')

    if not nickname or not username or not password:
        return api_response(400, '缺少参数'), 400

    if User.query.filter_by(username=username).first():
        return api_response(400, '用户名已存在'), 400

    user = User(username=username,nickname=nickname)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return api_response(201, '注册成功')


@user_bp.route('/info', methods=['GET'])
@require_auth
def get_user_info(user_id):
    """获取用户信息"""
    user = User.query.get(user_id)

    if not user:
        return api_response(404, '用户不存在'), 404  # 用户不存在

    user_data = {
        'user_id': user.id,
        'nickname': user.nickname,
        'avatar': user.avatar,
    }
    return jsonify({'errno': 0, 'data': user_data, 'message': '获取用户信息成功'})

@user_bp.route('/logout', methods=['GET'])
@require_auth
def logout(user_id):
    """用户登出"""
    return api_response(200, '登出成功')