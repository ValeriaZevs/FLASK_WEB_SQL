from flask import jsonify
from data import db_session
from data.jobs import Jobs
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template, redirect, request
from data.users_parser import *

app = Flask(__name__)
api = Api(app)


def abort_if_news_not_found(jobs_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        abort(404, message=f"Job {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_news_not_found(jobs_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': job.to_dict(only=('id', 'job', 'work_size', 'collaborators', 'content',
                                           'start_date', 'end_date',
                                           'is_finished', 'team_leader'))})

    def delete(self, jobs_id):
        abort_if_news_not_found(jobs_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(jobs_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'job', 'work_size', 'collaborators', 'content',
                                           'start_date', 'end_date',
                                           'is_finished', 'team_leader')) for item in job]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            id=args['id'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            content=args['content'],
            is_finished=args['is_finished'],
            team_leader=args['team_leader'])
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})








