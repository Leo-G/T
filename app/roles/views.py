#resource, resources, Resources
from flask import Blueprint, request, jsonify, make_response
from app.roles.models import Roles, RolesSchema
from flask_restful import Resource, Api
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from marshmallow import ValidationError

roles = Blueprint('roles', __name__, template_folder='templates')
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = RolesSchema(strict=True)
api = Api(roles)

# Roles

class RolesList(Resource):
   
    def get(self):
        roles_query = Roles.query.all()
        results = schema.dump(roles_query, many=True).data
        return results
       
    def post(self):
        raw_dict = request.get_json(force=True)
        role_dict = raw_dict['data']['attributes']
        try:
                schema.validate(role_dict)
                role = Roles(role_dict['name'])
                
                role.add(role)
                query = Roles.query.get(role.id)
                results = schema.dump(query).data                
                return results, 201
            
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 403
                return resp               
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 403
                return resp

   


class RolesUpdate(Resource):    
   
    
    def get(self, id):
        role_query = Roles.query.get_or_404(id)
        result = schema.dump(role_query).data
        return result       
    
    
    def patch(self, id):
        role = Roles.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        role_dict = raw_dict['data']['attributes']
        try:
            for key, value in role_dict.items():
                schema.validate({key:value})
                setattr(role, key, value)          
            role.update()            
            return self.get(id)
            
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp               
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        
        
         
    #http://jsonapi.org/format/#crud-deleting
    #A server MUST return a 204 No Content status code if a deletion request is successful and no content is returned.
    def delete(self, id):
        role = Roles.query.get_or_404(id)
        try:
            delete = role.delete(role)
            response = make_response()
            response.status_code = 204
            return response
            
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        

api.add_resource(RolesList, '/')
api.add_resource(RolesUpdate, '/<int:id>')