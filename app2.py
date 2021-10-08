from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app2)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id

@app2.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template('home.html')

    return render_template('home.html')

if __name__ == "__main__":
    app2.run(debug = True)