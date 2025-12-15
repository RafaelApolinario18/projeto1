#Início do Projeto - Cinema 
try:
    from tkinter import messagebox #Inportando biblioteca gráfica
except Exception:
    # Dummy messagebox if tkinter is not available
    class _DummyMessageBox:
        @staticmethod
        def showinfo(*a, **k):
            return None
    messagebox = _DummyMessageBox()
import sqlite3 #conectando o banco de dados


#criando a classe do sistema de cinema:
class sistema_cinema:
    def __init__(self):
        self.conexao = sqlite3.connect("banco.db")
        self.cursor = self.conexao.cursor() #cursor serve para executar comandos no banco de dados
        self.createtable_usuarios()
        self.createtable_filmes() #self é usado para referenciar a própria classe
        self.usuario_id = None
#definindo os métodos da classe sistema_cinema:
    def createtable_usuarios(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL UNIQUE
)
""")
    # A tabela `filmes` é criada pela definição abaixo (com `usuario_id` FK).
    def inserir_dados(self, nome, email):
        self.cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        # armazena o usuário logado (id da última inserção)
        try:
            self.usuario_id = self.cursor.lastrowid
        except Exception:
            self.usuario_id = None
        self.conexao.commit() #commit serve para salvar as alterações no banco de dados
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    
    def buscar_usuario(self, busca):
        self.cursor.execute("SELECT * FROM usuarios WHERE email = ?", (busca,))
        usuario = self.cursor.fetchone()
        return usuario

    def remover_usuario(self, email):
        # Remove usuário pelo email
        self.cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
        self.conexao.commit()
        messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")

    def atualizar_usuario(self, email):
        # Atualiza um usuário identificado pelo email
        usuario = self.buscar_usuario(email)
        if not usuario:
            messagebox.showinfo("Erro", "Usuário não encontrado.")
            return
        print("Qual dado você deseja atualizar?\n1 - Nome\n2 - Email")
        try:
            opcao = int(input(" "))
        except ValueError:
            print("Opção inválida.")
            return
        if opcao == 1:
            novo_nome = input("Digite o novo nome do usuário: ")
            self.cursor.execute("UPDATE usuarios SET nome = ? WHERE email = ?", (novo_nome, email))
        elif opcao == 2:
            novo_email = input("Digite o novo email do usuário: ")
            self.cursor.execute("UPDATE usuarios SET email = ? WHERE email = ?", (novo_email, email))
        else:
            print("Opção inválida.")
            return
        self.conexao.commit()
        messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")

    #CAMPO DA TABELA FILMES

    def createtable_filmes(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            diretor TEXT NOT NULL,
            genero TEXT NOT NULL,
            avaliacao TEXT,
            arquivo TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)               
            )
            """)
    def inserir_dados_filmes(self, titulo, diretor, genero, avaliacao, arquivo, usuario_id=None):
        # utiliza usuario_id passado ou o usuário logado (`self.usuario_id`)
        if usuario_id is None:
            usuario_id = self.usuario_id
        if usuario_id is None:
            raise ValueError("Nenhum usuário especificado para cadastrar o filme")
        self.cursor.execute(
            "INSERT INTO filmes (titulo, diretor, genero, avaliacao, arquivo, usuario_id) VALUES (?, ?, ?, ?, ?, ?)",
            (titulo, diretor, genero, avaliacao, arquivo, usuario_id)
        )
        self.conexao.commit()
        messagebox.showinfo("Sucesso", "Filme cadastrado com sucesso!")
        
    def listar_filmes(self, usuario_id=None):
        if usuario_id is None:
            usuario_id = self.usuario_id
        if usuario_id is None:
            return []
        self.cursor.execute("SELECT * FROM filmes WHERE usuario_id = ?", (usuario_id,))
        filmes = self.cursor.fetchall()
        return filmes
    def procurar_filme(self, titulo_procurado, usuario_id=None):
        if usuario_id is None:
            usuario_id = self.usuario_id
        self.cursor.execute("SELECT * FROM filmes WHERE titulo = ? AND usuario_id = ?", (titulo_procurado, usuario_id))
        filme = self.cursor.fetchone()
        if filme:
            id, titulo, diretor, genero, avaliacao, arquivo, usuario_id = filme
            return filme
        else:
            print("Filme não encontrado.")
            return None
    
    def remover_filme(self, titulo_procurado, usuario_id=None):
        if usuario_id is None:
            usuario_id = self.usuario_id
        self.cursor.execute("DELETE FROM filmes WHERE titulo = ? AND usuario_id = ?", (titulo_procurado, usuario_id))
        if self.cursor.rowcount == 0:
            messagebox.showinfo("Erro", "Filme não encontrado ou você não tem permissão para removê-lo.")
            return
        else:
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Filme removido com sucesso!")

    def receber_recomendacoes(self, tipo=None):
        """Se `tipo` for fornecido (1..5), retorna uma lista de títulos.
        Se `tipo` for None, executa o modo interativo (chama `pegandodadosdaweb.main()`)
        """

        if tipo is None:
            # Modo interativo: chamar o main do módulo externo
            import pegandodadosdaweb
            pegandodadosdaweb.main()
            return None

        # Tipo fornecido: obter a lista a partir do módulo externo; propagate errors
        import pegandodadosdaweb
        mapping = {
            1: pegandodadosdaweb.get_best_movies_scraping,
            2: pegandodadosdaweb.get_indie_movies_scraping,
            3: pegandodadosdaweb.get_action_movies_scraping,
            4: pegandodadosdaweb.get_national_movies_scraping,
            5: pegandodadosdaweb.get_animation_movies_scraping,
        }
        func = mapping.get(int(tipo))
        if func is None:
            raise ValueError("Tipo inválido")
        return func()


