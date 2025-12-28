# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from motor_loterias import (
    JOGOS,
    carregar_resultados,
    validar_jogo,
    conferir_jogo
)

app = Flask(__name__)
CORS(app)

# ==============================
# ROTAS BÁSICAS
# ==============================
@app.route("/")
def home():
    return "API de Loterias rodando corretamente 🚀"


# ==============================
# RESULTADOS COMPLETOS
# ==============================
@app.route("/resultados/<jogo>")
def resultados(jogo):
    if jogo not in JOGOS:
        return jsonify({"erro": "Jogo inválido"}), 404

    dados = carregar_resultados(jogo)
    return jsonify({
        "jogo": jogo,
        "total": len(dados),
        "resultados": [list(d) for d in dados]
    })


# ==============================
# ÚLTIMO CONCURSO
# ==============================
@app.route("/ultimo/<jogo>")
def ultimo_concurso(jogo):
    if jogo not in JOGOS:
        return jsonify({"erro": "Jogo inválido"}), 404

    dados = carregar_resultados(jogo)
    ultimo = dados[-1]

    return jsonify({
        "jogo": jogo,
        "dezenas": sorted(list(ultimo))
    })


# ==============================
# CONFERIR JOGO
# ==============================
@app.route("/conferir/<jogo>", methods=["POST"])
def conferir(jogo):
    if jogo not in JOGOS:
        return jsonify({"erro": "Jogo inválido"}), 404

    payload = request.get_json()
    dezenas = payload.get("dezenas", [])

    try:
        resultado = conferir_jogo(dezenas, jogo)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ==============================
# START
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
