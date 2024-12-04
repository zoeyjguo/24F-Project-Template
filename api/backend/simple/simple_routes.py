from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
import json
from backend.db_connection import db

# This blueprint handles some basic routes that you can use for testing
# blueprint is a collection to route in flask
simple_routes = Blueprint('simple_routes', __name__)

# ------------------------------------------------------------
@simple_routes.route('/reports', methods=['GET'])
def get_reports():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Report')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@simple_routes.route('/locations', methods=['GET'])
def get_locations():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Latitude, Longitude FROM User')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@simple_routes.route('/interests', methods=['GET'])
def get_interests():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Interest')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@simple_routes.route('/interests/counts', methods=['GET'])
def get_interest_counts():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT InterestId, COUNT(DISTINCT UserId) FROM UserInterests GROUP BY InterestId')

    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


@simple_routes.route('/messages', methods=['GET'])
def get_user_interests():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Message')

    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@simple_routes.route('/flagreports', methods=['GET']) 
def get_flag_reports(): 
    cursor = db.get_db().cursor() 
    cursor.execute('SELECT * FROM Flag f JOIN User u ON f.flagger = u.UserId JOIN Message m ON f.MessageId = m.MessageId')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Delete flag
@simple_routes.route('/flagreports/<flagId>', methods = ['DELETE']) 
def delete_flag(flagId): 
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Flag WHERE FlagId = {0}'.format(flagId))
    db.get_db().commit()

    response = make_response("Successfully deleted report with flag id {0}".format(flagId))
    response.status_code = 200
    return response

@simple_routes.route('/badges', methods=['GET'])
def get_badges():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Badge')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@simple_routes.route('/groupchats', methods=['GET'])
def get_groupchats():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM GroupChat')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response