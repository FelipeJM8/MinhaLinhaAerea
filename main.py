from flask import Flask, url_for,render_template,request, redirect, session, Blueprint, flash
from arquivos.dados import voos
from arquivos.dados import loginSenha

app = Flask(__name__)

#rotas

@app.route('/')
def principal():
    return render_template('index.html')


@app.route('/listaCatalogo')
def listaCatalogo():
  titulo = "Voos"
  return render_template('listaCatalogo.html', titulo = titulo, voos = voos)

@app.route('/tabelaUsuarios')
def tabelaUsuarios():
   titulo = 'Informacoes dos usuarios'
   return render_template('tabelaUsuarios.html', titulo = titulo, loginSenha = loginSenha) 

@app.route('/opcoes')
def opcoes():
   titulo = opcoes
   return render_template('opcoes.html')

@app.route('/login', methods = ['GET','POST'])
def login():
      
   if request.method == 'POST':

      email= request.form.get('email')
      senha = request.form.get('senha')

      if email in loginSenha and loginSenha[email]['senha'] == senha:
          return redirect(url_for('opcoes'))
      else:
         return render_template('login.html', error='ERRO')

      
   return render_template('login.html')

@app.route('/loginUsuario', methods = ['GET','POST'])
def loginUsuario():
      titulo = loginUsuario      
      return render_template('loginUsuario.html')

app.run(debug=True)