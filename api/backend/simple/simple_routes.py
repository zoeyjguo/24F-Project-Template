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

    
@simple_routes.route('groupchatsInterest', methods=['GET'])
def get_groupchats_interest():
    # Fetching the event IDs from the request's query parameter (e.g., EventIds=1,2,3)
    event_ids = request.args.get('EventId')
    
    if not event_ids:
        return jsonify({"error": "No event IDs provided"}), 400
    
    # Convert the event IDs to a list of integers
    event_ids = [int(id.strip()) for id in event_ids.split(',')]
    
    # Prepare the query using parameterized queries to prevent SQL injection
    query = '''
        SELECT i.Name
        FROM Interest i
        JOIN EventInterests ei ON ei.InterestId = i.InterestId
        WHERE ei.EventId IN ({})
    '''.format(','.join(['?'] * len(event_ids)))
    
    # Get database connection and cursor
    cursor = db.get_db().cursor()
    
    # Execute the query with event_ids as parameters
    cursor.execute(query, event_ids)
    
    # Fetch the data
    the_data = cursor.fetchall()
    
    # Check if data exists, otherwise return a message
    if not the_data:
        return jsonify({"message": "No interests found for the given events"}), 404
    
    # Prepare the response
    return jsonify(the_data), 200

#TODO
@simple_routes.route('/post', methods = ['POST'])
def add_user_friend(userId):
    event_info = request.json
    current_app.logger.info(event_info)

    # Get data from the request
    title = event_info.get('title')
    date = event_info.get('date')
    time = event_info.get('time')
    description = event_info.get('description')

    if not title or not date or not time or not description:
        response = make_response(
            "Missing required fields: title, date, time, and description are all required.",
            400
        )
        return response
    

    cursor = db.get_db().cursor()
    cursor.execute(
        '''
        INSERT INTO Event (title, date, time, description) 
        VALUES (%s, %s, %s, %s)
        ''',(title, date, time, description))
    db.get_db().commit()
    
    response = make_response("Successfully added post")
    response.status_code = 200
    return response



@simple_routes.route('postInterest', methods=['GET']) 
def get_post_interest(): 
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT DISTINCT
            u.FirstName AS CreatedByFirstName,
            u.LastName AS CreatedByLastName,
            Description, 
            EndTime, 
            g.Name AS GroupChatName, 
            StartTime, 
            e.EventId, 
            e.Latitude, 
            e.Longitude, 
            i.Name AS Interest, 
            p.Title AS PostTitle
        FROM 
            User u 
        JOIN 
            GroupChatMembers gcm ON gcm.UserId = u.UserId 
        JOIN 
            GroupChat g ON g.GroupChatId = gcm.GroupChatId 
        JOIN 
            Post p ON g.EventId = p.EventId 
        JOIN 
            Event e ON e.EventId = p.EventId 
        JOIN 
            EventInterests ei ON ei.EventId = p.EventId 
        JOIN 
            Interest i ON i.InterestId = ei.InterestId 
        JOIN 
            User u_first ON u_first.UserId = p.CreatedBy  -- Join User table again for the CreatedBy field
        JOIN 
            User u_last ON u_last.UserId = p.CreatedBy   -- Join User table for the last name
        WHERE 
            u.UserId = 1001
    ''')
    
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