# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)

# 🔓 CORS GLOBAL (ESSENCIAL NO RENDER)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

# 🔓 GARANTE HEADERS EM TODAS AS RESPOSTAS
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response


# ==============================
# CARREGAR RESULTADOS
# ==============================
def carregar_resultados():
    resultados = []

    with open("resultados_lotofacil.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            dezenas = []
            for i in range(1, 16):
                dezenas.append(int(linha[f"Bola{i}"]))
            resultados.append(set(dezenas))

    return resultados


RESULTADOS = carregar_resultados()


# ==============================
# ROTAS
# ==============================
@app.route("/", methods=["GET"])
def home():
    return "API Lotofácil rodando corretamente"


@app.route("/conferir", methods=["POST"])
def conferir():
    dados = request.get_json()

    jogo = set(map(int, dados["dezenas"]))

    contagem = {"11": 0, "12": 0, "13": 0, "14": 0, "15": 0}

    for resultado in RESULTADOS:
        acertos = len(jogo & resultado)
        if acertos >= 11:
            contagem[str(acertos)] += 1

    return jsonify({
        "total_concursos": len(RESULTADOS),
        "acertos": contagem
    })


@app.route("/historico_jogo", methods=["POST"])
def historico_jogo():
    dados = request.get_json()
    jogo = set(map(int, dados["dezenas"]))

    historico = []

    with open("resultados_lotofacil.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, linha in enumerate(reader):
            dezenas = []
            for i in range(1, 16):
                dezenas.append(int(linha[f"Bola{i}"]))

            resultado = set(dezenas)
            acertos = len(jogo & resultado)

            historico.append({
                "concurso": idx + 1,
                "acertos": acertos,
                "dezenas_sorteadas": dezenas,
                "premios": {
                    "15": linha["Rateio 15 acertos"],
                    "14": linha["Rateio 14 acertos"],
                    "13": linha["Rateio 13 acertos"],
                    "12": linha["Rateio 12 acertos"],
                    "11": linha["Rateio 11 acertos"]
                }
            })

    return jsonify({
        "total": len(historico),
        "historico": historico
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
