from flask import Flask, url_for,render_template,request, redirect, session, Blueprint, flash

import json
import os

app = Flask(__name__)
ARQUIVO_VOOS = "arquivos/voos.json"
ARQUIVOS_USUARIOS = "arquivos/funcionarios.json"#PRECISO ESCOLHER SE USUARIO E FUNCIONARIO VAI SER SEPARADO PARA TIRAR ESSA GAMBIARRA
app.secret_key = "segredo123"
#rotas

@app.route('/')#PRECISA SUBSTITUIR TOTALMENTE O ARQUIVO "dados" OU SEJA FAZER OS OUTRO json;
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

   if os.path.exists(ARQUIVOS_USUARIOS):
            with open(ARQUIVOS_USUARIOS, "r") as arquivoJson:
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

      if os.path.exists(ARQUIVOS_USUARIOS):
            with open(ARQUIVOS_USUARIOS, "r") as arquivoJson:
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


@app.route('/BTreeClientes')
def BTreeClientes():

    
    Ap, chave, dataframe = Inserir(Ap, chave)

    dataframe = pd.read_csv(arq)
    
    Ap, chave = _InserirElementos(Ap, ordem, dataframe, chave)

    reg.Chave = dataframe.iloc[i, 0]
    reg.Elemento = i

    Ap = _Insere(reg, Ap, ordem)

    return render_template("BTreeClientes.html")