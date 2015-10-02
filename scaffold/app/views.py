#resource, resources, Resources
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.{resources}.models import {Resources}, {Resources}Schema
from app.baseviews import add, update, delete

{resources} = Blueprint('{resources}', __name__, template_folder='templates')
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = {Resources}Schema()

#{Resources}


@{resources}.route('/')
def {resource}_index():
    {resources} = {Resources}.query.all()
    results = schema.dump({resources}, many=True).data
    return render_template('/{resources}/index.html', results=results)


@{resources}.route('/add', methods=['POST', 'GET'])
def {resource}_add():
    if request.method == 'POST':
        # Validate form values by de-serializing the request,
        # http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
            {resource} = {Resources}({add_fields})
            return add({resource}, success_url='{resources}.{resource}_index', fail_url='{resources}.{resource}_add')
        else:
            flash(form_errors)

    return render_template('/{resources}/add.html')


@{resources}.route('/update/<int:id>', methods=['POST', 'GET'])
def {resource}_update(id):
    # Get {resource} by primary key:
    {resource} = {Resources}.query.get_or_404(id)
    if request.method == 'POST':
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
            {update_fields}
            return update({resource}, id, success_url='{resources}.{resource}_index', fail_url='{resources}.{resource}_update')
        else:
            flash(form_errors)

    return render_template('/{resources}/update.html', {resource}={resource})


@{resources}.route('/delete/<int:id>', methods=['POST', 'GET'])
def {resource}_delete(id):
    {resource} = {Resources}.query.get_or_404(id)
    return delete({resource}, fail_url='{resources}.{resource}_index')
