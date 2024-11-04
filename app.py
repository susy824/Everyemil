from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Email {self.address}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    emails = Email.query.all()
    return render_template('index.html', emails=emails)

@app.route('/send', methods=['POST'])
def send_email():
    email_address = request.form.get('email')
    content = request.form.get('content')
    new_email = Email(address=email_address, content=content)
    db.session.add(new_email)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)