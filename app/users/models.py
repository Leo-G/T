from marshmallow import Schema, fields, validate
from app.basemodels import db, CRUD

# Relationships
translator_languages=db.Table('translator_languages',

                             db.Column('user_id', db.Integer,db.ForeignKey('users.id'), nullable=False),
                             db.Column('language_code',db.String(10), db.ForeignKey('languages.language_code'),nullable=False),
                             db.PrimaryKeyConstraint('user_id', 'language_code')
                             )

class UserLanguages():
    def __init__(self,user_id,language_code):
      self.user_id=user_id
      self.language_code=language_code


class Users(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, server_default="false", nullable=False)
    creation_time = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    modification_time = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False) 
    role =  db.Column(db.String(), db.ForeignKey('roles.name'))
    #many users to one  role    
    role_relation =  db.relationship('Roles', backref="users")
    #many users to many lang_codes
    language_codes = db.relationship('Languages', secondary='translator_languages', backref=db.backref('users', lazy='dynamic'))

    def __init__(self,  email,  password,  name, is_active, role):

        self.email = email
        self.password = password
        self.name = name
        self.is_active = is_active
        self.role = role
           
class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    email = fields.Email(validate=not_blank)
    password = fields.String(validate=not_blank)
    name = fields.String(validate=not_blank)
    is_active = fields.Boolean()
    role = fields.String(validate=not_blank)
    
     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}
   
    
    class Meta:
        type_ = 'users'
        #fields = ('id',  'email',  'name',  'is_active')
