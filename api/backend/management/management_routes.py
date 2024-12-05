from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
import json
from backend.db_connection import db

# This blueprint handles some basic routes that you can use for testing
management = Blueprint('management', __name__)

#######################
#### APP FEEDBACK #####
#######################

#------------------------------------------------------------
# Get all information about all reports in the database
@management.route('/reports', methods=['GET'])
def get_reports():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.FirstName, u.LastName, r.Title, r.Description, r.TimeReported, r.ReportId FROM Report r JOIN User u ON u.UserId = r.Reporter')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all information about all flags in the database
@management.route('/flags', methods=['GET'])
def get_flags():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Flag')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get 10 most recent flags that haven't been reviewed yet
@management.route('/tenFlags', methods=['GET'])
def get_ten_flags():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT f.Title, f.FlagId, m.MessageId, m.Text 
                      FROM Flag f JOIN Message m ON f.MessageId = m.MessageId 
                      WHERE f.Reviewer IS NULL
                      ORDER BY f.FlagId ASC
                      LIMIT 10''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a flag associated with a post made by Chloe Lane, an admin
@management.route('/flags/<post_id>', methods=['POST'])
def create_flag_post(postId):
    flag_info = request.json
    current_app.logger.info(flag_info)

    title = flag_info['Title']
    description = flag_info['Description']
    
    query = f'''
        INSERT INTO Flag (PostId, Title, Description, Flagger)
        VALUES ({str(postId)}, '{title}', '{description}', '76')
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully created flag for post {0}".format(postId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Create a flag associated with a message made by Chloe Lane, an admin
@management.route('/flags/<message_id>', methods=['POST'])
def create_flag_message(messageId):
    flag_info = request.json
    current_app.logger.info(flag_info)

    title = flag_info['Title']
    description = flag_info['Description']
    
    query = f'''
        INSERT INTO Flag (MessageId, Title, Description, Flagger)
        VALUES ({str(messageId)}, '{title}', '{description}', '76')
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully created flag for post {0}".format(messageId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Update a flag so that it is reviewed by Chloe Lane, an admin
@management.route('flags/<flagId>', methods=['PUT'])
def update_flag(flagId):
    query = f'''
        UPDATE Flag
        SET Reviewer = 76
        WHERE FlagId = {str(flagId)}
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated flag with id: {0}".format(flagId))
    response.status_code = 200
    return response

#######################
#### APP USER DATA ####
#######################

#------------------------------------------------------------
# Get all information about all badges in the database
@management.route('/badges', methods=['GET'])
def get_badges():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Badge')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get the number of students who have each badge in the database
@management.route('/badges/counts', methods=['GET'])
def get_badge_counts():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT BadgeId, COUNT(DISTINCT UserId) AS NumStudents FROM UserBadges GROUP BY BadgeId')

    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all distinct user locations from the database
@management.route('/locations', methods=['GET'])
def get_locations():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT Latitude, Longitude FROM User GROUP BY Latitude, Longitude')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all interests from the database
@management.route('/interests', methods=['GET'])
def get_interests():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Interest')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get the number of students interested in each interest in the database
@management.route('/interests/counts', methods=['GET'])
def get_interest_counts():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT InterestId, COUNT(DISTINCT UserId) AS NumStudents FROM UserInterests GROUP BY InterestId')

    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all information about group chats monitored by a specific admin
@management.route('/admin/<adminId>/groupchats', methods=['GET'])
def get_admin_groupchats(adminId):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM GroupChat WHERE Monitor = {0}'.format(adminId))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all information about all messages in the database
@management.route('/messages', methods=['GET'])
def get_messages():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Message')

    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete a message from the database
@management.route('/messages/<messageId>', methods=['DELETE'])
def delete_message(messageId):
    query = f'''
        DELETE FROM Message
        WHERE MessageId = {str(messageId)}
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully deleted : {0}".format(messageId))
    response.status_code = 200
    return response

#---------
@management.route('/groupchatsInterest', methods=['GET'])
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

# TODO
@management.route('/post', methods = ['POST'])
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

@management.route('/postInterest/<interestId>', methods=['GET']) 
def get_post_interest(interestId): 
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT DISTINCT
            p.Title, p.CreatedBy, p.EventId, ei.InterestId, e.StartTime, e.EndTime, p.Description
            FROM Post p 
            JOIN Event e ON e.EventId = p.EventId
            JOIN EventInterests ei ON ei.EventId = p.EventId 
            WHERE ei.InterestId = %s
    ''', (interestId,))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@management.route('/reportInfo', methods=['GET'])
def get_reporters():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.FirstName, u.LastName, r.Description, r.TimeReported, r.Title, r.ReportId FROM Report r Join User u ON r.Reporter = u.UserId')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Delete report with ReportId reportId from database
@management.route('/report/<reportId>', methods = ['DELETE'])
def delete_report(reportId):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Report WHERE ReportId = {0}'.format(reportId))
    db.get_db().commit()
    
    response = make_response("Successfully deleted report")
    response.status_code = 200
    return response

@management.route('/postUser', methods=['GET']) 
def get_post_user(): 
    cursor = db.get_db().cursor()
    cursor.execute('SELECT FirstName, LastName, p.EventId FROM User u JOIN Post p ON p.CreatedBy = u.UserId')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response