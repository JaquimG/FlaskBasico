from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user  # Usermixin já implementa os métodos necessários em user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # armazena a referência de flask
app.config["SECRET_KEY"] = 'secret'  # configura chave para poder usar autenticação
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db" # configura o nome da base de dados
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # desativa o envio de sinais de mofidicações

db = SQLAlchemy(app) # armazena a referência de sqlalchemy
login_manager = LoginManager(app) # armazena a referência de LoginManager


@login_manager.user_loader
def current_user(user_id):
    
    return User.query.get(user_id)


# criação de tabela
class User(db.Model, UserMixin):
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


    def __str__(self):  # Imprime a tabela como string
        return self.name

# cria rota para requisição http
@app.route("/")
def index():
    users = User.query.all() # Select * from users; 
    return render_template("users.html", users=users) # renderiza o template de users

@app.route("/users/<int:id>")
@login_required  # decorator para garantir visibilidade através do login
def unique(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)

@app.route("/users/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User()
        user.name = request.form["name"]
        user.email = request.form["email"]
        user.password = generate_password_hash(request.form["password"]) # gera uma criptografia da senha
 
        db.session.add(user)
        db.session.commit()
 
        return redirect(url_for("index"))
 
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login(): # método para logar um usuário
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Credenciais incorretas.")
            return redirect(url_for("login"))
        
        if not check_password_hash(user.password, password):
            flash("Credenciais incorretas.")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("index")) 
    return render_template("login.html")
@app.route("/logout")
def logout(): # método para deslogar um usuário
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__": # verifica a condição para rodar o app no modo debug
    app.run(debug=True)