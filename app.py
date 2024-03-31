from flask import Flask, jsonify, render_template, request, redirect, session
from usuario import Usuario
from chat import Chat



app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect('/chat')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        telefone = request.form['telefone']
        senha = request.form['senha']
        usuario = Usuario()
        usuario.logar(telefone, senha)
        if usuario.logado:
            usuario_dict = {
                'telefone': usuario.telefone,
                'nome': usuario.nome,
                'logado': usuario.logado
            }
            # Armazenar o dicionário na sessão
            session['usuario'] = usuario_dict
            return redirect('/chat')
        return 'Usuário ou senha inválido'
    else:
        return render_template('login.html')
    
@app.route('/cadastro', methods=['POST'])
def cadastro():
    telefone = request.form.get('telefone')
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    usuario = Usuario()

    if usuario.cadastrar(telefone, nome, senha):
        session['usuario_logado'] = {'nome': usuario.nome, 'telefone': usuario.telefone}
        return render_template("chat.html")
    else:
        session.clear()
        return jsonify({'mensagem': 'Erro ao cadastrar'}), 500


    # if request.method == 'POST':
    #     nome = request.form['nome']
    #     telefone = request.form['telefone']
    #     senha = request.form['senha']

    #     usuario = Usuario()
    #     cadastrado = usuario.cadastrar(telefone, nome, senha)

    #     if cadastrado:
    #         # Se o usuário for cadastrado com sucesso, redirecione para a página de login
    #         return redirect('/')
    #     else:
    #         # Se ocorrer um erro ao cadastrar, retorne para a página de cadastro com uma mensagem de erro
    #         return render_template("index.html", mensagem="Erro ao cadastrar usuário.")

@app.route('/chat')
def chat():
    if 'usuario' not in session:
        return redirect('/')
    usuario_dict = session['usuario']
    usuario = Usuario()
    usuario.telefone = usuario_dict['telefone']
    usuario.nome = usuario_dict['nome']
    usuario.logado = usuario_dict['logado']
    chatcrabiz = Chat(usuario.nome, usuario.telefone)
    contatos = chatcrabiz.retorna_contatos()
    
    # Aqui você precisa obter as mensagens apenas para o usuário logado
    mensagens = chatcrabiz.verificar_mensagem()
    
    return render_template('chat.html', contatos=contatos, mensagens=mensagens, usuario=usuario)


@app.route('/enviar', methods=['POST'])
def enviar_mensagem():
    if 'usuario' not in session:
        return redirect('/')
    
    usuario_dict = session['usuario']
    chatcrabiz = Chat(usuario_dict['nome'], usuario_dict['telefone'])
    
    destinatario_nome = request.form.get('destinatario')
    mensagem = request.form.get('mensagem')
    
    # Encontrar o contato pelo nome
    contato = None
    for c in chatcrabiz.retorna_contatos():
        if c.nome == destinatario_nome:
            contato = c
            break
    
    if contato is None:
        return 'Contato não encontrado'
    
    if chatcrabiz.enviar_mensagem(mensagem, contato, usuario_dict['nome']):  # Adicione o nome do remetente como argumento
        return redirect('/chat')
    else:
        return 'Erro ao enviar mensagem'



@app.route('/mensagens')
def carregar_mensagens():
    if 'usuario' not in session:
        return redirect('/')
    
    nome_destinatario = request.args.get('contato')

    if nome_destinatario:
        # Obtenha as mensagens para o contato especificado
        chatcrabiz = Chat(session['usuario']['nome'], session['usuario']['telefone'])
        mensagens = chatcrabiz.obter_mensagens_para_contato(nome_destinatario)
        return render_template('mensagens.html', mensagens=mensagens)
    else:
        return 'Nome do destinatário não especificado'




if __name__ == '__main__':
    app.run(debug=True)
