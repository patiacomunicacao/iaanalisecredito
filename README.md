
# API de Análise de Crédito (Simples)

Esta é uma API local feita em Flask que simula a aprovação ou reprovação de crédito com base em regras de negócio simples.

## Como rodar

1. Abra o terminal e vá até a pasta do projeto:
```
cd api_credito_local
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Inicie a API:
```
python app.py
```

A API estará disponível em `http://127.0.0.1:5000/analisar_credito`

## Como testar

Você pode usar o Postman ou um script Python para enviar um POST como este:

### Exemplo de corpo JSON:
```json
{
  "score_credito": 750,
  "restricao_nome": 0,
  "inadimplencias_3_anos": 0,
  "percentual_entrada": 25,
  "prazo_solicitado_anos": 15,
  "renda_mensal": 7000,
  "renda_complementar": 1000,
  "valor_financiamento": 200000
}
```

### Exemplo de resposta:
```json
{
  "status": "Aprovado",
  "justificativa": "Cliente atende a todos os critérios de aprovação."
}
```
