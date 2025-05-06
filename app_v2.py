# app.py
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Carrega o modelo
with open('modelo_treinado.pkl', 'rb') as f:
    modelo = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    dados = request.get_json()

    try:
        # Extrair os dados da requisição
        idade = dados['idade']
        renda = dados['renda']
        tempo_emprego = dados['tempo_emprego']
        score_credito = dados['score_credito']

        # Montar o array de entrada
        entrada = np.array([[idade, renda, tempo_emprego, score_credito]])

        # Fazer a predição
        predicao = modelo.predict(entrada)[0]

        # Traduzir o resultado
        if predicao == 0:
            resultado = 'aprovado'
        else:
            resultado = 'reprovado'

        return jsonify({'resultado': resultado})

    except Exception as e:
        return jsonify({'erro': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
