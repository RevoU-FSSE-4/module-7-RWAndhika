from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.review import Review

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from decorators.role_checker import role_required
from cerberus import Validator
from validations.review_insert import review_insert_schema

from flask_login import current_user

review_routes = Blueprint("review_routes", __name__)

@review_routes.route("/review", methods=["GET"])
@role_required('Admin')
def review_home():

    Session = sessionmaker(connection)
    s = Session()

    try:
        review_query = select(Review)
        result = s.execute(review_query)
        reviews = []
        for row in result.scalars():
            reviews.append({
                'id': row.id,
                'email': row.email,
                'rating': row.rating,
                'description': row.description,
                'created_at': row.created_at
            })
        
        return {'reviews': reviews}, 200 
    
    except Exception as e:
        return {'message': 'Unexpected Error'}, 500

@review_routes.route("/review", methods=["POST"])
@role_required('Admin')
def review_insert():

    v = Validator(review_insert_schema)
    request_body = {
        'rating': int(request.form['rating']),
        'description': request.form['description']
    }

    if not v.validate(request_body):
        return {'error': v.errors}, 409

    Session = sessionmaker(connection)
    s = Session()
    s.begin()

    try:
        NewReview = Review(
            email = current_user.email,
            rating = request.form['rating'],
            description = request.form['description']
        )
        s.add(NewReview)
        s.commit()
    
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to Insert'}, 500
    
    return {'message': 'Success insert review data'}, 200 