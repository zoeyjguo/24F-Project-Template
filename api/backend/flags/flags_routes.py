from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create a new Blueprint object for flags
flags = Blueprint('flags', __name__)

#------------------------------------------------------------
# Return all flags
@flags.route('/flags', methods=['GET'])
def get_flags():
    
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Flag')
    theData = cursor.fetchall()
 
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Create a flag associated with a post made by Chloe Lane, an admin
@flags.route('/flags/<post_id>', methods=['POST'])
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
@flags.route('/flags/<message_id>', methods=['POST'])
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
@flags.route('flags/<flagId>', methods=['PUT'])
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