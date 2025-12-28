# -*- coding: utf-8 -*-

import csv

# ==========================
# CONFIGURAÇÕES DOS JOGOS
# ==========================
JOGOS = {
    "lotofacil": {
        "min": 1,
        "max": 25,
        "qtd_jogo": 15,
        "arquivo": "dados/lotofacil.csv",
        "premios": [11, 12, 13, 14, 15]
    },
    "mega_sena": {
        "min": 1,
        "max": 60,
        "qtd_jogo": 6,
        "arquivo": "dados/mega_sena.csv",
        "premios": [4, 5, 6]
    },
    "quina": {
        "min": 1,
        "max": 80,
        "qtd_jogo": 5,
        "arquivo": "dados/quina.csv",
        "premios": [2, 3, 4, 5]
    },
    "lotomania": {
        "min": 0,
        "max": 99,
        "qtd_jogo": 50,
        "arquivo": "dados/lotomania.csv",
        "premios": [0, 15, 16, 17, 18, 19, 20]
    },
    "dupla_sena": {
        "min": 1,
        "max": 50,
        "qtd_jogo": 6,
        "arquivo": "dados/dupla_sena.csv",
        "premios": [3, 4, 5, 6]
    },
    "dia_de_sorte": {
        "min": 1,
        "max": 31,
        "qtd_jogo": 7,
        "arquivo": "dados/dia_de_sorte.csv",
        "premios": [4, 5, 6, 7]
    }
}

# ==========================
# CARREGAR RESULTADOS
# ==========================
def carregar_resultados(jogo):
    config = JOGOS[jogo]
    resultados = []

    with open(config["arquivo"], newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        for linha in reader:
            dezenas = []

            for v in linha:
                try:
                    n = int(v)
                    if config["min"] <= n <= config["max"]:
                        dezenas.append(n)
                except:
                    continue

            if len(dezenas) == config["qtd_jogo"]:
                resultados.append(set(dezenas))

    return resultados


# ==========================
# VALIDAR JOGO DO USUÁRIO
# ==========================
def validar_jogo(jogo, tipo):
    config = JOGOS[tipo]
    jogo = set(jogo)

    if len(jogo) != config["qtd_jogo"]:
        raise ValueError(
            f"O jogo deve ter exatamente {config['qtd_jogo']} dezenas"
        )

    if any(n < config["min"] or n > config["max"] for n in jogo):
        raise ValueError("Dezenas fora do intervalo permitido")

    return jogo


# ==========================
# CONFERIR JOGO
# ==========================
def conferir_jogo(jogo, tipo):
    config = JOGOS[tipo]
    resultados = carregar_resultados(tipo)
    jogo = validar_jogo(jogo, tipo)

    resumo = {str(p): 0 for p in config["premios"]}

    for dezenas in resultados:
        acertos = len(jogo & dezenas)
        if acertos in config["premios"]:
            resumo[str(acertos)] += 1

    return {
        "jogo": tipo,
        "total_concursos": len(resultados),
        "resultado": resumo
    }
