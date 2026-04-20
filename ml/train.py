"""
Train XGBoost anomaly classifier on synthetic IIoT access logs.
Produces:
  - Classification report + ROC-AUC
  - SHAP summary plot (global feature importance)
  - SHAP waterfall for a single flagged request (local explanation)
  - DiCE counterfactuals: minimal changes that would drop the risk flag
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import shap
import dice_ml
import matplotlib.pyplot as plt
import joblib

# ── Load & encode ─────────────────────────────────────────────────────
df = pd.read_csv("iiot_access_logs.csv")

cat_cols = ["user_role", "device_posture", "resource_type"]
encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Train XGBoost ─────────────────────────────────────────────────────
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

# ── Evaluate ──────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n── Classification Report ──────────────────────────────")
print(classification_report(y_test, y_pred, target_names=["normal", "anomalous"]))
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

# ── SHAP: global summary plot ─────────────────────────────────────────
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test, show=False)
plt.tight_layout()
plt.savefig("shap_summary.png", dpi=150)
plt.close()
print("\nSHAP summary plot  → shap_summary.png")

# ── SHAP: waterfall for a single high-risk flagged request ────────────
# Pick the test sample with the highest predicted risk score
flagged_idx = np.argmax(y_prob)
flagged_sample = X_test.iloc[[flagged_idx]]
flagged_score  = y_prob[flagged_idx]

shap_explanation = explainer(flagged_sample)
shap.plots.waterfall(shap_explanation[0], show=False)
plt.tight_layout()
plt.savefig("shap_waterfall.png", dpi=150)
plt.close()

print(f"\nSHAP waterfall (highest-risk request, score={flagged_score:.3f})")
print(f"  Sample: {flagged_sample.to_dict(orient='records')[0]}")
# Top 3 contributing features
contrib = pd.Series(shap_explanation[0].values, index=X_test.columns)
top3 = contrib.abs().nlargest(3)
print("  Top SHAP contributors:")
for feat, val in top3.items():
    direction = "↑ risk" if contrib[feat] > 0 else "↓ risk"
    print(f"    {feat}: {contrib[feat]:+.4f}  ({direction})")
print("  → shap_waterfall.png")

# ── DiCE: counterfactual explanations ────────────────────────────────
print("\n── DiCE Counterfactuals ───────────────────────────────")

# DiCE needs the training data with the label column
train_df = X_train.copy()
train_df["label"] = y_train.values

continuous_feats = [
    "hour_of_day", "day_of_week", "geo_dist_km",
    "req_velocity", "session_dur_s", "baseline_dev"
]
categorical_feats = ["user_role", "device_posture", "resource_type"]

dice_data = dice_ml.Data(
    dataframe=train_df,
    continuous_features=continuous_feats,
    outcome_name="label"
)

dice_model = dice_ml.Model(model=model, backend="sklearn", model_type="classifier")
exp = dice_ml.Dice(dice_data, dice_model, method="random")

# Generate counterfactuals for the same flagged request
cf_result = exp.generate_counterfactuals(
    flagged_sample,
    total_CFs=3,
    desired_class="opposite",   # flip from anomalous → normal
    features_to_vary=continuous_feats,
)

print(f"  Original request (risk score={flagged_score:.3f}, predicted anomalous):")
print(f"  {flagged_sample.to_dict(orient='records')[0]}\n")
print("  Counterfactuals (minimal changes to become 'normal'):")
cf_df = cf_result.cf_examples_list[0].final_cfs_df
for i, row in cf_df.iterrows():
    changes = {
        col: f"{flagged_sample[col].values[0]:.2f} → {row[col]:.2f}"
        for col in continuous_feats
        if abs(row[col] - flagged_sample[col].values[0]) > 0.01
    }
    print(f"  CF {i+1}: {changes}  → predicted label: {int(row['label'])}")

# ── Save model ────────────────────────────────────────────────────────
joblib.dump(model, "iiot_risk_model.joblib")
print("\nModel saved → iiot_risk_model.joblib")
