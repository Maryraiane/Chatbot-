import requests
import urllib.parse
import ast
import operator as op
from datetime import datetime


def obter_hora():
    agora = datetime.now()
    return agora.strftime("Agora são %H:%M do dia %d/%m/%Y")

def buscar_wikipedia(query):
    try:
        # 🔥 Corrige capitalização
        query = query.strip().capitalize()

        query_formatada = urllib.parse.quote(query)

        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{query_formatada}"
        r = requests.get(url, timeout=5)

        if r.status_code == 200:
            data = r.json()

            texto = data.get("extract")

            # evita páginas ruins/desambiguação
            if texto and "pode referir-se a:" not in texto.lower():
                return texto

        return None

    except:
        return None

def buscar_ddg(query):
    try:
        url = "https://api.duckduckgo.com/"

        params = {
            "q": query,
            "format": "json",
            "kl": "br-pt",
            "no_redirect": 1,
            "no_html": 1,
            "skip_disambig": 1
        }

        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        if data.get("AbstractText"):
            return data["AbstractText"]

        if data.get("Answer"):
            return data["Answer"]

        if data.get("RelatedTopics"):
            for item in data["RelatedTopics"]:
                if isinstance(item, dict) and item.get("Text"):
                    return item["Text"]

        return None

    except:
        return None

def buscar(query):
    # 🟢 tentativa 1
    resultado = buscar_wikipedia(query)
    if resultado:
        return resultado

    # 🟢 tentativa 2 (Title Case)
    resultado = buscar_wikipedia(query.title())
    if resultado:
        return resultado

    # 🟡 fallback
    resultado = buscar_ddg(query)
    if resultado:
        return resultado

    return None


def limpar_query(texto):
    texto = texto.lower().strip()

    comandos = [
        "pesquisar", "pesquise", "buscar", "procurar",
        "me fale sobre", "fale sobre", "explique",
        "o que é", "o que e", "encontre", "mostre",
        "traga informações sobre"
    ]

    stopwords = ["o", "a", "os", "as", "do", "da", "dos", "das", "de", "sobre"]

    # remove comandos do início
    for cmd in comandos:
        if texto.startswith(cmd):
            texto = texto.replace(cmd, "", 1).strip()

    # remove palavras inúteis
    palavras = texto.split()
    palavras_filtradas = [p for p in palavras if p not in stopwords]

    return " ".join(palavras_filtradas)


OPERADORES = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow
}

def calcular(expressao):
    try:
        node = ast.parse(expressao, mode='eval').body

        def _eval(n):
            if isinstance(n, ast.Constant):
                return n.value
            elif isinstance(n, ast.BinOp):
                return OPERADORES[type(n.op)](_eval(n.left), _eval(n.right))
            elif isinstance(n, ast.UnaryOp):
                return -_eval(n.operand)
            else:
                raise ValueError

        return _eval(node)

    except:
        return None



def responder(mensagem, historico):
    mensagem = mensagem.lower().strip()

    # ⏰ hora
    if "que horas" in mensagem or "hora agora" in mensagem:
        return obter_hora()

    # 👤 memória
    if mensagem.startswith("meu nome é"):
        nome = mensagem.replace("meu nome é", "").strip()
        return f"Prazer, {nome}! 😊 Vou lembrar disso."

    if "qual meu nome" in mensagem:
        for h in historico:
            if "meu nome é" in h.mensagem.lower():
                nome = h.mensagem.lower().split("meu nome é")[1].strip()
                return f"Seu nome é {nome} 😊"
        return "Ainda não sei seu nome 😅"


    if any(op in mensagem for op in ["+", "-", "*", "/", "**"]):
        resultado = calcular(mensagem)
        if resultado is not None:
            return f"O resultado é {resultado} 😊"
        return "Não consegui calcular isso 😅"


    if any(p in mensagem for p in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]):
        return "Olá! 😊 Como posso te ajudar?"


    query = limpar_query(mensagem)

    resultado = buscar(query)

    if resultado:
        return resultado


    resultado = buscar(mensagem)
    if resultado:
        return resultado

    return "Desculpe 😊 não encontrei informações claras."