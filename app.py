from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='templates')

app.secret_key = 'organize'

#configuração do Banco de Dados (usando sqlite como exemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:matheus20@localhost/form'
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False #desativar notificações de modificação
db = SQLAlchemy(app)

#
class Usuario(db.Model):
    __tablename__ = 'users' #nome da tabela Banco de Dados

    #definição das colunas
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #coluna id 
    nome_completo = db.Column(db.String(255), nullable = False) #coluna nome completo
    email = db.Column(db.String(255), nullable = False, unique = True) #coluna para email
    senha = db.Column(db.String(255), nullable = False) #coluna para senha
    confirmar_senha = db.Column(db.String(255), nullable = False) #coluna confirmar senha
    
    def __repr__(self):
        return f"<Usuario {self.nome_completo}>"

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
            # 
            return "As senhas não coecidem", 400
        
        #verifica email cadastrado
        usuarioExistente = Usuario.query.filter_by(email = email).first()
        if usuarioExistente:
            # return "Este email já está cadastrado", 400
             flash('E-mail já cadastrado. Tente novamente com outro e-mail.', 'error')
             return redirect(url_for('cadastro'))
        
        #criptografia a senha 
        hashed_password = generate_password_hash(senha)

        
        #criar novo usuario
        novo_usuario = Usuario(nome_completo = nome_completo, email = email, senha = hashed_password, confirmar_senha = conSenha)

        
        
        #adiciona ao banco de dados e faz commit
        db.session.add(novo_usuario)
        db.session.commit()


        return redirect(url_for('home')) #página de login
    return render_template('cadastro.html')


@app.route('/', methods = ['GET'])

def home():
    return render_template('index.html') #página login.html ou index.html

@app.route('/esqueci_senha', methods = ['GET','POST'])
def forgot():
    return render_template('esqueci_senha.html')

#inicia o servidor 
if __name__ == '__main__':
    #criação de tabelas
    with app.app_context():
        db.create_all() #cria as tabelas no banco de dados 
    app.run(debug=True)
