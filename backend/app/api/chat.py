import requests
from flask import Blueprint, request, Response, stream_with_context, jsonify
import json

from .. import Config
from ..models.database import db
from ..models.models import Message
from ..utils.auth import require_auth
from ..utils.response import api_response

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/sendText', methods=['POST'])
@require_auth
def send_text(user_id):
    data = request.get_json()
    group_id = data.get('group_id')
    message = data.get('message')

    if group_id is None or group_id == "" or message is None or message == "":
        return api_response(400, '缺少 group_id 或 message'), 400

    # 保存用户消息
    user_message = Message(group_id=group_id, user='我', message=message)
    db.session.add(user_message)
    db.session.commit()

    # 获取历史对话作为上下文（限制最近 10 条消息）
    history = Message.query.filter_by(group_id=group_id).order_by(Message.created_at.asc()).limit(10).all()
    messages = [
        {"role": "user" if msg.user == '我' else "assistant", "content": msg.message}
        for msg in history
    ]
    if messages and messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": message})
    elif not messages:
        messages = [{"role": "user", "content": message}]

    # LLaMA-Factory 服务端的 URL
    llama_factory_url = Config.LLAMA_FACTORY_URL

    def generate_ai_response():
        try:
            # 构建 LLaMA-Factory API 的请求体
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.95,
                "n": 1,
                "max_tokens": 1024,
                "stop": None,
                "stream": True,
                "tools": [],
            }

            # 发送 POST 请求到 LLaMA-Factory 服务端，并启用流式传输
            with requests.post(llama_factory_url, json=payload, stream=True, timeout=60) as response:
                response.raise_for_status()  # 检查 HTTP 错误

                # 从 LLaMA-Factory 服务端读取 SSE 数据，并逐行发送给客户端
                for line in response.iter_lines():
                    if line:  # 过滤掉空行
                        try:
                            # 解析 SSE 数据
                            decoded_line = line.decode('utf-8')
                            if decoded_line.startswith("data:"):
                                if decoded_line.strip() == "data: [DONE]":
                                    # 遇到 [DONE] 消息，直接结束生成器，不发送任何消息
                                    return

                                json_data = json.loads(decoded_line[5:])  # 去掉 "data:" 前缀并解析 JSON

                                # 提取 content (delta content)
                                if 'choices' in json_data and len(json_data['choices']) > 0 and 'delta' in \
                                        json_data['choices'][0] and 'content' in json_data['choices'][0]['delta']:
                                    content = json_data['choices'][0]['delta']['content']
                                    yield f"{content}".encode('utf-8')  # 只发送 content

                        except json.JSONDecodeError:
                            print(f"JSONDecodeError: {line}")
                            yield f"data: {json.dumps({'error': 'JSONDecodeError'})}\n\n".encode('utf-8')  # 发送错误信息
                        except Exception as e:
                            print(f"Error processing SSE line: {e}")
                            yield f"{json.dumps({'error': str(e)})}\n\n".encode('utf-8')  # 发送错误信息

        except requests.exceptions.RequestException as e:
            error_message = f"[error]LLaMA-Factory 服务错误: {str(e)}"
            yield f"{json.dumps({'error': error_message})}\n\n".encode('utf-8')
        except Exception as e:
            error_message = f"[error]未知错误: {str(e)}"
            yield f"{json.dumps({'error': error_message})}\n\n".encode('utf-8')

    return Response(stream_with_context(generate_ai_response()), content_type='text/event-stream')


@chat_bp.route('/saveAIMessage', methods=['POST'])
@require_auth
def save_ai_message(user_id):
    data = request.get_json()
    group_id = data.get('group_id')
    message = data.get('message')

    if group_id is None or group_id == "" or message is None or message == "":
        return api_response(400, '缺少 group_id 或 message'), 400

    # 保存AI消息
    ai_message = Message(group_id=group_id, user='AI', message=message)
    db.session.add(ai_message)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': '保存AI消息成功'
    }), 200


@chat_bp.route('/getHistoryMsg', methods=['POST'])
@require_auth
def get_history_msg(user_id):
    try:
        data = request.get_json()  # 获取请求体中的 JSON 数据
        group_id = data.get('group_id')  # 从请求体中获取 group_id
        page = int(data.get('page', 1))  # 从请求体中获取 page，默认值为 1
        pagesize = int(data.get('pagesize', 10))  # 从请求体中获取 pagesize，默认值为 10

        if not group_id:
            return api_response(400, '缺少 group_id'), 400

        messages = Message.query.filter_by(group_id=group_id).order_by(Message.created_at.asc()).paginate(page=page,
                                                                                                          per_page=pagesize)

        message_list = [{
            'id': msg.id,
            'group_id': msg.group_id,
            'user': msg.user,
            'message': msg.message,
            'created_at': msg.created_at.isoformat()
        } for msg in messages.items]

        return jsonify({
            'success': True,
            'data': {
                'list': message_list,
                'count': messages.total
            },
            'message': '历史消息获取成功'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': '获取历史消息失败', 'details': str(e)}), 500
