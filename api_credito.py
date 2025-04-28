!pip install flask

from flask import Flask, request, jsonify

app =  Flask(__name__)

#Função para aplicar as regras de negócio
def analisar_credito(dados):
  try:
    score_credito = dados.get('score_credito')
    restricao_nome = dados.get('restricao_nome')
    inadimplencia_3_anos = dados.get('inadimplencia_3_anos')
    percentual_entrada = dados.get('percentual_entrada')
    prazo_solicitado_anos = dados.get ('prazo_solicitado_anos')
    renda_mensal = dados.get('renda_mensal')
    renda_complementar = dados.get('renda_complementar')
    valor_financiamento = dados.get('valor_financiamento')

    #Calcular renda total e valor estimado da parcela
    entrada = valor_financiamento * (percentual_entrada / 100)
    valor_parcela = (valor_financiamento -  entrada) / (prazo_solicitado_anos * 12)
    renda_total = renda_mensal + renda_complementar

    #Aplicar regras de negócio
    if score_credito < 500:
      return "Reprovado", "Score de crédito inferior ao mínimo exigido."
    if restricao_nome == 1:
      return "Reprovado", "Cliente possui restrições no nome (SPC/Serasa)."
    if inadimplencia_3_anos == 1:
      return "Reprovado", "Cliente com histórico recente de inadimplência."
    if percentual_entrada < 20:
      return "Reprovado", "Percentual de entrada inferior ao mínimo exigido (20%)."
    if prazo_solicitado_anos > 20:
      return "Reprovado", "Prazo solicitado acima do máximo permitido (20 anos)."
    if renda_total < 3 * valor_parcela:
      return "Reprovado", "Capacidade de pagamento insuficiente (renda abaixo de 3x a parcela)."

    return "Aprovado", "Cliente atende a todos os critérios de aprovação."

  except Exception as e:
    return "Erro", str(e)

#Endpoint da API
@app.route('/analisar_credito', methods=['POST'])
def analisar():
  dados = request.get_json()
  status, justificativa = analisar_credito(dados)
  return jsonify({
      "status": status,
      "justificativa": justificativa
  })

  #Rodar a API localmente
  if __name__ == '__main__':
    app.run(debug=True)
     
