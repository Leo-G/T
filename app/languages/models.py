from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD


class Languages(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    language_code = db.Column(db.String(10), unique=True, nullable=False)
    language_name = db.Column(db.String(100), unique=True, nullable=False)
    dir = db.Column(db.String(10), default="ltr", nullable=False)

    def __init__(self,  language_code,  language_name,  dir ):
        self.language_code = language_code
        self.language_name = language_name
        self.dir = dir


class LanguagesSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    language_code = fields.String(validate=not_blank)
    language_name = fields.String(validate=not_blank)
    dir = fields.String(validate=not_blank)

    def get_top_level_links(self, data, many):
        if many:
            self_link = "/languages/"
        else:
            self_link = "/languages/{}".format(data['id'])
        return {'self': self_link}
   
    
    class Meta:
        type_ = 'languages'
