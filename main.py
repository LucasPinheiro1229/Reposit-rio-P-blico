import requests
import json
from pathlib import Path

BASE_URL = "https://api.github.com"

# Coloque aqui o seu nome de usuário do GitHub
USERNAME = "LucasPinheiro1229"

# Repositório open-source escolhido para análise
OPEN_SOURCE_OWNER = "numpy"
OPEN_SOURCE_REPO = "numpy"


def buscar_usuario(username):
    url = f"{BASE_URL}/users/{username}"
    resposta = requests.get(url)

    resposta.raise_for_status()
    return resposta.json()


def listar_repositorios(username):
    url = f"{BASE_URL}/users/{username}/repos"
    parametros = {
        "type": "public",
        "per_page": 100
    }

    resposta = requests.get(url, params=parametros)
    resposta.raise_for_status()

    return resposta.json()


def calcular_estrelas(repositorios):
    return sum(repo["stargazers_count"] for repo in repositorios)


def analisar_repositorio(owner, repo):
    # Informações principais
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    resposta = requests.get(url)
    resposta.raise_for_status()

    dados = resposta.json()

    # Linguagens
    url_linguagens = f"{BASE_URL}/repos/{owner}/{repo}/languages"
    resposta_linguagens = requests.get(url_linguagens)
    resposta_linguagens.raise_for_status()

    linguagens = resposta_linguagens.json()

    return {
        "nome": dados["name"],
        "proprietario": dados["owner"]["login"],
        "descricao": dados["description"],
        "estrelas": dados["stargazers_count"],
        "forks": dados["forks_count"],
        "issues_abertas": dados["open_issues_count"],
        "linguagens": list(linguagens.keys()),
        "url": dados["html_url"]
    }


def criar_dataset(repositorios):
    dataset = []

    for repo in repositorios:
        dataset.append({
            "nome": repo["name"],
            "proprietario": repo["owner"]["login"],
            "estrelas": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "linguagens": []
        })

    return dataset


def gerar_estatisticas(dataset):
    if not dataset:
        return {
            "total_repositorios": 0,
            "total_estrelas": 0,
            "media_estrelas": 0,
            "total_forks": 0
        }

    total_repositorios = len(dataset)
    total_estrelas = sum(repo["estrelas"] for repo in dataset)
    total_forks = sum(repo["forks"] for repo in dataset)

    media_estrelas = total_estrelas / total_repositorios

    return {
        "total_repositorios": total_repositorios,
        "total_estrelas": total_estrelas,
        "media_estrelas": round(media_estrelas, 2),
        "total_forks": total_forks
    }


def salvar_json(dados, nome_arquivo):
    pasta = Path("data")
    pasta.mkdir(exist_ok=True)

    caminho = pasta / nome_arquivo

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nArquivo salvo em: {caminho}")


def main():
    print("=" * 50)
    print("EXERCÍCIO - API DO GITHUB")
    print("=" * 50)

    # -----------------------------------------
    # 1. EXPLORAR SUA CONTA
    # -----------------------------------------

    print("\n[1] Informações do usuário")

    usuario = buscar_usuario(USERNAME)

    print(f"Usuário: {usuario['login']}")
    print(f"Nome: {usuario['name']}")
    print(f"Seguidores: {usuario['followers']}")
    print(f"Seguindo: {usuario['following']}")
    print(f"Repositórios públicos: {usuario['public_repos']}")

    repositorios = listar_repositorios(USERNAME)

    total_estrelas = calcular_estrelas(repositorios)

    print(f"Total de repositórios encontrados: {len(repositorios)}")
    print(f"Total de estrelas: {total_estrelas}")

    print("\nRepositórios:")

    for repo in repositorios:
        print(
            f"- {repo['name']} "
            f"| ⭐ {repo['stargazers_count']} "
            f"| 🍴 {repo['forks_count']}"
        )

    # -----------------------------------------
    # 2. ANALISAR PROJETO OPEN-SOURCE
    # -----------------------------------------

    print("\n[2] Análise do projeto open-source")

    projeto = analisar_repositorio(
        OPEN_SOURCE_OWNER,
        OPEN_SOURCE_REPO
    )

    print(f"Projeto: {projeto['nome']}")
    print(f"Proprietário: {projeto['proprietario']}")
    print(f"Estrelas: {projeto['estrelas']}")
    print(f"Forks: {projeto['forks']}")
    print(f"Issues abertas: {projeto['issues_abertas']}")

    print("Linguagens:")

    for linguagem in projeto["linguagens"]:
        print(f"- {linguagem}")

    # -----------------------------------------
    # 3. CRIAR DATASET
    # -----------------------------------------

    print("\n[3] Criando dataset")

    dataset = criar_dataset(repositorios)

    estatisticas = gerar_estatisticas(dataset)

    resultado = {
        "usuario": USERNAME,
        "repositorios": dataset,
        "estatisticas": estatisticas
    }

    salvar_json(resultado, "repositorios.json")

    print("\nEstatísticas:")
    print(f"Total de repositórios: {estatisticas['total_repositorios']}")
    print(f"Total de estrelas: {estatisticas['total_estrelas']}")
    print(f"Média de estrelas: {estatisticas['media_estrelas']}")
    print(f"Total de forks: {estatisticas['total_forks']}")

    print("\n✅ Exercício concluído!")


if __name__ == "__main__":
    main()
