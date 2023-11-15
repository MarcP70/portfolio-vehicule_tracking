from flask import request, jsonify, session, redirect, url_for, render_template
from api.models.user_models import User
from api.app import app, login_required


@app.route('/register/')
def register():
    """
    Renders the 'register.html' template.

    Returns:
        str: The rendered 'register.html' template.
    """
    return render_template('register.html')


@app.route('/login/')
def login():
    """
    Renders the 'login.html' template.

    Returns:
        The rendered 'login.html' template as a response to the GET request.
    """
    return render_template('login.html')


@app.route('/account/')
@login_required
def account():
    """
    Renders the 'account.html' template.

    Returns:
        The rendered 'account.html' template as a response.
    """
    return render_template('account.html')


@app.route('/user/signup/', methods=['POST'])
def signup():
    """
    Handles the signup process for new users.

    Inputs:
    - email (string): The email address of the user.
    - name (string): The name of the user.
    - password (string): The password of the user.

    Outputs:
    - If successful, returns the user data as a JSON response with a status
        code of 201.
    - If the email address is invalid or already used by another user,
        returns an error message with a status code of 400.
    - If any other error occurs during the signup process,
        returns an error message with a status code of 500.
    """

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    try:
        user = User.create(email, name, password)
        session['logged_in'] = True
        session['user'] = {
            '_id': str(user.user_id),
            'name': user.user_data['name'],
            'email': user.user_data['email'],
            'role': user.user_data.get('role', 'user')
        }
        return jsonify(user.user_data), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user/login/', methods=['POST'])
def user_login():
    """
    Handles the login functionality for a user.

    Args:
        None

    Returns:
        If authentication is successful, returns a success message with the
            user data as a JSON response.
        If authentication fails due to an incorrect email or password,
            returns an error message as a JSON response.
        If any other exception occurs, returns an error message as a
            JSON response.
    """

    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = User.login(email, password)
        session['logged_in'] = True
        session['user'] = {
            '_id': str(user.user_id),
            'name': user.user_data['name'],
            'email': user.user_data['email'],
            'role': user.user_data.get('role', 'user')
        }
        return jsonify({"message": "Connexion réussie",
                       "user": user.user_data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user/update/', methods=['POST'])
@login_required
def update():
    """
    Update the name, email, and password of a user in the system.

    :return: JSON response with success message and updated user data if update
                is successful.
             JSON response with error message and appropriate status code if
                update fails.
    """
    user = User(session.get('user'))
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user.update(name, email, password)
        session['user']['name'] = name
        if email:
            session['user']['email'] = email
        return jsonify({"message": "Mise à jour effectuée",
                       "updated": user.user_data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user/delete/', methods=['POST'])
@login_required
def delete_user():
    """
    Deletes a user and all associated data from the system.

    Returns:
        A JSON response with a success message and status code 200 if the user
            deletion was successful.
        A JSON response with an error message and appropriate status code if
            the user deletion fails.
    """
    user_id = session['user']['_id']
    try:
        result = User.delete(user_id)
        session.clear()
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user/signout/')
@login_required
def signout():
    """
    Clears the session and redirects the user to the login page.

    Returns:
        None
    """
    session.clear()
    return redirect(url_for('login'))
