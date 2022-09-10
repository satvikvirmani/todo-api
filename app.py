from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    unique_key = db.Column(db.String(16), nullable=False)
    todo = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(200), default='Unknown')
    event_date = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Todo: {self.todo}, Author: {self.author}, Event Date: {self.event_date}, Date Created: {self.date_created}"

    def return_json(self) -> json:
        return {
            "todo": self.todo,
            "author": self.author,
            "event_date": self.event_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "date_created": self.date_created.strftime("%m/%d/%Y, %H:%M:%S")
        }


@app.route('/')
def index():
    return jsonify({
        "message": "Todo API"
    })


@app.route('/post', methods=['POST'])
def post():
    body = request.get_json()
    unique_key = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=16))
    todo = ToDo(unique_key=unique_key,
                todo=body['todo'], author=body['author'])
    db.session.add(todo)
    db.session.commit()
    return "ToDo created successfully"


@app.route('/get', methods=['GET'])
def get():
    body = request.get_json()
    this_todo = ToDo.query.filter_by(unique_key=body['unique_key']).first()
    return this_todo.todo


@app.route('/patch', methods=['PATCH'])
def update():
    body = request.get_json()
    this_todo = ToDo.query.filter_by(unique_key=body['unique_key']).first()
    if this_todo:
        db.session.delete(this_todo)
        db.session.commit()
        updated_todo = ToDo(unique_key=body['unique_key'],
                            todo=body['todo'] if 'todo' in body else this_todo.todo,
                            author=body['author'] if 'author' in body else this_todo.author,
                            event_date=body['event_date'] if 'event_date' in body else this_todo.event_date)
        db.session.add(updated_todo)
        db.session.commit()
    return "ToDo patched successfully"


@app.route('/delete', methods=['Delete'])
def delete():
    body = request.get_json()
    this_todo = ToDo.query.get(body['unique_key'])
    db.session.delete(this_todo)
    db.session.commit()
    return "ToDo delete successfully"


if __name__ == '__main__':
    app.run(debug=False)