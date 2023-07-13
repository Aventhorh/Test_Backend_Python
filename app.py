from flask import Flask, request, jsonify
from User import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=4000)
