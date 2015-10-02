from marshmallow import Schema, fields, validate
from app.basemodels import db, CRUD


class {Resources}(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    {db_rows}

    def __init__(self, {init_args}):
        {init_self_vars}


class {Resources}Schema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    {schema}

    class Meta:
        fields = ('id', {meta})
