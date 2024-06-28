from flask import Blueprint, request

from connectors.mysql_connector import connection
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models.user import User

from flask_login import login_user, logout_user, login_required


user_routes = Blueprint("user_routes", __name__)

@user_routes.route('/register', methods=['POST'])
def register_user():
    Session = sessionmaker(connection)
    s = Session()

    s.begin()
    try:
        NewUser = User(
            username = request.form['username'],
            email = request.form['email'],
            role = request.form['role']
        )
        
        NewUser.set_password(request.form['password'])

        s.add(NewUser)
        s.commit()
    except Exception as e:
        s.rollback()
        return { "message": "Fail to Register"}, 500
    
    return { "message": "Register Success" }, 200

@user_routes.route('/login', methods=['GET'])
def user_list():
    Session = sessionmaker(connection)
    s = Session()

    try:
        user_query = select(User)

        search_keyword = request.args.get('query')
        if search_keyword != None:
            user_query = user_query.where(User.username.like(f"%{search_keyword}%"))

        result = s.execute(user_query)
        Users = []
        for row in result.scalars():
            Users.append({
                'id': row.id,
                'email': row.email,
                'username': row.username,
                'created_at': row.created_at,
                'role': row.role
            })
        
        return {'users': Users}, 200

    except Exception as e:
        s.rollback()
        return {'message': 'Get User list Failed'}, 500

@user_routes.route('/login', methods=['POST'])
def user_login():
    Session = sessionmaker(connection)
    s = Session()

    s.begin()

    try:
        email = request.form['email']
        user = s.query(User).filter(User.email == email).first()

        if user == None:
            return {'message': 'User not found'}, 403
        
        if not user.check_password(request.form['password']):
            return {'message': 'Invalid password'}, 403
        
        login_user(user)
        session_id = request.cookies.get('session')

        return {
            'session_id': session_id,
            'message': 'Login Success'
        }, 200

    except Exception as e:
        s.rollback()
        return {'message': 'Login Failed'}, 500
    
@user_routes.route('/logout', methods=['GET'])
@login_required
def user_logout():
    logout_user()
    return {'message': "Success logout"}