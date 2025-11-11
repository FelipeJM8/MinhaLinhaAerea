from flask import Flask, url_for,render_template,request, redirect, session, Blueprint, flash
#from arquivos.dados import voos
from arquivos.dados import loginSenha
import json
import os

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

@app.route('/crudVoos', methods = ['GET','POST'])
def crudVoos():

   if request.method == 'POST':

      codigo = request.form.get('codigo')
      origem = request.form.get('origem')
      destino = request.form.get('destino')
      assentos = request.form.get('assentos')
      preco = request.form.get('preco')

   voo = {
   "codigo": codigo,
   "origem": origem,
   "destino": destino,
   "assentos": assentos,
   "preco": preco
   }
   string_json_formatada = json.dumps(dados_voo, indent=4)
       
   ARQUIVO_VOOS = 'voos.json'


   voos_existentes = []
   if os.path.exists(ARQUIVO_VOOS):
      with open(ARQUIVO_VOOS, 'r') as arquivo:
            try:
               voos_existentes = json.load(arquivo)
            except json.JSONDecodeError:
               voos_existentes = []

   voos_existentes.append(voo)

   with open(ARQUIVO_VOOS, 'w') as arquivo:
      json.dump(voos_existentes, arquivo, indent=4)
            
            
   return render_template('cruDvoos.html')




app.run(debug=True)