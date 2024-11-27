from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 


pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='templates', static_url_path = '/static', static_folder = 'static')

app.secret_key = 'organize' #chave de acesso

#configuração do Banco de Dados (usando Mysql como exemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:matheus20@localhost/form'
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False #desativar notificações de modificação
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

#
class Usuario(UserMixin, db.Model):
    __tablename__ = 'users' #nome da tabela Banco de Dados

    #definição das colunas
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #coluna id 
    nome_completo = db.Column(db.String(255), nullable = False) #coluna nome completo
    email = db.Column(db.String(255), nullable = False, unique = True) #coluna para email
    senha = db.Column(db.String(255), nullable = False) #coluna para senha
    confirmar_senha = db.Column(db.String(255), nullable = False) #coluna confirmar senha
    
    def __repr__(self):
        return f"<Usuario {self.nome_completo}>"
    
#função carregamento do usuário
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

#rota para a página de cadastro
@app.route('/cadastro', methods = ['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods = ['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        #recebe os dados do formulario
        nome_completo = request.form['username']
        email = request.form['email']
        senha = request.form['senha']
        conSenha = request.form['conPassword']

    #verifica se senha coecidem

        if senha != conSenha:
            flash('As senhas não coecidem!', 'error')
            return redirect(url_for('cadastro'))
        
        #verifica email cadastrado
        usuarioExistente = Usuario.query.filter_by(email = email).first()
        if usuarioExistente:
             flash('E-mail já cadastrado. Tente novamente com outro e-mail.', 'error')
             return redirect(url_for('cadastro'))
        
        #criptografia a senha 
        hashed_password = bcrypt.generate_password_hash(senha).decode('utf-8')

        
        #criar novo usuario
        novo_usuario = Usuario(nome_completo = nome_completo, email = email, senha = hashed_password, confirmar_senha = conSenha)

        
        
        #adiciona ao banco de dados e faz commit
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça o login para continuar. ', 'sucess')
        return redirect(url_for('home')) #página de login
    return render_template('cadastro.html')

#rota para a página de login
@app.route('/index', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        #verifica se o usuario existe
        usuario = Usuario.query.filter_by(email = email).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos!', 'error')
    return render_template('index.html')

#página dashboard (após o login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome = current_user.nome_completo)

#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta', 'info')
    return redirect(url_for('login'))

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html') #página login.html ou index.html

@app.route('/esqueci_senha', methods = ['GET','POST'])
def forgot():
    return render_template('esqueci_senha.html')


    #criação de tabelas
    #with app.app_context():
try:
    db.create_all() #cria as tabelas no banco de dados 
    print("Tabelas criadas com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    
    #inicia o servidor 
if __name__ == '__main__':
    app.run(debug=True)
