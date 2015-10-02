#resource, resources, Resources
from flask import Blueprint, request, jsonify, make_response
from app.languages.models import Languages, LanguagesSchema
from flask_restful import Resource, Api
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from marshmallow import ValidationError

languages = Blueprint('languages', __name__)
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = LanguagesSchema()
api = Api(languages)
# Languages

class LanguagesList(Resource):
   
    def get(self):
        languages_query = Languages.query.all()
        results = schema.dump(languages_query, many=True).data
        return results
       
    def post(self):
        raw_dict = request.get_json(force=True)
        language_dict = raw_dict['data']['attributes']
        try:
                schema.validate(language_dict) 
                language = Languages(language_dict['language_code'], language_dict['language_name'], language_dict['dir'])                
                language.add(language)
                query = Languages.query.get(language.id)
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

   


class LanguagesUpdate(Resource):    
   
    
    def get(self, id):
        language_query = Languages.query.get_or_404(id)
        result = schema.dump(language_query).data
        return result       
    
    
    def patch(self, id):
        language = Languages.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        language_dict = raw_dict['data']['attributes']
        try:
            for key, value in language_dict.items():
                schema.validate({key:value})
                setattr(language, key, value)          
            language.update()            
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
        language = Languages.query.get_or_404(id)
        try:
            delete = language.delete(language)
            response = make_response()
            response.status_code = 204
            return response
            
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        

api.add_resource(LanguagesList, '/')
api.add_resource(LanguagesUpdate, '/<int:id>')

