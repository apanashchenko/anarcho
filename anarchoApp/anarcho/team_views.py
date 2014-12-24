from anarcho import app, db
from anarcho.serializer import serialize, PermissionSerializer
from anarcho.models.user import User
from anarcho.models.user_app import UserApp
from anarcho.access_manager import app_permissions, login_required
from flask import request, make_response
from flask.ext.cors import cross_origin


@app.route('/api/permission/<app_key>', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
@app_permissions(permissions=["w"])
def users_list(app_key=None):
    user_apps = UserApp.query.filter(UserApp.app_key == app_key, UserApp.permission != 'u').all()
    return serialize(user_apps, serializer=PermissionSerializer)


@app.route('/api/permission', methods=['POST', 'PATCH', 'DELETE'])
@cross_origin(headers=['x-auth-token', 'Content-Type'], methods=['POST', 'PATCH', 'DELETE'])
@login_required
@app_permissions(permissions=["w"])
def revoke_team_membership():
    if request.method == 'POST':
        result = add_user()
    if request.method == 'PATCH':
        result = update_user()
    if request.method == 'DELETE':
        result = remove_permission()
    return result


def remove_permission():
    app_key = request.json['app_key']
    email = request.json['email']
    user_app = UserApp.query.filter_by(app_key=app_key, email=email).first()
    db.session.delete(user_app)
    db.session.commit()
    return serialize(user_app, PermissionSerializer)


def update_user():
    app_key = request.json['app_key']
    email = request.json['email']
    permission = request.json['permission']
    user_app = UserApp.query.filter_by(app_key=app_key, email=email).first()
    if user_app is None:
        return make_response('{"error":"user_app_not_found}', 404)
    user_app.permission = permission
    db.session.commit()
    return serialize(user_app, PermissionSerializer)


def add_user():
    app_key = request.json['app_key']
    email = request.json['email']
    permission = request.json['permission']

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email)
        db.session.add(user)
        db.session.commit()
    user_app = UserApp(user.id, app_key, permission)
    user_app.user = user
    db.session.add(user_app)
    db.session.commit()
    return serialize(user_app, PermissionSerializer)