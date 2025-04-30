from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Carregar modelo treinado
with open("modelo_credito.pkl", "rb") as f:
    modelo = pickle.load(f)

# Função para preparar os dados
def preparar_dados(dados):
    df = pd.DataFrame([dados])

    # Mapear variáveis categóricas conforme usadas no treino
    map_estado_civil = {"Solteiro": 2, "Casado": 0, "Divorciado": 1}
    map_regiao = {"Norte": 3, "Nordeste": 2, "Sul": 4, "Sudeste": 1, "Centro-Oeste": 0}
    map_tipo_imovel = {"Casa": 0, "Apartamento": 1, "Terreno": 2}

    df["estado_civil"] = df["estado_civil"].map(map_estado_civil)
    df["regiao"] = df["regiao"].map(map_regiao)
    df["tipo_imovel"] = df["tipo_imovel"].map(map_tipo_imovel)

    return df

@app.route("/analisar_credito", methods=["POST"])
def analisar_credito():
    dados = request.get_json()
    df = preparar_dados(dados)
    pred = modelo.predict(df)[0]
    status = "Aprovado" if pred == 1 else "Reprovado"
    return jsonify({
        "status": status,
        "modelo": True
    })

if __name__ == "__main__":
    app.run(debug=True)
