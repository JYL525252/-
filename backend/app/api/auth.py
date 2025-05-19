from flask import Blueprint, request, jsonify

from ..models.models import User
from ..utils.auth import generate_token, require_auth
from ..utils.response import api_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return api_response(400, '缺少参数'), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):  # 使用 check_password 方法验证密码
        return api_response(401, '用户名或密码错误'), 401

    token = generate_token(user.id)
    return jsonify({'success': True, 'data': {'token': token}, 'message': '登录成功'}), 200


@auth_bp.route('/getInfo', methods=['GET'])
@require_auth
def get_info(user_id):
    """获取用户信息 (需要认证)"""
    user = User.query.get(user_id)
    if not user:
        return api_response(404, '用户不存在'), 404

    return jsonify({'success': True, 'data': user.to_dict(), 'message': '获取用户信息成功'}), 200
