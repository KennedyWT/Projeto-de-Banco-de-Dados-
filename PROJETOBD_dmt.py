import mysql.connector
from mysql.connector import Error
import PIL
from PIL import Image
import io

def conexao():
    try:
        con_BD = mysql.connector.connect(
            host='localhost',
            user='root',
            password='40028922',
            database='plataforma_de_vendas_de_jogos_online'
        )
        if con_BD.is_connected():
            print("Conexão bem-sucedida ao MySQL")
            return con_BD
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

conexao = conexao()

def exibir_imagem(foto):
    try:
        # Converter BLOB em objeto de imagem
        image = Image.open(io.BytesIO(foto))
        image.show()  # Abre a imagem na visualização padrão do sistema
    except Exception as e:
        print(f"Erro ao exibir a imagem: {e}")

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Perfil_Usuário
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_perfil_usuario(con_BD, idPerfil_Usuário, caminho_foto_perfil, Biografia, Localização):
    try:
        cursor = con_BD.cursor()
        
        # Ler o arquivo de imagem em modo binário
        with open(caminho_foto_perfil, 'rb') as file:
            Foto_perfil = file.read()
        
        sql = """
        INSERT INTO perfil_usuário (idPerfil_Usuário, Foto_perfil, Biografia, Localização)
        VALUES (%s, %s, %s, %s)
        """
        valores = (idPerfil_Usuário, Foto_perfil, Biografia, Localização)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Perfil do usuário inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir perfil do usuário: {e}")
    finally:
        cursor.close()
        

def ler_perfil_usuario(con_BD, idPerfil_Usuário):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idPerfil_Usuário, Foto_perfil, Biografia, Localização
        FROM perfil_usuário
        WHERE idPerfil_Usuário = %s
        """
        cursor.execute(sql, (idPerfil_Usuário,))
        resultado = cursor.fetchone()
        if resultado:
            idPerfil_Usuário, Foto_perfil, Biografia, Localização = resultado
            print(f"ID Perfil: {idPerfil_Usuário}")
            print(f"Biografia: {Biografia}")
            print(f"Localização: {Localização}")
            
            #Ele abre a imagem em um novo separador, ele tá usando uma função def exibir_imagem(foto),
            #para isso tem que instalar a biblioteca PIL (usando from PIL import Image) e a IO
            exibir_imagem(Foto_perfil)

            # Se quiser salvar a foto em um arquivo, pode fazer assim:
            with open('foto_perfil.jpg', 'wb') as file:
                file.write(Foto_perfil)
            print("Foto do perfil salva como 'foto_perfil.jpg'")
        else:
            print("Perfil de usuário não encontrado.")
    except Error as e:
        print(f"Erro ao inserir perfil do usuário: {e}")
    finally:
        cursor.close()

def atualizar_perfil_usuario(con_BD, idPerfil_Usuário):
    ler_perfil_usuario(conexao, idPerfil_Usuário)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Foto de Perfil")
    print("2. Biografia")
    print("3. Localização")
    print("4. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_caminho_foto_perfil = input("Digite o caminho da nova foto de perfil: ")
            with open(novo_caminho_foto_perfil, 'rb') as file:
                nova_foto_perfil = file.read()
            sql = "UPDATE perfil_usuário SET Foto_perfil = %s WHERE idPerfil_Usuário = %s"
            valores = (nova_foto_perfil, idPerfil_Usuário)
            cursor.execute(sql, valores)
        elif escolha == '2':
            nova_biografia = input("Digite a nova biografia: ")
            sql = "UPDATE perfil_usuário SET Biografia = %s WHERE idPerfil_Usuário = %s"
            valores = (nova_biografia, idPerfil_Usuário)
            cursor.execute(sql, valores)
        elif escolha == '3':
            nova_localizacao = input("Digite a nova localização: ")
            sql = "UPDATE perfil_usuário SET Localização = %s WHERE idPerfil_Usuário = %s"
            valores = (nova_localizacao, idPerfil_Usuário)
            cursor.execute(sql, valores)
        elif escolha == '4':
            print("Saindo da atualização de perfil.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do perfil atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar perfil do usuário: {e}")
    
    finally:
        cursor.close()


def deletar_perfil_usuario(con_BD, idPerfil_Usuário): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM perfil_usuário
        WHERE idPerfil_Usuário = %s
        """
        cursor.execute(sql, (idPerfil_Usuário,))
        con_BD.commit()
        print("Perfil do usuário deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar perfil do usuário: {e}")
    finally:
        cursor.close()
    
    
