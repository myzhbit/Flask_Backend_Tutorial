import re

from flask import Blueprint, request, jsonify, session, Response

from controller.user import UserController
from models import db_session
from models.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['POST'])
def create_user():
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Invalid request'}), 400

    email = req.get('email', None)
    nickname = req.get('nickname', None)
    password = req.get('password', None)

    email_re = re.match(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$', email)
    pass_re = re.match(r'^[A-Za-z0-9]{6,}$', password)
    nickname_re = re.match(r'^[A-Za-z0-9]{3,20}$', nickname)
    if not email_re or not pass_re:
        return jsonify({'error': 'Invalid email or password'}), 400
    if not nickname_re:
        return jsonify({'error': 'Invalid nickname'}), 400

    if UserController.create_user(email, password, nickname):
        return jsonify({'success': 'User registered'}), 200
    else:
        return jsonify({'error': 'User already exists'}), 400


@user_bp.route('/user', methods=['GET'])
def get_user_info():
    email = session.get('email', None)
    if not email:
        return jsonify({'error': 'Not logged in'}), 403

    user_dict = UserController.get_user_info(email)
    if not user_dict:
        del session['email']
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user_dict), 200


@user_bp.route('/logout', methods=['POST'])
def logout():
    email = session.get('email', None)
    if not email:
        return jsonify({'error': 'Not logged in'}), 403

    session.pop('email')
    return jsonify({'success': 'Logout successful'}), 200


@user_bp.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Invalid request'}), 400

    email = req.get('email', None)
    password = req.get('password', None)

    if not email or not password:
        return jsonify({'error': 'Invalid email or password'}), 400

    if UserController.login(email, password):
        session['email'] = email
        return jsonify({'success': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Login failed'}), 400


@user_bp.route('/avatar/<string:user_hash>', methods=['GET'])
def get_user_avatar(user_hash):
    avatar, mimetype = UserController.get_user_avatar(user_hash)
    if not avatar:
        return jsonify({'error': 'User not found'}), 404
    res = Response(avatar, mimetype=mimetype, content_type=mimetype)
    return res


@user_bp.route('/avatar/modify', methods=['POST'])
def modify_user_avatar():
    email = session.get('email', None)
    if not email:
        return jsonify({'error': 'Not logged in'}), 403

    user = db_session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    avatar = request.files.get('file', None)
    if not avatar:
        return jsonify({'error': 'No avatar'}), 400

    if UserController.modify_user_avatar(user, avatar):
        return jsonify({'success': 'Avatar modified'}), 200
    else:
        return jsonify({'error': 'Avatar not modified'}), 400
