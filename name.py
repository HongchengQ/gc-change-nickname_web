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
        uid = int(request.form['uid'])
        new_nickname = (request.form['new_nickname'])
        update_nickname(uid, new_nickname)
    return render_template('index.html')

def update_nickname(uid, new_nickname):
    condition = {"_id": (uid)}#_id对应数据库中的_id 不可更改
    existing_document = collection.find_one(condition)
    if existing_document:
        update = {"$set": {"nickname": new_nickname}}
        collection.update_one(condition, update)
    else:
        return {"status": "error"}

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=21472)
