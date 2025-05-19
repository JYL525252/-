from flask import Blueprint, request, jsonify
from ..models.database import db
from ..models.models import Group
from ..utils.auth import require_auth

group_bp = Blueprint('group', __name__)

@group_bp.route('/getGroupList', methods=['POST'])
@require_auth
def get_group_list(user_id):
    try:
        data = request.get_json()  # 获取请求体中的 JSON 数据

        page = int(data.get('page', 1))  # 从请求体中获取 page，默认值为 1
        pagesize = int(data.get('pagesize', 20))  # 从请求体中获取 pagesize，默认值为 20

        groups = Group.query.filter_by(user_id=user_id).paginate(page=page, per_page=pagesize)
        group_list = [{
            'id': group.id,
            'title': group.title,
            'created_at': group.created_at.isoformat()
        } for group in groups.items]

        return jsonify({
            'success': True,
            'data': {
                'list': group_list,
                'count': groups.total
            },
            'message': '群组列表获取成功'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': '获取群组列表失败', 'details': str(e)}), 500

@group_bp.route('/getGroup', methods=['POST'])
@require_auth
def get_group(user_id):
    try:
        data = request.get_json()  # 获取请求体中的 JSON 数据

        group_id = data.get('id')

        if group_id is None:
            return jsonify({'success': False, 'message': '群组不存在'}), 404

        group = Group.query.get(group_id)
        if group:
            return jsonify({
                'success': True,
                'data': {
                    'id': group.id,
                    'title': group.title,
                    'created_at': group.created_at.isoformat()
                },
                'message': '群组信息获取成功'
            }), 200
        else:
            return jsonify({'success': False, 'message': '群组不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': '获取群组信息失败', 'details': str(e)}), 500

@group_bp.route('/saveGroup', methods=['POST'])
@require_auth
def save_group(user_id):
    try:
        data = request.get_json()
        group_id = data.get('id')
        title = data.get('title', "新的会话")

        if group_id:
            # 更新现有群组
            group = Group.query.get(group_id)
            if group:
                group.title = title
                db.session.commit()
                return jsonify({
                    'success': True,
                    'data': {
                        'id': group.id,
                        'title': group.title
                    },
                    'message': '群组更新成功'
                }), 200
            else:
                return jsonify({'success': False, 'message': '群组不存在'}), 404
        else:
            # 创建新群组
            new_group = Group(title=title, user_id=user_id)
            db.session.add(new_group)
            db.session.commit()
            return jsonify({
                'success': True,
                'data': {
                    'id': new_group.id,
                    'title': new_group.title
                },
                'message': '群组创建成功'
            }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': '保存群组失败', 'details': str(e)}), 500

@group_bp.route('/delGroup', methods=['POST'])
@require_auth
def del_group(user_id):
    try:
        group_id = request.get_json().get('id')  # 从请求体中获取 ID
        group = Group.query.get(group_id)

        if group:
            db.session.delete(group)
            db.session.commit()
            return jsonify({'success': True, 'message': '群组删除成功'}), 200
        else:
            return jsonify({'success': False, 'message': '群组不存在'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': '删除群组失败', 'details': str(e)}), 500
