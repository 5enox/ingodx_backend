from .extensions import api
from flask_restx import fields


course_model = api.model('Course', {
    'id': fields.Integer,
    'name': fields.String,

})


student_model = api.model('Student', {
    'id': fields.Integer,
    'name': fields.String,

})
