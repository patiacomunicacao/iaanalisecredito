# treinar_modelo.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Dados simulados
dados = pd.DataFrame({
    'idade': [25, 40, 35, 50, 23, 45, 33, 60, 38, 29],
    'renda': [2000, 8000, 5000, 9000, 1500, 7000, 4000, 12000, 5200, 3000],
    'tempo_emprego': [1, 10, 5, 15, 0.5, 12, 3, 20, 4, 2],
    'score_credito': [600, 800, 720, 850, 500, 780, 700, 900, 710, 620],
    'inadimplente': [1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
})

X = dados.drop('inadimplente', axis=1)
y = dados['inadimplente']

modelo = RandomForestClassifier()
modelo.fit(X, y)

with open('modelo_treinado.pkl', 'wb') as f:
    pickle.dump(modelo, f)
