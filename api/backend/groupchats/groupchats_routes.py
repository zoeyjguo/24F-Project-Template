from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
groupchats = Blueprint('groupchats', __name__)

#------------------------------------------------------------
# Delete a particular groupchat from the database
@groupchats.route('/groupchats/<groupchatId>', methods=['DELETE'])
def delete_groupchat(groupchatId):
    query = 'DELETE FROM GroupChat WHERE GroupChatId = {0}'.format(groupchatId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()

    response = make_response("Successfully deleted groupchat with id: {0}".format(groupchatId))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add a message to a particular groupchat
@groupchats.route('/groupchats/<groupchatId>/messages', methods=['POST'])
def create_message(groupchatId):
    the_data = request.json
    sender = the_data['Sender']
    text = the_data['Text']
    image_link = the_data['ImageLink']

    query = 'INSERT INTO Message (Sender, GroupChatId, EventId, Text, ImageLink) VALUES (%s, %s, %s, %s, %s)'
    data = (sender, groupchatId, groupchatId, text, image_link)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()

    response = make_response("Successfully created message with text: {0}".format(text))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add a user to a particular groupchat
@groupchats.route('/groupchats/<groupchatId>/members', methods=['POST'])
def add_member(groupchatId):
    userId = request.json['UserId']
    query = 'INSERT INTO GroupChatMembers (GroupChatId, UserId) VALUES (%s, %s)'
    data = (groupchatId, userId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()

    response = make_response("Successfully added user with id: {0} to groupchat with id: {1}".format(userId, groupchatId))
    response.status_code = 200
    return response

@groupchats.route('/groupchats/<groupchatId>/messages', methods=['GET'])
def get_groupchat_messages(groupchatId):
    
    cursor = db.get_db().cursor()
    query = f'''SELECT u.FirstName, u.LastName, m.Text, m.ImageLink
                FROM Message m
                JOIN GroupChat gc ON m.GroupChatId = gc.GroupChatId
                JOIN User u ON m.Sender = u.UserId
                WHERE gc.GroupChatId = {str(groupchatId)}
    '''
    cursor.execute(query)
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response