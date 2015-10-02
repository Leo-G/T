import unittest
import os
import sys

# Add app path to module path
sys.path.append(os.path.dirname(os.path.realpath(__file__).rsplit('/', 2)[0]))
from app import create_app
from app.roles.models import Roles


app = create_app('config')


class TestRoles(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_read(self):
        self.app = app.test_client()
        rv = self.app.get('/roles/')
        assert "Roles" in rv.data.decode('utf-8')

    def test_01_add(self):
        rv = self.app.post('/roles/add', data=dict(

            name='test string',), follow_redirects=True)

        assert 'Add was successful' in rv.data.decode('utf-8')

    def test_02_Update(self):

        with app.app_context():
            id = Roles.query.first().id
            rv = self.app.post(
                '/roles/update/{}'.format(id), data=dict(
                    name='test string',), follow_redirects=True)
            assert 'Update was successful' in rv.data.decode('utf-8')

    def test_03_delete(self):
        with app.app_context():
            id = Roles.query.first().id
            rv = self.app.post(
                'roles/delete/{}'.format(id), follow_redirects=True)
            assert 'Delete was successful' in rv.data.decode('utf-8')

if __name__ == '__main__':
    unittest.main()
