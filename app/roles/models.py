from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD


class Roles(db.Model, CRUD):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self,  name):
        self.name = name


class RolesSchema(Schema):

    not_blank = validate.Length(min=2, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=not_blank)

    def get_top_level_links(self, data, many):
        if many:
            self_link = "/roles/"
        else:
            self_link = "/roles/{}".format(data['id'])
        return {'self': self_link}
   
    
    class Meta:
        type_ = 'roles'
