from conexao import Conexao
from mensagem import Mensagem
from usuario import Usuario
from contato import Contato

class Chat:
    def __init__(self, nome: str, telefone: str):
        self.telefone_usuario = telefone
        self.nome_usuario = nome
        

    def enviar_mensagem(self, conteudo: str, destinatario: Contato) -> bool:
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            sql = "INSERT INTO tb_mensagem (tel_remetente, tel_destinatario, mensagem) VALUES (%s, %s, %s)"
            val = (self.telefone_usuario, destinatario.telefone, conteudo)  # Correção aqui
            mycursor.execute(sql, val)

            mydb.commit()
            mydb.close()

            return True
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False

    def verificar_mensagem(self):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # Consulta SQL para selecionar todas as mensagens sem filtrar pelo remetente
            sql = "SELECT tel_remetente, mensagem, nome FROM tb_mensagem tm INNER JOIN tb_usuario tu ON tm.tel_destinatario = tu.tel"
            
            mycursor.execute(sql)
            resultado = mycursor.fetchall()

            mensagens = []

            for linha in resultado:
                remetente = linha[0]
                mensagem = linha[1].decode('utf-8', 'ignore') if isinstance(linha[1], bytes) else linha[1]
                nome_destinatario = linha[2]
                mensagens.append(Mensagem(remetente, mensagem, nome_destinatario))

            return mensagens
        except Exception as e:
            print(f"Erro ao verificar mensagens: {e}")
            return []

    def retorna_contatos(self):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT nome, tel FROM tb_usuario WHERE tel != %s ORDER BY nome"  # Exclui o usuário logado da lista de contatos
            mycursor.execute(sql, (self.telefone_usuario,))
            resultado = mycursor.fetchall()

            lista_contatos = []

            for linha in resultado:
                lista_contatos.append(Contato(linha[0], linha[1]))

            return lista_contatos
        except Exception as e:
            print(f"Erro ao retornar contatos: {e}")
            return []