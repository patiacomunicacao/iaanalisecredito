from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Carregar artefatos
modelo = joblib.load('modelo_credito_refinado.pkl')
scaler_idade = joblib.load('scaler_idade.pkl')
colunas_modelo = joblib.load('colunas_modelo.pkl')

# Nome do arquivo de histórico
HISTORICO_PATH = 'historico_analises.xlsx'

# Função para preparar entrada
def preparar_input(data):
    # Normalizar idade
    idade_df = pd.DataFrame([[data['idade']]], columns=['idade'])
    idade_norm = scaler_idade.transform(idade_df)[0][0]

    # OneHotEncoding manual da região
    regioes = ['regiao_Norte', 'regiao_Nordeste', 'regiao_Sudeste', 'regiao_Sul', 'regiao_Centro-Oeste']
    regiao_data = {col: 0 for col in regioes}
    regiao_col = f"regiao_{data['regiao']}"
    if regiao_col in regiao_data:
        regiao_data[regiao_col] = 1

    # Montar DataFrame de entrada
    entrada = pd.DataFrame([{
        'renda_mensal': data['renda_mensal'],
        'score_credito': data['score_credito'],
        'restricoes_spc': data['restricoes_spc'],
        'inadimplencia_3anos': data['inadimplencia_3anos'],
        'percentual_entrada': data['percentual_entrada'],
        'prazo_anos': data['prazo_anos'],
        'idade_norm': idade_norm,
        **regiao_data
    }])

    return entrada

# Rota de análise de crédito
@app.route('/analisar_credito', methods=['POST'])
def analisar_credito():
    data = request.get_json()

    # Validar campos obrigatórios
    required_fields = ['renda_mensal', 'score_credito', 'restricoes_spc',
                       'inadimplencia_3anos', 'percentual_entrada', 'prazo_anos',
                       'idade', 'regiao']
    if not all(field in data for field in required_fields):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    # Preparar input para predição
    entrada = preparar_input(data)
    entrada = entrada.reindex(columns=colunas_modelo, fill_value=0)

    # Fazer a predição
    proba = modelo.predict_proba(entrada)[0][1]
    status = modelo.predict(entrada)[0]

    resultado = 'Aprovado' if status == 1 else 'Reprovado'
    justificativa = f"Probabilidade de inadimplência estimada em {round((1 - proba) * 100, 1)}%"

    # Responder para o usuário
    resposta = {
        'resultado': resultado,
        'score_probabilidade': round(proba, 3),
        'justificativa': justificativa
    }

    # ------------------------
    # Salvamento no histórico
    # ------------------------
    registro = {
        'renda_mensal': data['renda_mensal'],
        'score_credito': data['score_credito'],
        'restricoes_spc': data['restricoes_spc'],
        'inadimplencia_3anos': data['inadimplencia_3anos'],
        'percentual_entrada': data['percentual_entrada'],
        'prazo_anos': data['prazo_anos'],
        'idade': data['idade'],
        'regiao': data['regiao'],
        'resultado': resultado,
        'score_probabilidade': round(proba, 3)
    }

    novo_registro_df = pd.DataFrame([registro])

    # Se arquivo existir, carregar e concatenar
    if os.path.exists(HISTORICO_PATH):
        historico_df = pd.read_excel(HISTORICO_PATH)
        historico_df = pd.concat([historico_df, novo_registro_df], ignore_index=True)
    else:
        historico_df = novo_registro_df

    # Salvar atualizado
    historico_df.to_excel(HISTORICO_PATH, index=False)

    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
