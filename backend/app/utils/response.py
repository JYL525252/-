from flask import jsonify

def api_response(code=200, message='成功', data=None):
    response = {'code': code, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response)
