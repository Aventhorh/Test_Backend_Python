from flask import request, jsonify
from models.User import db, User
from services import app
from modules.calculate_email_domain_ratio import calculate_email_domain_ratio
from modules.count_recent_users import count_recent_users
from modules.format_top_users import format_top_users
from modules.get_top_users import get_top_users

@app.route('/users', methods=['POST'])
def create_user() -> tuple:
    """
    Create a new user.

    Returns:
        tuple: A tuple containing the response JSON data and the HTTP status code.
    """
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    response = {'message': 'User created successfully'}
    return jsonify(response), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> tuple:
    """
    Get a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing the response JSON data and the HTTP status code.
    """
    user = User.query.get(user_id)
    if not user:
        response = {'message': 'User not found'}
        return jsonify(response), 404
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'registration_date': user.registration_date
    }
    return jsonify(user_data), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int) -> tuple:
    """
    Update a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing the response JSON data and the HTTP status code.
    """
    user = User.query.get(user_id)
    if not user:
        response = {'message': 'User not found'}
        return jsonify(response), 404
    data = request.json
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    response = {'message': 'User updated successfully'}
    return jsonify(response), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> tuple:
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing the response JSON data and the HTTP status code.
    """
    user = User.query.get(user_id)
    if not user:
        response = {'message': 'User not found'}
        return jsonify(response), 404
    db.session.delete(user)
    db.session.commit()
    response = {'message': 'User deleted successfully'}
    return jsonify(response), 200

@app.route('/users', methods=['GET'])
def get_users() -> tuple:
    """
    Get a list of users.

    Returns:
        tuple: A tuple containing the response JSON data and the HTTP status code.
    """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', default=10))
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    result = []
    for user in users.items:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'registration_date': user.registration_date
        }
        result.append(user_data)
    return jsonify(result), 200

@app.route('/stats', methods=['GET'])
def get_user_stats() -> tuple:
    """
    Get user statistics.

    Returns:
        tuple: A tuple containing the response JSON data and the HTTP status code.
    """
    recent_users_count = count_recent_users()
    top_users = get_top_users()
    domain = 'example.com'
    email_domain_ratio = calculate_email_domain_ratio(domain)

    stats_data = {
        'recent_users_count': recent_users_count,
        'top_users': format_top_users(top_users),
        'email_domain_ratio': email_domain_ratio
    }

    return jsonify(stats_data), 200