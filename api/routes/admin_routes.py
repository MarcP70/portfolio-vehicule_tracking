# admin_routes.py
from flask import request, jsonify, redirect, url_for, render_template
from api.models.user_models import (
    User,
    PasswordResetError,
    UserDeletionError,
    UserNotFoundError
)
from api.app import app, login_required, admin_required


@app.route('/admin/dashboard/')
@admin_required
def admin_dashboard():
    """
    Renders the 'admin_dashboard.html' template.

    Returns:
        The rendered 'admin_dashboard.html' template.
    """
    return render_template('admin_dashboard.html')


@app.route('/admin/reset_password/', methods=['PATCH'])
@admin_required
def admin_reset_password():
    """
    Resets the password of a user by an admin.

    :return: A JSON response with a success message if the password reset is
        successful, or an error message if it fails.
    :rtype: dict
    """
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    try:
        message = User.reset_password(user_id, new_password)
        return jsonify(message), 200
    except PasswordResetError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/admin/delete_user/', methods=['DELETE'])
@admin_required
def admin_delete_user():
    """
    Deletes a user from the system.

    :return: JSON response with a success message if the deletion is successful
        , or an error message if any exception occurs.
    :rtype: flask.Response
    """
    user_id = request.form.get('_id')
    try:
        message = User.delete(user_id)
        return jsonify(message), 200
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except UserDeletionError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/admin/users/', methods=['GET'])
@admin_required
def admin_users():
    """
    Retrieves all users with the role 'user' from the database and renders the
        'admin_dashboard.html' template.

    :return: None
    """
    users = User.get_all_users()
    return render_template('admin_dashboard.html', users=users)