def main():
     #tela inicial:
    print("Iniciando o Sistema de Cinema...")
    sistema = sistema_cinema()

    # Login / cadastro inicial
    while True:
        login = input("Você já possui um cadastro? (S/N): ")
        if login.upper() in {"S", "N"}:
            break
        print("Entrada inválida. Por favor, digite S para sim ou N para não.")

    if login.upper() == 'N':
        nome = input("Digite o nome do usuário: ")
        email = input("Digite o email do usuário: ")
        sistema.inserir_dados(nome, email)
        # `inserir_dados` atribui `sistema.usuario_id`
    else:
        email = input("Digite o email do usuário: ")
        usuario = sistema.buscar_usuario(email)
        if usuario:
            sistema.usuario_id = usuario[0]
            print(f"Bem-vindo de volta, {usuario[1]}!")
        else:
            print("Usuário não encontrado. Por favor, verifique o email e tente novamente.")
            return

    # menu principal
    menu_ = """
Escolha uma das opções abaixo:
1 - Cadastrar Novo Usuário
2 - Remover Usuário
3 - Atualizar Usuário
4 - Cadastrar Filme
5 - Listar Filmes
6 - Procurar Filme
7 - Remover Filme
8 - Enviar lista de filmes por email
9 - Receber recomendações de filmes
10 - Sair"""

    while True:
        print(menu_)
        try:
            opcao = int(input("Digite a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Digite um número entre 1 e 10.")
            continue
        except (StopIteration, EOFError):
            # Permitir saída limpa quando as entradas se esgotarem (os testes fornecem entradas finitas).
            return

        if opcao == 1:
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o email do usuário: ")
            sistema.inserir_dados(nome, email)
        elif opcao == 2:
            busca = input('Digite o email que deseja buscar: ')
            sistema.remover_usuario(busca)
        elif opcao == 3:
            email = input('Digite o email que deseja buscar: ')
            sistema.atualizar_usuario(email)
        elif opcao == 4:
            titulo = input("Digite o título do filme: ")
            diretor = input("Digite o diretor do filme: ") 
            genero = input("Digite o gênero do filme: ")
            avaliacao = input("Digite a avaliação do filme (ou deixe em branco se não quiser avaliar): ")
            arquivo = input("Digite o nome do arquivo do filme: ")
            sistema.inserir_dados_filmes(titulo, diretor, genero, avaliacao, arquivo)
        elif opcao == 5:
            filmes = sistema.listar_filmes()
            for filme in filmes:
                print(filme)
        elif opcao == 6:
            titulo_procurado = input("Digite o título do filme que deseja procurar: ")
            filme_encontrado = sistema.procurar_filme(titulo_procurado)
            if filme_encontrado:
                print(filme_encontrado)
        elif opcao == 7:
            titulo_procurado = input("Digite o título do filme que deseja remover: ")
            sistema.remover_filme(titulo_procurado)
        elif opcao == 8:
            print("Funcionalidade de envio de email ainda não implementada.")
        elif opcao == 9:
            print("Escolha o tipo de recomendação que deseja:\n1 - Melhores Filmes de Todos os Tempos\n2 - Melhores Filmes Indie\n3 - Melhores Filmes de Ação\n4 - Melhores Filmes Nacionais\n5 - Melhores Filmes de Animação")
            try:
                tipo = int(input("Digite o número da sua escolha: "))
            except ValueError:
                print("Opção inválida. Voltando ao menu.")
                continue

            try:
                recomendacoes = sistema.receber_recomendacoes(tipo)
            except ModuleNotFoundError:
                print("Dependência ausente: instale 'requests' e 'beautifulsoup4' para obter recomendações online.")
                continue
            except Exception as e:
                print("Erro ao obter recomendações:", e)
                continue

            # exibe recomendações
            if not recomendacoes:
                print("Nenhuma recomendação encontrada.")
            else:
                print("Recomendações:")
                for title in recomendacoes:
                    print(title)

                # pergunta se deseja salvar
                save = input("Deseja salvar as recomendações em um arquivo? (S/N): ")
                if save.upper() == 'S':
                    default = f"recomendacoes_tipo{tipo}.txt"
                    filename = input(f"Digite o nome do arquivo (Enter para '{default}'): ").strip()
                    if not filename:
                        filename = default
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            for line in recomendacoes:
                                f.write(line + "\n")
                        print(f"Recomendações salvas em {filename}")
                    except Exception as e:
                        print("Erro ao salvar arquivo:", e)
        elif opcao == 10:
            break
        else:
            print("Opção inválida. Digite um número entre 1 e 10.")

if __name__ == '__main__':
    main()