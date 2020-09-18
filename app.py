from flask import Flask, render_template, redirect 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # armazena a referência de flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db" # configura o nome da base de dados
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # desativa o envio de sinais de mofidicações

db = SQLAlchemy(app) # armazena a referência de sqlalchemy


# criação de tabela
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __str__(self):
        return self.name

# melhorar inserção no bd
class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def __str__(self):  # Imprimir a tabela como string
        return self.name

# cria rota para requisição http
@app.route("/")
def index():
    users = User.query.all() # Select * from users; 
    return render_template("users.html", users=users) # renderiza o template de users

@app.route("/users/<int:id>")
def unique(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)

@app.route("/users/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__": # verifica a condição para rodar o app no modo debug
    app.run(debug=True)