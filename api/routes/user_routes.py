from flask import request, jsonify, session, redirect, url_for, render_template
from api.models.user_models import User
from api.app import app, login_required

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/account/')
@login_required
def account():
    return render_template('account.html')

@app.route('/user/signup/', methods=['POST'])
def signup():
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
        return jsonify({"message": "Connexion réussie", "user": user.user_data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/update/', methods=['POST'])
@login_required
def update():
    user = User(session.get('user'))
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user.update(name, email, password)
        session['user']['name'] = name
        if email:
            session['user']['email'] = email
        return jsonify({"message": "Mise à jour effectuée", "updated": user.user_data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/delete/', methods=['POST'])
@login_required
def delete_user():
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
    session.clear()
    return redirect(url_for('login'))
