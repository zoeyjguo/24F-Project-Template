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
# Create a new Blueprint object
flags = Blueprint('flags', __name__)

@flags.route('/flags/<post_id>', methods=['POST'])
def create_flag_post():

    query = '''
       INSERT INTO Flags (PostId)
       VALUES (%s, %s);
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
 
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get rank of a specific user in the system
@flag.route('/flags/<message_id>', methods=['POST'])
def create_flag_message(userId):
    
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO Flags (MessageId) VALUES (%s, %s)')
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

