from flask import Flask, url_for,render_template,request, redirect, session, Blueprint, flash
import arquivos.ArvoreB.BTreeBiblioteca as bt

import pandas
import json
import os

#VARIAVEIS PARA A ARVORE
RAIZ_CPF = None
RAIZ_NOME = None
DATAFRAME = None
CHAVE_CONTADOR = 0
ORDEM = 10 
ARQUIVO_CLIENTES = 'Clientes.csv'

#//____________________//
app = Flask(__name__)
ARQUIVO_VOOS = "arquivos/voos.json"
ARQUIVOS_FUNCIONARIOS = "arquivos/funcionarios.json"
app.secret_key = "segredo123"
#rotas

@app.route('/')
def principal():
    return render_template('index.html')


@app.route('/listaCatalogo')
def listaCatalogo():
  titulo = "Voos"

  if os.path.exists(ARQUIVO_VOOS):
            with open(ARQUIVO_VOOS, "r") as arquivoJson:
                voos = json.load(arquivoJson)#COLOCAR UM ELSE

  return render_template('listaCatalogo.html', titulo = titulo, voos = voos)

@app.route('/tabelaUsuarios')
def tabelaUsuarios():
   titulo = "Informacoes dos usuarios"

   if os.path.exists(ARQUIVOS_FUNCIONARIOS):
            with open(ARQUIVOS_FUNCIONARIOS, "r") as arquivoJson:
                loginSenha = json.load(arquivoJson)#COLOCAR UM ELSE

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

      if os.path.exists(ARQUIVOS_FUNCIONARIOS):
            with open(ARQUIVOS_FUNCIONARIOS, "r") as arquivoJson:
                loginSenha = json.load(arquivoJson)#COLOCAR UM ELSE

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
   titulo = crudVoos      
   return render_template('crudVoos.html')



@app.route('/deletar', methods=['GET', 'POST'])
def deletar():
    if request.method == 'POST':
        codigo = request.form.get('codigo')

        if not os.path.exists(ARQUIVO_VOOS) or os.path.getsize(ARQUIVO_VOOS) == 0:
            voosDoArquivo = {}
        else:
            with open(ARQUIVO_VOOS, "r", encoding="utf-8") as arquivoJson:
                try:
                    voosDoArquivo = json.load(arquivoJson)
                except json.JSONDecodeError:
                    voosDoArquivo = {}

        if codigo in voosDoArquivo:
            del voosDoArquivo[codigo]
            with open(ARQUIVO_VOOS, "w", encoding="utf-8") as arquivo:
                json.dump(voosDoArquivo, arquivo, indent=4, ensure_ascii=False)
            flash(f"Voo {codigo} deletado com sucesso!", "sucesso")
        else:
            flash(f"Voo {codigo} não encontrado!", "erro")

        return render_template("deletar.html")
    
    return render_template("deletar.html")


@app.route('/alterar', methods=['GET', 'POST'])
def alterar():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        origem = request.form.get('origem')
        destino = request.form.get('destino')
        assentos = request.form.get('assentos')
        preco = request.form.get('preco')

        if os.path.exists(ARQUIVO_VOOS):
            with open(ARQUIVO_VOOS, "r") as arquivoJson:
                voosDoArquivo = json.load(arquivoJson)
        else:
            voosDoArquivo = {}

        if codigo in voosDoArquivo:
            
            voosDoArquivo[codigo]["origem"] = origem
            voosDoArquivo[codigo]["destino"] = destino
            voosDoArquivo[codigo]["assentos"] = int(assentos)
            voosDoArquivo[codigo]["preco"] = float(preco)

          
            with open(ARQUIVO_VOOS, "w") as arquivo:
                json.dump(voosDoArquivo, arquivo, indent=4, ensure_ascii=False)

            flash(f"Voo {codigo} atualizado com sucesso!", "sucesso")
        else:
            flash(f"O voo {codigo} não existe no arquivo!", "erro")

        return redirect(url_for('alterar'))

    return render_template('alterar.html')
      

@app.route('/criar', methods = ['GET','POST'])
def criar():

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

      with open("arquivos/voos.json", "r") as arquivoJson:
         voosDoArquivo = json.load(arquivoJson) #Dicionario
         voosDoArquivo[codigo] = voo

      with open("arquivos/voos.json", "w") as arquivo:
         json.dump(voosDoArquivo, arquivo, indent=4)
      
      return render_template('criar.html')
   return render_template('criar.html')

app.run(debug=True)

def inicializar_arvores():
    global RAIZ_CPF, RAIZ_NOME, DATAFRAME, CHAVE_CONTADOR

    colunas_dtype = {0: str}
    try:
        df = pd.read_csv(ARQUIVO_CLIENTES, header=None, dtype=colunas_dtype)
        RAIZ_CPF, RAIZ_NOME, CHAVE_CONTADOR = bt._InserirElementos(
        RAIZ_CPF, RAIZ_NOME, ORDEM, df, CHAVE_CONTADOR
        )
        DATAFRAME = df
        print("Árvores B (CPF e Nome) construídas com sucesso.")
    except FileNotFoundError:
            print(f"ERRO: Arquivo {ARQUIVO_DADOS} não encontrado. As árvores não foram carregadas.")

from flask import Flask, render_template, request, jsonify


@app.route('/BTreeClientes', methods = ['GET', 'POST'])
def BTreeClientes():
    resultado = None #MODIFICAR ARQUIVO HTML PARA RECEBER O REGISTRO
    
    if request.method == 'POST':
        
        nome = request.form.get('nome', default='').strip()

        if nome:
            reg_busca = bt.Registro()
            reg_busca.Chave = nome

            resultado_registro = bt.Pesquisa(reg_busca, RAIZ_NOME)
            
            if resultado_registro:
        
                indice_df = resultado_registro.Elemento
                dados_completos = DATAFRAME.iloc[indice_df].to_dict()

                resultado = {
                    "status": "sucesso",
                    "nome_buscado": nome,
                    "dados": dados_completos
                }
            else:
                resultado = {
                    "status": "nao_encontrado",
                    "nome_buscado": nome,
                    "mensagem": f"O nome '{nome}' não foi encontrado na Árvore B."
                }
        else:
            resultado = {
                "status": "aviso",
                "mensagem": "Por favor, digite um nome para pesquisar."
            }
        
    return render_template("BTreeClientes.html", resultado=resultado)