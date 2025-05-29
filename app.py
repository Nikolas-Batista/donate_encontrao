from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que seu site (HTML) fale com o Python

# Estoque guardado na memória
estoque = {
    "Banana": 10,
    "Maçã": 5,
    "Arroz": 20
}

@app.route("/estoque", methods=["GET"])
def ver_estoque():
    return jsonify(estoque)

@app.route("/doacao", methods=["POST"])
def registrar_doacao():
    data = request.json
    item = data.get("item")
    quantidade = int(data.get("quantidade", 0))

    if item not in estoque:
        return jsonify({"erro": "Item não encontrado"}), 400

    estoque[item] += quantidade
    return jsonify({"mensagem": "Doação registrada com sucesso", "novo_estoque": estoque[item]})

if __name__ == "__main__":
    app.run(debug=True)


