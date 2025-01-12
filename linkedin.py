from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/leads_db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do Lead
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Lead {self.name}>"

# Rota para página inicial (listar leads)
@app.route('/')
def index():
    leads = Lead.query.all()
    return render_template('index.html', leads=leads)

# Rota para adicionar leads manualmente (opcional)
@app.route('/add', methods=['GET', 'POST'])
def add_lead():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        company = request.form['company']
        email = request.form['email']

        new_lead = Lead(name=name, position=position, company=company, email=email)
        db.session.add(new_lead)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_lead.html')

# Inicializar o banco de dados
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)