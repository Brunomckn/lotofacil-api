# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

# ==============================
# CONFIG
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

MAPA_ARQUIVOS = {
    "lotofacil": "lotofacil.csv",
    "megasena": "mega_sena.csv",
    "quina": "quina.csv",
    "lotomania": "lotomania.csv",
    "duplasena": "dupla_sena.csv",
    "diadesorte": "dia_de_sorte.csv"
}

# ==============================
# FUNÇÕES AUXILIARES
# ==============================
def carregar_csv(jogo):
    arquivo = MAPA_ARQUIVOS.get(jogo)
    if not arquivo:
        return None

    caminho = os.path.join(DADOS_DIR, arquivo)
    resultados = []

    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            dezenas = []

            for k, v in linha.items():
                if "Bola" in k or k.lower().startswith("dezena"):
                    if v and v.isdigit():
                        dezenas.append(int(v))

            resultados.append({
                "concurso": linha.get("Concurso"),
                "data": linha.get("Data"),
                "dezenas": dezenas,
                "premios": linha
            })

    return resultados


# ==============================
# ROTAS
# ==============================

@app.route("/")
def home():
    return "API de Loterias rodando corretamente 🚀"


# 🔹 RESULTADOS COMPLETOS
@app.route("/resultados/<jogo>")
def resultados(jogo):
    dados = carregar_csv(jogo)
    if not dados:
        return jsonify({"erro": "Jogo inválido"}), 404
    return jsonify(dados)


# 🔹 ÚLTIMO CONCURSO
@app.route("/ultimo/<jogo>")
def ultimo_concurso(jogo):
    dados = carregar_csv(jogo)
    if not dados:
        return jsonify({"erro": "Jogo inválido"}), 404
    return jsonify(dados[-1])


# 🔹 PREMIAÇÃO DO ÚLTIMO
@app.route("/premiacao/<jogo>")
def premiacao(jogo):
    dados = carregar_csv(jogo)
    if not dados:
        return jsonify({"erro": "Jogo inválido"}), 404

    ultimo = dados[-1]
    premios = {}

    for k, v in ultimo["premios"].items():
        if "acertos" in k.lower():
            premios[k] = v

    return jsonify({
        "concurso": ultimo["concurso"],
        "data": ultimo["data"],
        "premiacao": premios
    })


# 🔹 CONFERIR JOGO
@app.route("/conferir/<jogo>", methods=["POST"])
def conferir_jogo(jogo):
    dados = carregar_csv(jogo)
    if not dados:
        return jsonify({"erro": "Jogo inválido"}), 404

    payload = request.get_json()
    dezenas_usuario = set(payload.get("dezenas", []))

    resultado = {
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0
    }

    for concurso in dados:
        acertos = len(dezenas_usuario & set(concurso["dezenas"]))
        if str(acertos) in resultado:
            resultado[str(acertos)] += 1

    return jsonify({
        "total_concursos": len(dados),
        "resultado": resultado
    })


# ==============================
# START
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
