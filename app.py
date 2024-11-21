from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='tamplates')

#usúarios ficticio
usuarios = {
    'admin': 'senha123',
    'user1': 'senha456'
}

#rota para a página principal

@app.route('/cadastro', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Verifica se o usúario e senha estão corretos
        if username in usuarios and usuarios[username] == password:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro = 'Usuario ou senha invalidos')
        
    return render_template('cadastro.html')

@app.route('/index')
def index():
    return render_template('index.html')

#inicia o servidor 
if __name__ == '__main__':
    app.run(debug=True)
