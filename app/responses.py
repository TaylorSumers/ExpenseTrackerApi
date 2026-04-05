from flask import jsonify


def success_response(data=None, message: str | None = None, status_code: int = 200):
	payload = {
		'data': data
	}
	if message:
		payload['message'] = message
	return jsonify(payload), status_code

def error_response(message: str, code: str,  status_code: int, details: dict | None = None):
	payload = {
		'error': {
			'code': code,
			'message': message
		}
	}
	if details:
		payload['error']['details'] = details
	return jsonify(payload), status_code