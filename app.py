from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(70), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        note = Note(title=title, description=description)
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    
    notes = Note.query.all()
    return render_template('home.html', notes=notes)

@app.route('/delete/<int:sno>')
def delete(sno):
    note = Note.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

@app.route('/view/<int:sno>')
def view(sno):
    note = Note.query.filter_by(sno=sno).first()
    return render_template('view.html', note=note)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        note = Note.query.filter_by(sno=sno).first()
        note.title = title
        note.description = description
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    note = Note.query.filter_by(sno=sno).first()
    return render_template('update.html', note=note)

if __name__ == '__main__':
    app.run(debug=True, port=8000)