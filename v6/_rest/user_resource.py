from flask_restful import Resource, abort, reqparse
from flask import jsonify

from v6.data import db_session
from v6.data.users import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)




def abort_if_not_id(id):
    db_sess = db_session.create_session()
    if not db_sess.query(User).get(id):
        abort(404, message=f"Человек с id равным {id} отсутсвует")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_not_id(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify(
            {
                'user':
                    user.to_dict(
                        only=('id', 'name', 'position', 'email'))
            }
        )

    def delete(self, user_id):
        abort_if_not_id(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'key': 'success'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(
                        only=('id', 'name'))
                        for item in users]
            }
        )

    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        user = User(name=args['name'],
                    surname=args['surname'],
                    age=args['age'],
                    position=args['position'],
                    speciality=args['speciality'],
                    address=args['address'],
                    email=args['email'])
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'key': 'success'})