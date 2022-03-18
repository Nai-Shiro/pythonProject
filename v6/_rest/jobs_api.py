import datetime

from flask_restful import Resource, abort, reqparse
from flask import jsonify

from v6.data import db_session
from v6.data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('work_size', type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True)
parser.add_argument('end_date', required=True)
parser.add_argument('is_finished', type=bool, required=True)
parser.add_argument('team_leader', type=int, required=True)


def abort_if_not_id(id):
    db_sess = db_session.create_session()
    if not db_sess.query(Jobs).get(id):
        abort(404, message=f"Задача с id равным {id} отсутсвует")



class JobListRes(Resource):
    def get(self):
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs':
                    [item.to_dict(
                        only=('id', 'job', 'team_leader', 'work_size', "collaborators", 'start_date', 'end_date',
                              'is_finished'))
                     for item in jobs]
            }
        )

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        job = Jobs(job=args['job'],
                   work_size=args['work_size'],
                   collaboratos=args['collaborators'],
                   start_date=datetime.datetime.strptime(args['start_date'], format='%d%m%y'),
                   end_date=datetime.datetime.strptime(args['end_date'], format='%d%m%y'),
                   is_finished=args['is_finished'],
                   team_leader=args['team_leader'])
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'key': 'success'})


class JobRes(Resource):
    def get(self, job_id):
        abort_if_not_id(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        return jsonify(
                {
                    'jobs':
                        job.to_dict(
                            only=('id', 'job', 'team_leader', 'work_size', "collaborators", 'start_date', 'end_date',
                                  'is_finished'))
                }
            )

    def delete(self, job_id):
        abort_if_not_id(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({'key': 'success'})

