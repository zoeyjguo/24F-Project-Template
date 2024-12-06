from flask import Blueprint
from flask import jsonify
from flask import make_response
from backend.db_connection import db

#------------------------------------------------------------
# New Blueprint object for events routes
events = Blueprint('events', __name__)

#------------------------------------------------------------
# Return all events in the database
@events.route('/events', methods=['GET'])
def get_events():
    
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Event')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete an event from the database
@events.route('/events/<eventId>', methods = ['DELETE'])
def delete_event(eventId):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Event WHERE EventId = {0}'.format(eventId))
    db.get_db().commit()
    
    response = make_response("Successfully deleted event {0}".format(eventId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Update the verified status of an event
@events.route('/events/<eventId>', methods = ['PUT'])
def add_user_interest(eventId):
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE Event SET IsVerified = TRUE WHERE EventId = {0})'.format(eventId))
    db.get_db().commit()
    
    response = make_response("Successfully verified event {0}".format(eventId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Return all detailed information about computer-generated events
@events.route('/events/generated', methods=['GET'])
def get_generated_events():
    
    cursor = db.get_db().cursor()
    query = '''SELECT e.Latitude, e.Longitude, e.StartTime, e.EndTime, e.PointsWorth, e.IsVerified
                FROM Event e
                JOIN Post p ON e.EventId = p.EventId
                WHERE p.CreatedBy IS NULL
            '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Return all events associated with an interest
@events.route('/events/interests/<interestId>', methods=['GET'])
def get_interest_events(interestId):
    
    cursor = db.get_db().cursor()
    query = f'''SELECT e.Latitude, e.Longitude, e.StartTime, e.EndTime, e.PointsWorth, e.IsVerified
                FROM Event e
                JOIN EventInterests ei ON e.EventId = ei.EventId
                WHERE ei.InterestId = {str(interestId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get the names of the participants of an event
@events.route('/events/<eventId>/participants', methods=['GET'])
def get_event_participants(eventId):
    
    cursor = db.get_db().cursor()
    query = f'''SELECT u.FirstName, u.LastName
                FROM GroupChatMembers gcm
                JOIN Event e ON gcm.EventId = e.EventId
                JOIN User u ON gcm.UserId = u.UserId
                WHERE e.EventId = {str(eventId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response