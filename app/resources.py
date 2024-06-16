from turtle import st
from flask_restx import Namespace, Resource
from .api_models import course_model, student_model
from .models import Course, Student

ns = Namespace('api', description='Resource API')


@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'restx'}


@ns.route('/courses')
class CourseAPI(Resource):
    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()


@ns.route('/students')
class StudentAPI(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()
