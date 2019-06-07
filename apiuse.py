
from pymongo import MongoClient

client = MongoClient("mongodb+srv://test:test@cluster0-emyai.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('preference_db')

records = db.preference_records

def datadict(**data):
    return data

def upload(sess_id, recv, sent, fav =False):
    records.insert_one(datadict(session_id = sess_id,message_received = recv,message_sent = sent,favourite = fav))
    return
