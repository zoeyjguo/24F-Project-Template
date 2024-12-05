from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

users = Blueprint('users', __name__)

#------------------------------------------------------------
# Return all information about all users in the database
@users.route('/users', methods=['GET'])
def get_users():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM User')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Return all information about a single user
@users.route('/users/<userId>', methods=['GET'])
def get_user(userId):
    
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM User WHERE UserId = {0}'.format(userId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete a user from the database
@users.route('/users/<userId>', methods = ['DELETE'])
def delete_user(userId):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM User WHERE UserId = {0}'.format(userId))
    db.get_db().commit()
    
    response = make_response("Successfully deleted user {0}".format(userId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Return the friends a user has
@users.route('/users/<userId>/friends', methods=['GET'])
def get_user_friends(userId):
    
    cursor = db.get_db().cursor()
    query = f'''SELECT uf.FirstName,
                       uf.LastName
                FROM User u
                JOIN Friend f ON u.UserId = f.UserId
                JOIN User uf ON uf.UserId = f.FriendId
                WHERE u.UserId = {str(userId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a friend to a particular user's friend list
@users.route('/users/<userId>/friends', methods = ['POST'])
def add_user_friend(userId):
    friend_info = request.json
    current_app.logger.info(friend_info)

    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Friend VALUES ({0}, {1}), ({1}, {0})'.format(friend_info['FriendId'], userId))
    db.get_db().commit()
    
    response = make_response("Successfully added friend to user {0}".format(userId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get the badges a user has acquired
@users.route('/users/<userId>/badges', methods=['GET'])
def get_user_badges(userId):
    
    cursor = db.get_db().cursor()
    query = f'''SELECT b.Name
                FROM Badge b
                JOIN UserBadges ub ON b.BadgeId = ub.BadgeId
                JOIN User u on ub.UserId = u.UserId
                WHERE u.UserId = {str(userId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get rank and points of a specific user in the system
@users.route('/users/<userId>/rank', methods=['GET'])
def get_user_rank(userId):
    
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Title, Points FROM User WHERE UserId = {0}'.format(userId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get events a specific user in the system is attending/has attended
@users.route('/users/<userId>/events', methods=['GET'])
def get_user_events(userId):

    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT DISTINCT p.Title, e.StartTime, e.EndTime
        FROM Post p JOIN Event e ON p.EventId = e.EventId
                    JOIN GroupChat gc ON p.GroupChatId = gc.GroupChatId
                    JOIN GroupChatMembers gcm ON gc.GroupChatId = gcm.GroupChatId
        WHERE gcm.UserId = {0}'''.format(userId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get posts a specific user in the system has made 
@users.route('/users/<userId>/posts', methods=['GET'])
def get_user_posts(userId):

    cursor = db.get_db().cursor()
    cursor.execute('SELECT Title FROM Post WHERE CreatedBy = {0}'.format(userId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get a user's interests
@users.route('/users/<userId>/interests', methods=['GET'])
def get_user_interests(userId):

    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT i.Name
        FROM User u
        JOIN UserInterests ui ON u.UserId = ui.UserId
        JOIN Interest i ON i.InterestId = ui.InterestId
        WHERE u.UserId = {0}'''.format(userId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add to the interests of a particular user
@users.route('/users/<userId>/interests', methods = ['POST'])
def add_user_interest(userId):
    interest_info = request.json
    current_app.logger.info(interest_info)

    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO UserInterests (UserId, InterestId) VALUES ({0}, {1})'.format(userId, interest_info['InterestId']))
    db.get_db().commit()
    
    response = make_response("Successfully added interest to user {0}".format(userId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Delete from the interests of a particular user
@users.route('/users/<userId>/interests', methods = ['DELETE'])
def delete_user_interest(userId):
    interest_info = request.json
    current_app.logger.info(interest_info)

    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM UserInterests WHERE UserId = {0} AND InterestId = {1}'.format(userId, interest_info['InterestId']))
    db.get_db().commit()
    
    response = make_response("Successfully deleted interest from user {0}".format(userId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Update the location of a particular user
@users.route('/users/<userId>/location', methods=['PUT'])
def update_user_location(userId):
    the_data = request.json
    current_app.logger.info(the_data)
    
    lat = the_data['Latitude']
    lon = the_data['Longitude']

    query = f'''
        UPDATE User
        SET Latitude = '{lat}', Longitude = '{lon}'
        WHERE UserId = {str(userId)}
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated location")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get a user's interests
@users.route('/users/<userId>/location', methods=['GET'])
def get_user_location(userId):

    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT Latitude, Longitude
        FROM User u
        WHERE u.UserId = {0}'''.format(userId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update the notification settings of a particular user
@users.route('/users/<userId>/notifications', methods=['PUT'])
def update_user_notifications(userId):
    the_data = request.json
    current_app.logger.info(the_data)

    query = f'''
        UPDATE User
        SET HasNotifs = '{the_data}'
        WHERE UserId = {str(userId)}
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated notification settings")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get a user's friend suggestions
@users.route('/users/<userId>/suggestions', methods=['GET'])
def get_user_suggestions(userId):
    
    cursor = db.get_db().cursor()
    query = f'''SELECT fu.FirstName, fu.LastName
                FROM User u
                JOIN FriendSuggestion fs ON u.UserId = fs.UserId
                JOIN User fu on fs.SuggestedUser = fu.UserId
                WHERE u.UserId = {str(userId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete from the friend suggestions of a particular user
@users.route('/users/<userId>/suggestions', methods = ['DELETE'])
def delete_user_suggestion(userId):
    suggestion_info = request.json
    current_app.logger.info(suggestion_info)

    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM FriendSuggestion WHERE UserId = {0} AND SuggestedUser = {1}'.format(userId, suggestion_info['FriendId']))
    db.get_db().commit()
    
    response = make_response("Successfully deleted friend suggestion from user {0}".format(userId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get group chats a specific user is a part of
@users.route('/users/<userId>/groupchats', methods=['GET'])
def get_user_groupchats(userId):

    cursor = db.get_db().cursor()
    query = f'''SELECT gc.Name, gc.GroupChatId
                FROM GroupChat gc
                JOIN GroupChatMembers gcm ON gc.GroupChatId = gcm.GroupChatId
                WHERE gcm.UserId = {str(userId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Remove a particular user from one of their group chats
@users.route('/users/<userId>/groupchats', methods = ['DELETE'])
def delete_user_groupchat(userId):
    groupchat_info = request.json
    current_app.logger.info(groupchat_info)

    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM GroupChatMembers WHERE UserId = {0} AND GroupChatId = {1}'.format(userId, groupchat_info['GroupChatId']))
    db.get_db().commit()
    
    response = make_response("Successfully deleted group chat {0}".format(groupchat_info['GroupChatId']))
    response.status_code = 200
    return response
#------------------------------------------------------------
