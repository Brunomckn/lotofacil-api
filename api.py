# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# ==============================
# CARREGAR RESULTADOS DA LOTOFÁCIL
# ==============================

def carregar_resultados():
    try:
        df = pd.read_excel("Lotofácil.xlsx")

        # Remove linhas vazias
        df = df.dropna()

        resultados = []

        for _, linha in df.iterrows():
            dezenas = set()

            # Ajuste se suas dezenas estiverem em outras colunas
            for i in range(2, 17):  # colunas das dezenas
                dezenas.add(int(linha[i]))

            resultados.append(dezenas)

        return resultados

    except Exception as e:
        print("Erro ao carregar Excel:", e)
        return []


RESULTADOS = carregar_resultados()


# ==============================
# ROTA PRINCIPAL
# ==============================

@app.route("/")
def home():
    return "API Lotofácil rodando corretamente"


# ==============================
# CONFERIR JOGO
# ==============================

@app.route("/conferir", methods=["POST"])
def conferir():
    dados = request.json
    jogo = set(map(int, dados.get("jogo", [])))

    contagem = {
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0
    }

    for resultado in RESULTADOS:
        acertos = len(jogo & resultado)
        if acertos >= 11:
            contagem[acertos] += 1

    return jsonify(contagem)


# ==============================
# INICIAR SERVIDOR
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

