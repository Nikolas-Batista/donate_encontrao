from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Item, Doacao

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)
db.init_app(app)

@app.before_first_request
def criar_tabelas():
    db.create_all()

@app.route("/itens", methods=["GET"])
def listar_itens():
    itens = Item.query.all()
    return jsonify([
        {"id": i.id, "nome": i.nome, "estoque": i.quantidade_estoque}
        for i in itens
    ])

@app.route("/itens", methods=["POST"])
def adicionar_item():
    data = request.json
    item = Item(nome=data["nome"], quantidade_estoque=data["quantidade"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"mensagem": "Item criado com sucesso"})

@app.route("/doar", methods=["POST"])
def doar():
    data = request.json
    item = Item.query.get(data["item_id"])
    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404

    quantidade = int(data["quantidade"])
    item.quantidade_estoque += quantidade

    doacao = Doacao(item_id=item.id, quantidade=quantidade)
    db.session.add(doacao)
    db.session.commit()
    return jsonify({"mensagem": "Doação registrada com sucesso"})

@app.route("/doacoes", methods=["GET"])
def listar_doacoes():
    doacoes = Doacao.query.order_by(Doacao.data.desc()).all()
    return jsonify([
        {
            "item": d.item.nome,
            "quantidade": d.quantidade,
            "data": d.data.strftime("%d/%m/%Y %H:%M")
        }
        for d in doacoes
    ])

if __name__ == "__main__":
    app.run(debug=True)
