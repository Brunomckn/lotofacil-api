# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

# 🔑 LIBERA CORS PARA QUALQUER ORIGEM (GitHub Pages, etc.)
CORS(app, resources={r"/*": {"origins": "*"}})

# ==============================
# CARREGAR RESULTADOS
# ==============================
def carregar_resultados():
    df = pd.read_excel("Lotofácil.xlsx")
    df = df.dropna()

    resultados = []

    for _, linha in df.iterrows():
        dezenas = set()
        for i in range(2, 17):  # colunas das dezenas
            dezenas.add(int(linha[i]))
        resultados.append(dezenas)

    return resultados


RESULTADOS = carregar_resultados()


@app.route("/", methods=["GET"])
def home():
    return "API Lotofácil rodando corretamente"


@app.route("/conferir", methods=["POST", "OPTIONS"])
def conferir():
    if request.method == "OPTIONS":
        # Resposta correta para preflight
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response, 200

    dados = request.get_json()

    if not dados or "dezenas" not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    jogo = set(map(int, dados["dezenas"]))

    contagem = {11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

    for resultado in RESULTADOS:
        acertos = len(jogo & resultado)
        if acertos >= 11:
            contagem[acertos] += 1

    return jsonify(contagem)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
