import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import joblib

print("Treinando e avaliando modelo próprio (Scikit-Learn Random Forest) com limpeza de infinitos...")

features = []
labels = []

peaks_dir = "resultado_peaks"
for f in os.listdir(peaks_dir):
    if f.endswith(".csv"):
        df_p = pd.read_csv(os.path.join(peaks_dir, f))
        if not df_p.empty:
            for _, row in df_p.iterrows():
                snr_val = row['snr']
                if np.isinf(snr_val) or np.isnan(snr_val):
                    snr_val = 999.0  # valor limite seguro
                feat = [float(row['altura']), float(row['fwhm']), float(row['prominence']), float(snr_val)]
                features.append(feat)
                lbl = 1 if float(row['prominence']) > 5.0 and float(row['altura']) > 0 else 0
                labels.append(lbl)

features = np.array(features)
labels = np.array(labels)

# Substituir infintos ou NaNs globais se houver
features = np.nan_to_num(features, nan=0.0, posinf=999.0, neginf=-999.0)

if len(features) > 10:
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"\n--- DESEMPENHO DA NOSSA IA LOCAL ---")
    print(f"Precisão (Precision): {prec:.4f}")
    print(f"Revocação (Recall):   {rec:.4f}")
    print(f"F1-Score:             {f1:.4f}")

    joblib.dump(clf, "modelo_ia_raman_proprio.joblib")
    print("Modelo local salvo com sucesso em 'modelo_ia_raman_proprio.joblib'.")
else:
    print("Dados insuficientes para treino local.")
