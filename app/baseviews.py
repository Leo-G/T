from flask import flash, redirect, url_for
# CRUD FUNCTIONS
# Arguments  are data to add, function to redirect to if the add was
# successful and if not


def add(data, success_url='', fail_url=''):
    add = data.add(data)
    # if does not return any error
    if not add:
        flash("Add was successful")
        return redirect(url_for(success_url))
    else:
        message = add
        flash(message)
        return redirect(url_for(fail_url))


def update(data, id, success_url='', fail_url=''):

    update = data.update()
    # if does not return any error
    if not update:
        flash("Update was successful")
        return redirect(url_for(success_url))
    else:
        message = update
        flash(message)
        return redirect(url_for(fail_url, id=id))


def delete(data, fail_url=''):
    delete = data.delete(data)
    if not delete:
        flash("Delete was successful")

    else:
        message = delete
        flash(message)
    return redirect(url_for(fail_url))
