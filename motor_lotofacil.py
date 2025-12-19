# -*- coding: utf-8 -*-

import pandas as pd


def carregar_resultados_excel(caminho_excel):
    """
    Lê o Excel da Lotofácil e retorna
    uma lista de sets com as dezenas de cada concurso
    """
    df = pd.read_excel(caminho_excel)

    resultados = []

    for _, linha in df.iterrows():
        dezenas = []

        for valor in linha.values:
            if isinstance(valor, (int, float)) and 1 <= int(valor) <= 25:
                dezenas.append(int(valor))

        if len(dezenas) == 15:
            resultados.append(set(dezenas))

    return resultados


def validar_jogo(jogo):
    jogo = set(jogo)

    if len(jogo) != 15:
        raise ValueError("Selecione exatamente 15 dezenas")

    if any(n < 1 or n > 25 for n in jogo):
        raise ValueError("Dezenas inválidas")

    return jogo


def conferir_jogo(jogo, resultados):
    resumo = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

    for dezenas in resultados:
        acertos = len(jogo & dezenas)
        if acertos >= 11:
            resumo[acertos] += 1

    return resumo
