from flask import Flask, render_template, request
from pymongo import MongoClient
from waitress import serve

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')  # 连接到MongoDB
db = client['grasscutter']
collection = db['players']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        accountId = request.form['accountId']
        new_nickname = request.form['new_nickname']
        update_nickname(accountId, new_nickname)
    return render_template('index.html')

def update_nickname(accountId, new_nickname):
    condition = {"_id": int(accountId)}
    existing_document = collection.find_one(condition)
    if existing_document:
        update = {"$set": {"nickname": new_nickname}}
        collection.update_one(condition, update)
    else:
        new_document = {"_id": int(accountId), "nickname": new_nickname}
        collection.insert_one(new_document)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=21472)