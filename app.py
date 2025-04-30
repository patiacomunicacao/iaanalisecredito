
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def analisar_credito(dados):
    score_credito = dados.get('score_credito')
    restricao_nome = dados.get('restricao_nome')
    inadimplencias_3_anos = dados.get('inadimplencias_3_anos')
    percentual_entrada = dados.get('percentual_entrada')
    prazo_solicitado_anos = dados.get('prazo_solicitado_anos')
    renda_mensal = dados.get('renda_mensal')
    renda_complementar = dados.get('renda_complementar')
    valor_financiamento = dados.get('valor_financiamento')

    entrada = valor_financiamento * (percentual_entrada / 100)
    valor_parcela = (valor_financiamento - entrada) / (prazo_solicitado_anos * 12)
    renda_total = renda_mensal + renda_complementar

    if score_credito < 600:
        return "Reprovado", "Score de crédito inferior ao mínimo exigido."
    if restricao_nome == 1:
        return "Reprovado", "Cliente possui restrições no nome (SPC/Serasa)."
    if inadimplencias_3_anos > 0:
        return "Reprovado", "Cliente com histórico recente de inadimplência."
    if percentual_entrada < 20:
        return "Reprovado", "Entrada abaixo do mínimo exigido (20%)."
    if prazo_solicitado_anos > 20:
        return "Reprovado", "Prazo acima do máximo permitido (20 anos)."
    if renda_total < 3 * valor_parcela:
        return "Reprovado", "Renda total inferior a 3x o valor da parcela."

    return "Aprovado", "Cliente atende a todos os critérios de aprovação."

@app.route('/analisar_credito', methods=['POST'])
def analisar():
    dados = request.get_json()
    status, justificativa = analisar_credito(dados)
    return jsonify({"status": status, "justificativa": justificativa})

if __name__ == "__main__":
    app.run(debug=True)

