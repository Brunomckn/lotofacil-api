# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)

# 🔓 LIBERA CORS PARA QUALQUER SITE (GitHub Pages, etc.)
CORS(app, resources={r"/*": {"origins": "*"}})

# ==============================
# CARREGAR RESULTADOS DA LOTOFÁCIL (CSV)
# ==============================
def carregar_resultados():
    resultados = []

    caminho = "resultados_lotofacil.csv"

    if not os.path.exists(caminho):
        print("❌ Arquivo CSV não encontrado:", caminho)
        return resultados

    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for linha in reader:
            dezenas = []

            for chave, valor in linha.items():
                if chave.lower().startswith("d"):
                    try:
                        dezenas.append(int(valor))
                    except:
                        pass

            if len(dezenas) == 15:
                resultados.append(set(dezenas))

    print(f"✅ {len(resultados)} concursos carregados")
    return resultados


RESULTADOS = carregar_resultados()

# ==============================
# ROTAS
# ==============================

@app.route("/", methods=["GET"])
def home():
    return "API Lotofácil rodando corretamente"


@app.route("/conferir", methods=["POST", "OPTIONS"])
def conferir():
    # Resposta ao preflight (CORS)
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    dados = request.get_json()

    if not dados or "dezenas" not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    try:
        jogo = set(map(int, dados["dezenas"]))
    except:
        return jsonify({"erro": "Formato inválido"}), 400

    contagem = {
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0
    }

    for resultado in RESULTADOS:
        acertos = len(jogo & resultado)
        if acertos >= 11:
            contagem[str(acertos)] += 1

    return jsonify(contagem)


# ==============================
# INICIAR SERVIDOR
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