#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Usuário
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_usuario(con_BD, idUsuario, Data_Nascimento, Nome, Data_Cadastro, Email, Telefone, ID_Biblioteca, ID_Perfil_Usuário, ID_Carrinho_de_Compras):
    try:
        cursor = con_BD.cursor()
        sql = """
        INSERT INTO usuário (idUsuario, Data_Nascimento, Nome, Data_Cadastro, Email, Telefone, ID_Biblioteca, ID_Perfil_Usuário, ID_Carrinho_de_Compras)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (idUsuario, Data_Nascimento, Nome, Data_Cadastro, Email, Telefone, ID_Biblioteca, ID_Perfil_Usuário, ID_Carrinho_de_Compras)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Usuário inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir usuário: {e}")
    finally:
        cursor.close()


def ler_usuario(con_BD, idUsuario):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idUsuario, Data_Nascimento, Nome, Data_Cadastro, Email, Telefone
        FROM usuário
        WHERE idUsuario = %s
        """
        cursor.execute(sql, (idUsuario,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            idUsuario, Data_Nascimento, Nome, Data_Cadastro, Email, Telefone = resultado
            print(f"ID Usuário: {idUsuario}")
            print(f"Data nascimento: {Data_Nascimento}")
            print(f"Nome: {Nome}")
            print(f"Data cadastro: {Data_Cadastro}")
            print(f"Email: {Email}")
            print(f"Telefone: {Telefone}")
            
        else:
            print("Usuário não encontrado.")
    except Error as e:
        print(f"Erro ao ler perfil do usuário: {e}")
    finally:
        cursor.close()


def atualizar_usuario(con_BD, idUsuario):
    ler_usuario(conexao, idUsuario)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Data de Nascimento")
    print("2. Nome")
    print("3. Email")
    print("4. Telefone")
    print("5. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            nova_data_nasc = input("Digite a nova data de nascimento: ")
            sql = "UPDATE usuário SET Data_Nascimento = %s WHERE idUsuario = %s"
            valores = (nova_data_nasc, idUsuario)
            cursor.execute(sql, valores)
        elif escolha == '2':
            novo_nome = input("Digite o novo nome: ")
            sql = "UPDATE usuário SET Nome = %s WHERE idUsuario = %s"
            valores = (novo_nome, idUsuario)
            cursor.execute(sql, valores)
        elif escolha == '3':
            novo_email = input("Digite o novo email: ")
            sql = "UPDATE usuário SET Email = %s WHERE idUsuario = %s"
            valores = (novo_email, idUsuario)
            cursor.execute(sql, valores)
        elif escolha == '4':
            novo_telefone = input("Digite o novo telefone: ")
            sql = "UPDATE usuário SET Telefone = %s WHERE idUsuario = %s"
            valores = (novo_telefone, idUsuario)
            cursor.execute(sql, valores)
        elif escolha == '5':
            print("Saindo da atualização de dados de usuário.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do usuário atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar dados do usuário: {e}")
    
    finally:
        cursor.close()
        
def deletar_usuario(con_BD, idUsuario): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM usuário
        WHERE idUsuario = %s
        """
        cursor.execute(sql, (idUsuario,))
        con_BD.commit()
        print("Usuário deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar Usuário: {e}")
    finally:
        cursor.close()

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Biblioteca_de_Jogos
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_biblioteca_jg(con_BD, idBiblioteca_de_Jogos, Status_Instalação, Data_de_Adição):
    try:
        cursor = con_BD.cursor()
        
        sql = """
        INSERT INTO biblioteca_de_jogos (idBiblioteca_de_Jogos, Status_Instalação, Data_de_Adição)
        VALUES (%s, %s, %s)
        """
        valores = (idBiblioteca_de_Jogos, Status_Instalação, Data_de_Adição)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Biblioteca de jogos feita com sucesso.")
    except Error as e:
        print(f"Erro ao fazer a biblioteca de jogos: {e}")
    finally:
        cursor.close()

def ler_biblioteca_jg(con_BD, idBiblioteca_de_Jogos):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idBiblioteca_de_Jogos, Status_Instalação, Data_de_Adição
        FROM biblioteca_de_jogos
        WHERE idBiblioteca_de_Jogos = %s
        """
        cursor.execute(sql, (idBiblioteca_de_Jogos,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            # Desempacotando o resultado da consulta
            idBiblioteca_de_Jogos, Status_Instalação, Data_de_Adição = resultado
            print(f"ID da biblioteca de jogos: {idBiblioteca_de_Jogos}")
            print(f"Status da Instalação: {Status_Instalação}")
            print(f"Dia que foi adionado: {Data_de_Adição}")
        else:
            print("Biblioteca não encontrada.")
    except Error as e:
        print(f"Erro ao ler a biblioteca: {e}")
    finally:
        cursor.close()


def atualizar_biblioteca_jg(con_BD, idBiblioteca_de_Jogos):
    ler_biblioteca_jg(conexao, idBiblioteca_de_Jogos)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Status da instalação")
    print("2. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_status = input("Digite a nova nota: ")
            sql = "UPDATE biblioteca_de_jogos SET Status_Instalação = %s WHERE idBiblioteca_de_Jogos = %s"
            valores = (novo_status, idBiblioteca_de_Jogos)
            cursor.execute(sql, valores)
        elif escolha == '2':
            print("Saindo da atualização de dados da biblioteca.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Biblioteca atualizada com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar à biblioteca: {e}")
    
    finally:
        cursor.close()
        
def deletar_biblioteca_jg(con_BD, idBiblioteca_de_Jogos): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM biblioteca_de_jogos
        WHERE idBiblioteca_de_Jogos = %s
        """
        cursor.execute(sql, (idBiblioteca_de_Jogos,))
        con_BD.commit()
        print("Biblioteca deletada com sucesso.")
    except Error as e:
        print(f"Erro ao deletar a nbiblioteca: {e}")
    finally:
        cursor.close()

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Avaliação
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_avaliacao(con_BD, idAvaliação, Nota, Comentário):
    try:
        cursor = con_BD.cursor()
        
        sql = """
        INSERT INTO avaliação (idAvaliação, Nota, Comentário)
        VALUES (%s, %s, %s)
        """
        valores = (idAvaliação, Nota, Comentário)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Avaliação feita com sucesso.")
    except Error as e:
        print(f"Erro ao fazer a avaliação: {e}")
    finally:
        cursor.close()

def ler_avaliacao(con_BD, idAvaliação):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idAvaliação, Nota, Comentário
        FROM avaliação
        WHERE idAvaliação = %s
        """
        cursor.execute(sql, (idAvaliação,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            # Desempacotando o resultado da consulta
            idAvaliação, Nota, Comentário = resultado
            print(f"ID da avaliação: {idAvaliação}")
            print(f"Nota: {Nota}")
            print(f"Comentário: {Comentário}")
        else:
            print("Avaliação não encontrada.")
    except Error as e:
        print(f"Erro ao ler avaliação: {e}")
    finally:
        cursor.close()


def atualizar_avaliacao(con_BD, idAvaliação):
    ler_avaliacao(conexao, idAvaliação)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Nota")
    print("2. Comentário")
    print("3. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            nova_nota = input("Digite a nova nota: ")
            sql = "UPDATE avaliação SET Nota = %s WHERE idAvaliação = %s"
            valores = (nova_nota, idAvaliação)
            cursor.execute(sql, valores)
        elif escolha == '2':
            novo_comentário = input("Digite seu novo comentário: ")
            sql = "UPDATE avaliação SET Comentário = %s WHERE idAvaliação = %s"
            valores = (novo_comentário, idAvaliação)
            cursor.execute(sql, valores)
        elif escolha == '3':
            print("Saindo da atualização de dados do carrinho.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Nota atualizada com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar à nota: {e}")
    
    finally:
        cursor.close()
        
def deletar_avaliacao(con_BD, idAvaliação): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM avaliação
        WHERE idAvaliação = %s
        """
        cursor.execute(sql, (idAvaliação,))
        con_BD.commit()
        print("Avaliação deletada com sucesso.")
    except Error as e:
        print(f"Erro ao deletar a nota: {e}")
    finally:
        cursor.close()

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Carrinho_de_Compras
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_carrinho_compras(con_BD, idCarrinho_de_Compras, Data_de_Adição, Quantidade, ID_Loja):
    try:
        cursor = con_BD.cursor()
        
        sql = """
        INSERT INTO carrinho_de_compras (idCarrinho_de_Compras, Data_de_Adição, Quantidade, ID_Loja)
        VALUES (%s, %s, %s, %s)
        """
        valores = (idCarrinho_de_Compras, Data_de_Adição, Quantidade, ID_Loja)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Carrinho inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir carrinho: {e}")
    finally:
        cursor.close()

def ler_carrinho_de_compras(con_BD, idCarrinho_de_Compras):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idCarrinho_de_Compras, Data_de_Adição, Quantidade, ID_Loja
        FROM carrinho_de_compras
        WHERE idCarrinho_de_Compras = %s
        """
        cursor.execute(sql, (idCarrinho_de_Compras,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            # Desempacotando o resultado da consulta
            idCarrinho, Data_de_Adição, Quantidade, ID_Loja = resultado
            print(f"ID carrinho de compras: {idCarrinho}")
            print(f"Data de adição: {Data_de_Adição}")
            print(f"Quantidade de itens: {Quantidade}")
            print(f"ID Loja: {ID_Loja}")
        else:
            print("Carrinho não encontrado.")
    except Error as e:
        print(f"Erro ao ler carrinho do usuário: {e}")
    finally:
        cursor.close()


def atualizar_carrinho(con_BD, idCarrinho_de_Compras):
    ler_carrinho_de_compras(conexao, idCarrinho_de_Compras)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Quantidade")
    print("2. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            nova_quantidade = input("Digite a nova quantidade: ")
            sql = "UPDATE carrinho_de_compras SET Quantidade = %s WHERE idCarrinho_de_Compras = %s"
            valores = (nova_quantidade, idCarrinho_de_Compras)
            cursor.execute(sql, valores)
        elif escolha == '2':
            print("Saindo da atualização de dados do carrinho.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do usuário atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar dados do usuário: {e}")
    
    finally:
        cursor.close()
        
def deletar_carrinho(con_BD, idCarrinho_de_Compras): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM carrinho_de_compras
        WHERE idCarrinho_de_Compras = %s
        """
        cursor.execute(sql, (idCarrinho_de_Compras,))
        con_BD.commit()
        print("Carrinho deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar o carrinho: {e}")
    finally:
        cursor.close()
#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Desenvolvedor
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_desenvolvedor(con_BD, idDesenvolvedor, Nome, Telefone, Email, ID_Perfil_Usuário):
    try:
        cursor = con_BD.cursor()
        sql = """
        INSERT INTO desenvolvedor (idDesenvolvedor, Nome, Telefone, Email, ID_Perfil_Usuário)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (idDesenvolvedor, Nome, Telefone, Email, ID_Perfil_Usuário)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Desenvolvedor inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir desenvolvedor: {e}")
    finally:
        cursor.close()


def ler_desenvolvedor(con_BD, idDesenvolvedor):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idDesenvolvedor, Nome, Telefone, Email
        FROM desenvolvedor
        WHERE idDesenvolvedor = %s
        """
        cursor.execute(sql, (idDesenvolvedor,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            idDesenvolvedor, Nome, Telefone, Email = resultado
            print(f"ID Desenvolvedor: {idDesenvolvedor}")
            print(f"Nome: {Nome}")
            print(f"Telefone: {Telefone}")
            print(f"Email: {Email}")
            
        else:
            print("Desenvolvedor não encontrado.")
    except Error as e:
        print(f"Erro ao ler perfil do desenvolvedor: {e}")
    finally:
        cursor.close()


def atualizar_desenvolvedor(con_BD, idDesenvolvedor):
    ler_desenvolvedor(conexao, idDesenvolvedor)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Nome")
    print("2. Telefone")
    print("3. Email")
    print("4. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_nome = input("Digite o novo nome: ")
            sql = "UPDATE desenvolvedor SET Nome = %s WHERE idDesenvolvedor = %s"
            valores = (novo_nome, idDesenvolvedor)
            cursor.execute(sql, valores)
        elif escolha == '2':
            novo_telefone = input("Digite o novo telefone: ")
            sql = "UPDATE desenvolvedor SET Telefone = %s WHERE idDesenvolvedor = %s"
            valores = (novo_telefone, idDesenvolvedor)
            cursor.execute(sql, valores)
        elif escolha == '3':
            novo_email = input("Digite o novo email: ")
            sql = "UPDATE desenvolvedor SET Email = %s WHERE idDesenvolvedor = %s"
            valores = (novo_email, idDesenvolvedor)
            cursor.execute(sql, valores)
        elif escolha == '4':
            print("Saindo da atualização de dados de usuário.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do usuário atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar dados do usuário: {e}")
    
    finally:
        cursor.close()
        
def deletar_desenvolvedor(con_BD, idDesenvolvedor): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM desenvolvedor
        WHERE idDesenvolvedor = %s
        """
        cursor.execute(sql, (idDesenvolvedor,))
        con_BD.commit()
        print("Desenvolvedor deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar desenvolvedor: {e}")
    finally:
        cursor.close()

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Jogo
#-----------------------------------------------------------------------------------------------------------------------------
def inserir_jogo(con_BD, idJogo, Descrição, Titulo, Categoria, Data_Lancamento, Capa, Processador, Memoria_RAM, Placa_de_Vídeo, Armazenamento):
    try:
        cursor = con_BD.cursor()
        
        # Ler o arquivo de imagem em modo binário
        with open(Capa, 'rb') as file:
            Foto_perfil = file.read()
        
        sql = """
        INSERT INTO jogo (idJogo, Descrição, Titulo, Categoria, Data_Lancamento, Capa, Processador, Memoria_RAM, Placa_de_Vídeo, Armazenamento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (idJogo, Descrição, Titulo, Categoria, Data_Lancamento, Capa, Processador, Memoria_RAM, Placa_de_Vídeo, Armazenamento)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Jogo inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir jogo: {e}")
    finally:
        cursor.close()
        

def ler_jogo(con_BD, idJogo):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idJogo, Descrição, Titulo, Categoria, Data_Lancamento, Capa, Processador, Memoria_RAM, Placa_de_Vídeo, Armazenamento
        FROM jogo
        WHERE idJogo = %s
        """
        cursor.execute(sql, (idJogo,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            idJogo, Descrição, Titulo, Categoria, Data_Lancamento, Capa, Processador, Memoria_RAM, Placa_de_Vídeo, Armazenamento = resultado
            print(f"ID do jogo: {idJogo}")
            print(f"Descrição do jogo: {Descrição}")
            print(f"Titulo: {Titulo}")
            print(f"Categoria: {Categoria}")
            print(f"Data de lançamento: {Data_Lancamento}")
            print(f"Capa: {Capa}")
            print(f"Requisitos de processador: {Processador}")
            print(f"Requisitos de memoria_RAM: {Memoria_RAM}")
            print(f"Requisitos de placa_de_Vídeo: {Placa_de_Vídeo}")
            print(f"Requisitos de armazenamento: {Armazenamento}")
            
            #Ele abre a imagem em um novo separador, ele tá usando uma função def exibir_imagem(foto),
            #para isso tem que instalar a biblioteca PIL (usando from PIL import Image) e a IO
            exibir_imagem(Capa)

            # Se quiser salvar a foto em um arquivo, pode fazer assim:
            with open('Capa.jpg', 'wb') as file:
                file.write(Capa)
            print("Foto da capa salva como 'Elden Ring.jpg'")
        else:
            print("Capa não encontrada.")
    except Error as e:
        print(f"Erro ao inserir capa do jogo: {e}")
    finally:
        cursor.close()

def atualizar_jogo(con_BD, idJogo):
    ler_jogo(conexao, idJogo)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Descrição")
    print("2. Titulo")
    print("3. Categoria")
    print("4. Data de Lançamento")
    print("5. Capa")
    print("6. Processador")
    print("7. Memoria RAM")
    print("8. Placa de Video")
    print("9. Armazenamento")
    print("4. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            nova_descricao = input("Digite a nova descrição: ")
            sql = "UPDATE jogo SET Descrição = %s WHERE idJogo = %s"
            valores = (nova_descricao, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '2':
            novo_titulo = input("Digite o novo titulo: ")
            sql = "UPDATE jogo SET Titulo = %s WHERE idJogo = %s"
            valores = (novo_titulo, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '3':
            nova_categoria = input("Digite a nova categoria: ")
            sql = "UPDATE jogo SET Categoria = %s WHERE idJogo = %s"
            valores = (nova_categoria, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '4':
            nova_data_lanc = input("Digite a nova data de lançamento: ")
            sql = "UPDATE jogo SET Data_Lacamento = %s WHERE idJogo = %s"
            valores = (nova_data_lanc, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '5':
            nova_capa = input("Digite o caminho da nova capa do jogo: ")
            with open(nova_capa, 'rb') as file:
                nova_capa  = file.read()
            sql = "UPDATE jogo SET Capa = %s WHERE idJogo = %s"
            valores = (nova_capa, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '6':
            novo_processador = input("Digite o novo processador: ")
            sql = "UPDATE jogo SET Processador = %s WHERE idJogo = %s"
            valores = (novo_processador, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '7':
            nova_ram = input("Digite a nova quantidade de memoria RAM: ")
            sql = "UPDATE jogo SET Memoria_RAM = %s WHERE idJogo = %s"
            valores = (nova_ram, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '8':
            nova_placa = input("Digite a nova placa de vídeo: ")
            sql = "UPDATE jogo SET Placa_de_Vídeo = %s WHERE idJogo = %s"
            valores = (nova_placa, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '9':
            novo_armazenamento = input("Digite o novo armazenamento: ")
            sql = "UPDATE jogo SET Armazenamento = %s WHERE idJogo = %s"
            valores = (novo_armazenamento, idJogo)
            cursor.execute(sql, valores)
        elif escolha == '10':
            print("Saindo da atualização de jogo.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do jogo atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar dados do jogo: {e}")
    
    finally:
        cursor.close()


def deletar_jogo(con_BD, idJogo): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM jogo
        WHERE idJogo = %s
        """
        cursor.execute(sql, (idJogo,))
        con_BD.commit()
        print("Jogo deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar jogo: {e}")
    finally:
        cursor.close()


#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Pagamento
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_pagamento(con_BD, idPagamento, Tipo_Pagamento, Status_Pagamento, Data_Pagamento, ID_Carrinhos_de_Compras):
    try:
        cursor = con_BD.cursor()
        sql = """
        INSERT INTO Pagamento (idPagamento, Tipo_Pagamento, Status_Pagamento, Data_Pagamento, ID_Carrinhos_de_Compras)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (idPagamento, Tipo_Pagamento, Status_Pagamento, Data_Pagamento, ID_Carrinhos_de_Compras)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Pagamento inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir pagamento: {e}")
    finally:
        cursor.close()

def ler_pagamento(con_BD, idPagamento):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idPagamento, Tipo_Pagamento, Status_Pagamento, Data_Pagamento, ID_Carrinhos_de_Compras
        FROM Pagamento
        WHERE idPagamento = %s
        """
        cursor.execute(sql, (idPagamento,))
        resultado = cursor.fetchone()
        if resultado:
            idPagamento, Tipo_Pagamento, Status_Pagamento, Data_Pagamento, ID_Carrinhos_de_Compras = resultado
            print(f"ID do Pagamento: {idPagamento}")
            print(f"Tipo de Pagamento: {Tipo_Pagamento}")
            print(f"Status do Pagamento: {Status_Pagamento}")
            print(f"Data do Pagamento: {Data_Pagamento}")
            print(f"ID do Carrinho de Compras: {ID_Carrinhos_de_Compras}")
        else:
            print("Pagamento não encontrado.")
    except Error as e:
        print(f"Erro ao ler pagamento: {e}")
    finally:
        cursor.close()

def atualizar_pagamento(con_BD, idPagamento):
    ler_pagamento(con_BD, idPagamento)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Tipo de Pagamento")
    print("2. Status do Pagamento")
    print("3. Data de Pagamento")
    print("4. ID do Carrinho de Compras")
    print("5. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_tipo = input("Digite o novo tipo de pagamento: ")
            sql = "UPDATE Pagamento SET Tipo_Pagamento = %s WHERE idPagamento = %s"
            valores = (novo_tipo, idPagamento)
            cursor.execute(sql, valores)
        elif escolha == '2':
            novo_status = input("Digite o novo status do pagamento: ")
            sql = "UPDATE Pagamento SET Status_Pagamento = %s WHERE idPagamento = %s"
            valores = (novo_status, idPagamento)
            cursor.execute(sql, valores)
        elif escolha == '3':
            nova_data = input("Digite a nova data de pagamento (YYYY-MM-DD): ")
            sql = "UPDATE Pagamento SET Data_Pagamento = %s WHERE idPagamento = %s"
            valores = (nova_data, idPagamento)
            cursor.execute(sql, valores)
        elif escolha == '4':
            novo_id_carrinho = input("Digite o novo ID do carrinho de compras: ")
            sql = "UPDATE Pagamento SET ID_Carrinhos_de_Compras = %s WHERE idPagamento = %s"
            valores = (novo_id_carrinho, idPagamento)
            cursor.execute(sql, valores)
        elif escolha == '5':
            print("Saindo da atualização de dados de pagamento.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do pagamento atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar pagamento: {e}")
    
    finally:
        cursor.close()

def deletar_pagamento(con_BD, idPagamento):
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM Pagamento
        WHERE idPagamento = %s
        """
        cursor.execute(sql, (idPagamento,))
        con_BD.commit()
        print("Pagamento deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar pagamento: {e}")
    finally:
        cursor.close()


#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Sistema_Operacional
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_sistema_operacional(con_BD, IP, Nome, Versão, Fabricante, Data_Lançamento):
    try:
        cursor = con_BD.cursor()
        sql = """
        INSERT INTO Sistema_Operacional (IP, Nome, Versão, Fabricante, Data_Lançamento)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (IP, Nome, Versão, Fabricante, Data_Lançamento)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Sistema Operacional inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir sistema operacional: {e}")
    finally:
        cursor.close()

def ler_sistema_operacional(con_BD, IP):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT IP, Nome, Versão, Fabricante, Data_Lançamento
        FROM Sistema_Operacional
        WHERE IP = %s
        """
        cursor.execute(sql, (IP,))
        resultado = cursor.fetchone()
        if resultado:
            IP, Nome, Versão, Fabricante, Data_Lançamento = resultado
            print(f"IP: {IP}")
            print(f"Nome: {Nome}")
            print(f"Versão: {Versão}")
            print(f"Fabricante: {Fabricante}")
            print(f"Data de Lançamento: {Data_Lançamento}")
        else:
            print("Sistema Operacional não encontrado.")
    except Error as e:
        print(f"Erro ao ler sistema operacional: {e}")
    finally:
        cursor.close()

def atualizar_sistema_operacional(con_BD, IP):
    ler_sistema_operacional(con_BD, IP)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Nome")
    print("2. Versão")
    print("3. Fabricante")
    print("4. Data de Lançamento")
    print("5. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_nome = input("Digite o novo nome: ")
            sql = "UPDATE Sistema_Operacional SET Nome = %s WHERE IP = %s"
            valores = (novo_nome, IP)
            cursor.execute(sql, valores)
        elif escolha == '2':
            nova_versao = input("Digite a nova versão: ")
            sql = "UPDATE Sistema_Operacional SET Versão = %s WHERE IP = %s"
            valores = (nova_versao, IP)
            cursor.execute(sql, valores)
        elif escolha == '3':
            novo_fabricante = input("Digite o novo fabricante: ")
            sql = "UPDATE Sistema_Operacional SET Fabricante = %s WHERE IP = %s"
            valores = (novo_fabricante, IP)
            cursor.execute(sql, valores)
        elif escolha == '4':
            nova_data = input("Digite a nova data de lançamento (YYYY-MM-DD): ")
            sql = "UPDATE Sistema_Operacional SET Data_Lançamento = %s WHERE IP = %s"
            valores = (nova_data, IP)
            cursor.execute(sql, valores)
        elif escolha == '5':
            print("Saindo da atualização de dados do sistema operacional.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do sistema operacional atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar sistema operacional: {e}")
    
    finally:
        cursor.close()

def deletar_sistema_operacional(con_BD, IP):
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM Sistema_Operacional
        WHERE IP = %s
        """
        cursor.execute(sql, (IP,))
        con_BD.commit()
        print("Sistema Operacional deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar sistema operacional: {e}")
    finally:
        cursor.close()

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Suporte
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_suporte(con_BD, Protocolo, Problema, Data_Solicitação, Resposta):
    try:
        cursor = con_BD.cursor()
        sql = """
        INSERT INTO Suporte (Protocolo, Problema, Data_Solicitação, Resposta)
        VALUES (%s, %s, %s, %s)
        """
        valores = (Protocolo, Problema, Data_Solicitação, Resposta)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Suporte inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir suporte: {e}")
    finally:
        cursor.close()
        
def ler_suporte(con_BD, Protocolo):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT Protocolo, Problema, Data_Solicitação, Resposta
        FROM Suporte
        WHERE Protocolo = %s
        """
        cursor.execute(sql, (Protocolo,))
        resultado = cursor.fetchone()
        if resultado:
            Protocolo, Problema, Data_Solicitação, Resposta = resultado
            print(f"Protocolo: {Protocolo}")
            print(f"Problema: {Problema}")
            print(f"Data da Solicitação: {Data_Solicitação}")
            print(f"Resposta: {Resposta}")
        else:
            print("Suporte não encontrado.")
    except Error as e:
        print(f"Erro ao ler suporte: {e}")
    finally:
        cursor.close()

def atualizar_suporte(con_BD, Protocolo):
    ler_suporte(con_BD, Protocolo)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Problema")
    print("2. Resposta")
    print("3. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_problema = input("Digite o novo problema: ")
            sql = "UPDATE Suporte SET Problema = %s WHERE Protocolo = %s"
            valores = (novo_problema, Protocolo)
            cursor.execute(sql, valores)
        elif escolha == '2':
            nova_resposta = input("Digite a nova resposta: ")
            sql = "UPDATE Suporte SET Resposta = %s WHERE Protocolo = %s"
            valores = (nova_resposta, Protocolo)
            cursor.execute(sql, valores)
        elif escolha == '3':
            print("Saindo da atualização de dados de suporte.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados do suporte atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar suporte: {e}")
    
    finally:
        cursor.close()

def deletar_suporte(con_BD, Protocolo):
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM Suporte
        WHERE Protocolo = %s
        """
        cursor.execute(sql, (Protocolo,))
        con_BD.commit()
        print("Suporte deletado com sucesso.")
    except Error as e:
        print(f"Erro ao deletar suporte: {e}")
    finally:
        cursor.close()

#-----------------------------------------------------------------------------------------------------------------------------
# Códigos Loja
#-----------------------------------------------------------------------------------------------------------------------------

def inserir_loja(con_BD, idLoja, Preço, ID_Jogo):
    try:
        cursor = con_BD.cursor()
        
        sql = """
        INSERT INTO loja (idLoja, Preço, ID_Jogo)
        VALUES (%s, %s, %s)
        """
        valores = (idLoja, Preço, ID_Jogo)
        cursor.execute(sql, valores)
        con_BD.commit()
        print("Loja inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir loja: {e}")
    finally:
        cursor.close()

def ler_loja(con_BD, idLoja):
    try:
        cursor = con_BD.cursor()
        sql = """
        SELECT idLoja, Preço, ID_Jogo
        FROM loja
        WHERE idLoja = %s
        """
        cursor.execute(sql, (idLoja,))
        resultado = cursor.fetchone()  # Obtém o primeiro registro (se houver)
        if resultado:
            # Desempacotando o resultado da consulta
            idLoja, Preço, ID_Jogo = resultado
            print(f"ID Loja: {idLoja}")
            print(f"Preço: {Preço}")
            print(f"ID jogo: {ID_Jogo}")
        else:
            print("Loja não encontrada.")
    except Error as e:
        print(f"Erro ao ler carrinho do usuário: {e}")
    finally:
        cursor.close()


def atualizar_loja(con_BD, idLoja):
    ler_carrinho_de_compras(conexao, idLoja)
    print("\nEscolha o campo que deseja atualizar:")
    print("1. Preço")
    print("2. Sair")
    
    escolha = input("Digite o número da opção desejada: ")
    
    try:
        cursor = con_BD.cursor()
        if escolha == '1':
            novo_preco = input("Digite o novo preço: ")
            sql = "UPDATE loja SET Preço = %s WHERE idLoja = %s"
            valores = (novo_preco, idLoja)
            cursor.execute(sql, valores)
        elif escolha == '2':
            print("Saindo da atualização de dados da loja.")
            return
        else:
            print("Opção inválida.")
            return
        
        con_BD.commit()
        print("Dados da loja atualizados com sucesso.")
    
    except Error as e:
        print(f"Erro ao atualizar dados da loja: {e}")
    
    finally:
        cursor.close()
        
def deletar_loja(con_BD, idLoja): 
    try:
        cursor = con_BD.cursor()
        sql = """
        DELETE FROM loja
        WHERE idLoja = %s
        """
        cursor.execute(sql, (idLoja,))
        con_BD.commit()
        print("Loja deletada com sucesso.")
    except Error as e:
        print(f"Erro ao deletar loja: {e}")
    finally:
        cursor.close()
        
#-----------------------------------------------------------------------------------------------------------------------------
dados_usuario = {
    "idUsuario": "0001",
    "Data_Nascimento": "2000-01-01",
    "Nome": "João da Silva",
    "Data_Cadastro": "2015-03-02",
    "Email": "Joãozin123@gmail.com",
    "Telefone": "61985561228",
    "ID_Biblioteca": 245,
    "ID_Perfil_Usuário": 22,
    "ID_Carrinho_de_Compras": 3405
}


#inserir_perfil_usuario(
#    conexao,
#    idPerfil_Usuário=22,
#    caminho_foto_perfil = r'C:\Users\Kennedy\Pictures\WALLPAPERS\Nova pasta\01.png',
#    Biografia='Bem-vindo',
#    Localização='Brasil'
#)

#inserir_perfil_usuario(
#    conexao,
#    idPerfil_Usuário=25,
#    caminho_foto_perfil = r'C:\Users\Kennedy\Pictures\WALLPAPERS\Nova pasta\download.jpg',
#    Biografia='Best Game',
#    Localização='Brasil'
#)
#inserir_usuario(conexao, **dados_usuario)

#ler_perfil_usuario(conexao, idPerfil_Usuário=25)
#atualizar_perfil_usuario(conexao, 22)
#deletar_perfil_usuario(conexao, 22)

#ler_usuario(conexao, 1)
#atualizar_usuario(conexao, 1)
#deletar_usuario(conexao, 1)

#inserir_carrinho_compras(conexao, 3405, '2024-02-09',2, 58)
#ler_carrinho_de_compras(conexao, 3405)
#atualizar_carrinho(conexao, 3405)
#deletar_carrinho(conexao, 3405)

#inserir_avaliacao(conexao,234,10,'Excelente')
#ler_avaliacao(conexao,234)
#atualizar_avaliacao(conexao,234)
#deletar_avaliacao(conexao,234)

#inserir_biblioteca_jg(conexao, 245, 1, '2024-09-18')
#ler_biblioteca_jg(conexao, 245)
#atualizar_biblioteca_jg(conexao, 245)
#deletar_biblioteca_jg(conexao, 245)

#inserir_desenvolvedor(conexao, 2510, 'FromSoftware', 521744621, 'fromsoftware@gmail.com', 25)
#ler_desenvolvedor(conexao, 2510)
#atualizar_desenvolvedor(conexao, 2510)
#deletar_desenvolvedor(conexao, 2510)

#inserir_jogo(
#    conexao,
#    77,
#    'O que não tem mata, te faz mais forte',
#    'Elden ring',
#    'Souls like',
#    '2022-02-24',
#    r'C:\Users\Kennedy\Pictures\WALLPAPERS\Nova pasta\3.jpg',
#    'INTEL CORE I7-8700K',
#    '16 GB',
#    'GTX 1070 8 GB',
#    '60 GB')
#ler_jogo(conexao, 77)
#atualizar_jogo(conexao, 77)
#deletar_jogo(conexao, 77)

#inserir_pagamento(conexao, 78, 'PIX', 'Concluído', '2024-08-10', 3405)
#ler_pagamento(conexao, 78)
#atualizar_pagamento(conexao, 78)
#deletar_pagamento(conexao, 78)

#inserir_loja(conexao, 58, 'R$220,00', 77)
#ler_loja(conexao, 58)
#atualizar_loja(conexao, 58)
#deletar_loja(conexao, 58)
            
