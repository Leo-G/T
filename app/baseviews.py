# Token Auth functions
import jwt
from jwt import DecodeError, ExpiredSignature
from config import SECRET_KEY
from datetime import datetime, timedelta
from functools import wraps
from flask import g, Blueprint, jsonify, make_response, request
from flask_restful import Resource, Api
import flask_restful
from app.users.models import Users
from werkzeug.security import check_password_hash

login = Blueprint('login', __name__)
api = Api(login)

# JWT AUTh process start
def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1),
        'scope': user.role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

# Login decorator function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            #print(request.headers.get('Authorization'))
            payload = parse_token(request)
            if payload['scope'] != "admin":
                response = jsonify(error='Admin Access Required')
                response.status_code = 401
                return response
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function




# JWT AUTh process end

class Auth(Resource):

    def post(self):
        raw_dict = request.get_json(force=True)
        data = raw_dict['data']['attributes']
        email = data['email']
        password = data['password']
        user = Users.query.filter_by(email=email).first()
        if user == None:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response
        if check_password_hash(user.password, password):

            token = create_token(user)
            return {'token': token}
        else:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response

api.add_resource(Auth, '/')


# Adding the login decorator to the Resource class
#class Resource(flask_restful.Resource):
#    method_decorators = [login_required]
    
class Resource(flask_restful.Resource):
    method_decorators = [admin_login_required]    

