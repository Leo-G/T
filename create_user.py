from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.users.models import Users, db
from app.roles.models import Roles

app = create_app('config')

name='Leo'
email='ryan@leog.in'
password=generate_password_hash('password')
is_active=True
admin_role_name=["admin", "support", "translator"]
role="support"


def db_commit():
    try:
          db.session.commit()
          print("{} was added successfully".format(email))
          return True
    except SQLAlchemyError as e:
          reason=str(e)
          print (reason)
          return False

with app.app_context():
    
        user=Users(email,  password,  name, is_active, role)
        db.session.add(user)
        db_commit()