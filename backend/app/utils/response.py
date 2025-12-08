from flask import jsonify

def ok(data=None, message="OK"):
    return jsonify({"code": "OK", "message": message, "data": data or {}}), 200

def bad_request(message="BAD_REQUEST"):
    return jsonify({"code": "BAD_REQUEST", "message": message, "data": {}}), 400

def unauthorized(message="UNAUTHORIZED"):
    return jsonify({"code": "UNAUTHORIZED", "message": message, "data": {}}), 401

def forbidden(message="FORBIDDEN"):
    return jsonify({"code": "FORBIDDEN", "message": message, "data": {}}), 403

def conflict(message="CONFLICT"):
    return jsonify({"code": "CONFLICT", "message": message, "data": {}}), 409
