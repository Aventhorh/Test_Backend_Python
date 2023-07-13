from services.UserService import app
from flask import request, jsonify
from models.User import  User, db
from flask_restx import Api, Resource, fields
from modules.calculate_email_domain_ratio import calculate_email_domain_ratio
from modules.count_recent_users import count_recent_users
from modules.format_top_users import format_top_users
from modules.get_top_users import get_top_users

api = Api(app)

user_model = api.model('User', {
    'username': fields.String(required=True, description='The username of the user'),
    'email': fields.String(required=True, description='The email of the user')
})

@api.route('/users')
class UsersResource(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User created successfully')
    def post(self):
        """
        Create a new user.
        """
        data = request.json
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        response = {'message': 'User created successfully'}
        return jsonify(response), 201

    @api.doc('get_users')
    @api.response(200, 'Success')
    def get(self):
        """
        Get a list of users.
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

@api.route('/users/<int:user_id>')
@api.param('user_id', 'The ID of the user')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get a user by ID.
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

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update a user by ID.
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

    @api.doc('delete_user')
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """
        Delete a user by ID.
        """
        user = User.query.get(user_id)
        if not user:
            response = {'message': 'User not found'}
            return jsonify(response), 404
        db.session.delete(user)
        db.session.commit()
        response = {'message': 'User deleted successfully'}
        return jsonify(response), 200

@api.route('/stats')
class StatsResource(Resource):
    @api.doc('get_user_stats')
    @api.response(200, 'Success')
    def get(self):
        """
        Get user statistics.
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
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=4000)
