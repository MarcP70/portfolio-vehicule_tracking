# admin_routes.py
from flask import request, jsonify, redirect, url_for, render_template
from api.models.user_models import User, PasswordResetError, UserDeletionError, UserNotFoundError
from api.app import app, login_required, admin_required

@app.route('/admin/dashboard/')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/admin/reset_password/', methods=['PATCH'])
@admin_required
def admin_reset_password():
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
    users = User.get_all_users()
    return render_template('admin_dashboard.html', users=users)
