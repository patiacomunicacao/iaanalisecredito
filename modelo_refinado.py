import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib
 
# 1. Carregar dataset (seu CSV com idade e regiao)
df = pd.read_csv('dataset_credito_simulado.csv')  # Substitua se for outro nome

# 2. Normalizar idade
scaler = StandardScaler()
df['idade_norm'] = scaler.fit_transform(df[['idade']])

# 3. One-Hot Encoding da variável 'regiao'
df = pd.get_dummies(df, columns=['regiao'], drop_first=True)

# 4. Definir Features (X) e Target (y)
X = df.drop(columns=['status', 'idade'])  # Remover idade original, usamos idade_norm
y = df['status']

# 5. Separar em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Treinar RandomForest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 7. Avaliar desempenho
y_pred = modelo.predict(X_test)
y_proba = modelo.predict_proba(X_test)[:, 1]

print("\nRelatorio de Classificacao:")
print(classification_report(y_test, y_pred))

auc = roc_auc_score(y_test, y_proba)
print(f"AUC: {auc:.3f}")

# 8. Salvar o modelo refinado em .pkl
joblib.dump(modelo, 'modelo_credito_refinado.pkl')
print("Modelo salvo como modelo_credito_refinado.pkl")

# 9. Salvar scaler para normalizar idade em produção
joblib.dump(scaler, 'scaler_idade.pkl')
print("Scaler salvo como scaler_idade.pkl")
