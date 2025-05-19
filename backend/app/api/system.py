from flask import Blueprint, jsonify

system_bp = Blueprint('system', __name__)

@system_bp.route('/login/system', methods=['POST'])
def get_system_info():
    """获取系统信息 (例如，Logo, 页面标题等)"""
    system_info = {
        'page_title': '电力知识问答助手',
        'copyright': '© 2025 电力知识问答助手',
        'copyright_link': 'https://www.baidu.com'
    }

    return jsonify({'errno': 0, 'data': system_info, 'message': '获取系统信息成功'})