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

@simple_routes.route('/admin/<adminId>/groupchats', methods=['GET'])
def get_admin_groupchats(adminId):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM GroupChat WHERE Monitor = {0}'.format(adminId))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

    

@simple_routes.route('postInterest', methods=['GET']) 
def get_post_interest(): 
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT CreatedBy, Description, EndTime, g.Name as GroupChatName, StartTime, e.EventId, e.Latitude, e.Longitude, i.Name AS Interest, p.Title as PostTitle  FROM User u JOIN GroupChatMembers gcm ON gcm.UserId = u.UserId JOIN GroupChat g ON g.GroupChatId = gcm.GroupChatId JOIN Post p ON g.EventId = p.EventId JOIN Event e ON e.EventId = p.EventId JOIN EventInterests ei ON ei.EventId = p.EventId JOIN Interest i ON i.InterestId = ei.InterestId WHERE u.UserId = 1001')
    #cursor.execute('SELECT Description, EndTime, ei.EventId, p.GroupChatId, i.Name, StartTime, p.Title, g.Name, u.FirstName, u.LastName FROM EventInterests ei JOIN Post p ON ei.EventId = p.EventId JOIN Interest i ON i.InterestId = ei.PostId JOIN Event e ON p.EventId = e.EventId JOIN GroupChat g ON g.EventId = p.EventId JOIN User u ON p.CreatedBy = u.UserId WHERE u.UserId = 1001')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@simple_routes.route('/reportInfo', methods=['GET'])
def get_reporters():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.FirstName, u.LastName, r.Description, r.TimeReported, r.Title, r.ReportId FROM Report r Join User u ON r.Reporter = u.UserId')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Delete report with ReportId reportId from database
@simple_routes.route('/report/<reportId>', methods = ['DELETE'])
def delete_report(reportId):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Report WHERE ReportId = {0}'.format(reportId))
    db.get_db().commit()
    
    response = make_response("Successfully deleted report")
    response.status_code = 200
    return response

@simple_routes.route('postUser', methods=['GET']) 
def get_post_user(): 
    cursor = db.get_db().cursor()
    cursor.execute('SELECT FirstName, LastName, p.EventId FROM User u JOIN Post p ON p.CreatedBy = u.UserId')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response