# -*- coding: utf-8 -*-
import csv
import os

# ==============================
# CONFIGURAÇÃO DAS LOTERIAS
# ==============================
LOTOS = {
    "lotofacil": {
        "min": 1,
        "max": 25,
        "quantidade": 15,
        "arquivo": "lotofacil.csv"
    },
    "megasena": {
        "min": 1,
        "max": 60,
        "quantidade": 6,
        "arquivo": "megasena.csv"
    },
    "quina": {
        "min": 1,
        "max": 80,
        "quantidade": 5,
        "arquivo": "quina.csv"
    },
    "lotomania": {
        "min": 0,
        "max": 99,
        "quantidade": 50,
        "arquivo": "lotomania.csv"
    },
    "duplasena": {
        "min": 1,
        "max": 50,
        "quantidade": 6,
        "arquivo": "duplasena.csv"
    },
    "diadesorte": {
        "min": 1,
        "max": 31,
        "quantidade": 7,
        "arquivo": "diadesorte.csv"
    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

# ==============================
# CARREGAR RESULTADOS
# ==============================
def carregar_resultados(jogo):
    if jogo not in LOTOS:
        raise ValueError("Loteria inválida")

    caminho = os.path.join(DADOS_DIR, LOTOS[jogo]["arquivo"])
    resultados = []

    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            dezenas = []

            for k, v in linha.items():
                if v and v.isdigit():
                    n = int(v)
                    if LOTOS[jogo]["min"] <= n <= LOTOS[jogo]["max"]:
                        dezenas.append(n)

            if len(dezenas) >= LOTOS[jogo]["quantidade"]:
                resultados.append({
                    "concurso": linha.get("Concurso"),
                    "data": linha.get("Data"),
                    "dezenas": set(dezenas[:LOTOS[jogo]["quantidade"]]),
                    "raw": linha
                })

    return resultados

# ==============================
# VALIDAR JOGO DO USUÁRIO
# ==============================
def validar_jogo(jogo, tipo):
    jogo = set(jogo)
    regras = LOTOS[tipo]

    if len(jogo) != regras["quantidade"]:
        raise ValueError(f"Selecione exatamente {regras['quantidade']} dezenas")

    for n in jogo:
        if n < regras["min"] or n > regras["max"]:
            raise ValueError("Dezenas inválidas")

    return jogo

# ==============================
# CONFERIR JOGO
# ==============================
def conferir_jogo(jogo_usuario, resultados):
    resumo = {}

    for concurso in resultados:
        acertos = len(jogo_usuario & concurso["dezenas"])
        resumo[acertos] = resumo.get(acertos, 0) + 1

    return resumo

# ==============================
# ESTATÍSTICAS BÁSICAS
# ==============================
def estatisticas(resultados):
    freq = {}

    for concurso in resultados:
        for n in concurso["dezenas"]:
            freq[n] = freq.get(n, 0) + 1

    return freq
