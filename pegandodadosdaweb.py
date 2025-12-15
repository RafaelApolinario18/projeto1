from bs4 import BeautifulSoup
import requests

def get_best_movies_scraping():
    dados = requests.get("https://filmow.com/listas/os-melhores-filmes-de-todos-os-tempos-l19453/")
    pagina = BeautifulSoup(dados.content, 'html.parser')
    filmes = pagina.find_all('span', class_="title")
    lista_titulo=[]
    for titulo in filmes:
        lista_titulo.append(titulo.text)
    lista_titulo= lista_titulo[:10]
    return lista_titulo

def get_indie_movies_scraping():
    dados = requests.get("https://cinema10.com.br/generos/filmes-independentes")
    pagina = BeautifulSoup(dados.content, 'html.parser')
    filmes = pagina.find_all('span', class_="movie-name")
    lista_titulo=[]
    for titulo in filmes:
        lista_titulo.append(titulo.text)
    return lista_titulo[:10]

def get_action_movies_scraping():
    dados = requests.get("https://filmow.com/listas/100-melhores-filmes-de-acao-l221999/")
    pagina = BeautifulSoup(dados.content, 'html.parser')
    filmes = pagina.find_all('span', class_="title")
    lista_titulo=[]
    for titulo in filmes:
        lista_titulo.append(titulo.text)
    return lista_titulo[:10]

def get_national_movies_scraping():
    dados = requests.get("https://filmow.com/listas/top-30-melhores-filmes-nacionais-l212172/")
    pagina = BeautifulSoup(dados.content, 'html.parser')
    filmes = pagina.find_all('span', class_="title")
    lista_titulo=[]
    for titulo in filmes:
        lista_titulo.append(titulo.text)
    return lista_titulo

def get_animation_movies_scraping():
    dados = requests.get("https://filmow.com/listas/top-150-filmes-de-animacao-japonesa-l24901/")
    pagina = BeautifulSoup(dados.content, 'html.parser')
    filmes = pagina.find_all('span', class_="title")
    lista_titulo=[]
    for titulo in filmes:
        lista_titulo.append(titulo.text)
    return lista_titulo[:30]
def main():
    confirmacao=input("Se desejar recomendações de filmes, confirme (S/N): ")

    while confirmacao.upper() not in ('S', 'N'):
        confirmacao=input("Entrada inválida. Por favor, digite S para sim ou N para não: ")

    if confirmacao.upper() == 'S':
        print("Escolha o tipo de recomendação que deseja:\n1 - Melhores Filmes de Todos os Tempos\n2 - Melhores Filmes Indie\n3 - Melhores Filmes de Ação\n4 - Melhores Filmes Nacionais\n5 - Melhores Filmes de Animação")

    while confirmacao.upper() == 'S':
        try:
            opcao = int(input("Digite o número da sua escolha: "))
        except ValueError:
            print("Opção inválida. Por favor, escolha um número entre 1 e 5.")
            continue

        if opcao == 1:
            print("Top 10 Melhores Filmes de Todos os Tempos:")
            for title in get_best_movies_scraping():
                print(title)
        elif opcao == 2:
            print("Top 10 Filmes Indie:")
            for title in get_indie_movies_scraping():
                print(title)
        elif opcao == 3:
            print("Top 10 Filmes de Ação:")
            for title in get_action_movies_scraping():
                print(title)
        elif opcao == 4:
            print('30 Títulos dos Melhores Filmes Nacionais:')
            for title in get_national_movies_scraping():
                print(title)
        elif opcao == 5:
            print("30 Melhores Filmes de Animação:")
            for title in get_animation_movies_scraping():
                print(title)
        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 5.")

        confirmacao=input("Se ainda desejar recomendações de filmes, confirme (S/N): ")


if __name__ == '__main__':
    main()