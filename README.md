# ZTA: Explainable ML Risk Alarm Layer for IIoT Zero Trust

Conceptual framework + proof-of-concept code for a two-stage Zero Trust Architecture (ZTA) for Industrial IoT (IIoT). Deterministic Policy Engine retains sole authorization authority. Secondary ML layer (XGBoost + SHAP + DiCE) flags contextually anomalous but policy-authorized access requests as an advisory alarm, never blocking.

Paper: `paper_materials/paper.pdf`

## Motivation

ZTA Policy Engines verify every access request against identity, device posture, and context. In IIoT, deploying ML at the edge introduces problems: opaque authorization, audit gaps, and safety risk when a model blocks a legitimate control-room action. This project places an **explainable ML advisory layer alongside — not inside — the deterministic enforcement path**.

## Two-Stage Architecture

1. **Stage 1 — Deterministic Policy Evaluation.** PE applies identity, role/attribute, device compliance, and resource-specific rules. Denial is final. ML not consulted for denied requests.
2. **Stage 2 — ML Risk Alarm.** For policy-cleared requests, gradient-boosted classifier evaluates contextual signals (device attestation, geolocation deviation, time-of-access, behavioral baseline divergence, request velocity). Produces risk score + SHAP attribution + optional DiCE counterfactual. Logs, alerts, or escalates monitoring. No enforcement path.

## Edge Deployment Stack

| Component | Tool | Role |
|-----------|------|------|
| Policy Enforcement Point | Envoy | Ingress gateway |
| Policy Engine | Open Policy Agent (OPA) | Rego policy evaluation |
| Identity Provider | Keycloak | OIDC + MFA |
| Workload Identity | SPIRE / SPIFFE | mTLS SVIDs |
| Secrets / PKI | HashiCorp Vault | Dynamic creds, short-lived certs |
| Orchestration | K3s | Lightweight Kubernetes for edge |
| ML Layer | XGBoost + TreeSHAP + DiCE | Risk scoring + explanations |

## Repo Layout

```
paper_materials/   IEEE conference paper (paper.tex, paper.pdf) + references
ml/                Proof-of-concept training pipeline
  train.py         XGBoost trainer, SHAP + DiCE generator
  iiot_access_logs.csv   Synthetic access log dataset
  iiot_risk_model.joblib Trained model
  shap_summary.png       Global feature importance
  shap_waterfall.png     Local explanation for flagged request
Notes/             Paper summaries and future work
Research_Papers/   Referenced ZTA / IIoT / auth papers
Study_Material/    NIST SP 800-207 and supporting material
```

## Synthetic Dataset Schema

Public IIoT intrusion-detection datasets (KDD'99, CICIDS2017, CSE-CIC-IDS2018, ISCXIDS2012, Kyoto 2006+, Edge-IIoTset, UNSW-NB15) capture network flows, not identity-bound access requests. They lack `user_role`, `device_posture`, `geo_dist_km`, `baseline_dev`, and `req_velocity`. An LLM-generated synthetic corpus bootstraps the training pipeline:

| Field | Type | Example |
|-------|------|---------|
| `user_role` | categorical | operator, engineer, auditor |
| `hour_of_day` | int [0–23] | 14 |
| `day_of_week` | int [0–6] | 2 |
| `geo_dist_km` | float | 12.4 |
| `device_posture` | categorical | compliant, unknown |
| `resource_type` | categorical | historian, PLC, HMI |
| `req_velocity` | float (req/min) | 3.2 |
| `session_dur_s` | float | 142.0 |
| `baseline_dev` | float [0–1] | 0.71 |
| `label` | binary | 0 = normal, 1 = anomalous |

Synthetic data is proof-of-concept only. Not deployment-ready.

## Running the Proof-of-Concept

```bash
cd ml
pip install xgboost scikit-learn shap dice-ml pandas numpy matplotlib joblib
python train.py
```

Outputs classification report, ROC-AUC, SHAP summary + waterfall plots, and DiCE counterfactuals for the highest-risk flagged request.

## Proof-of-Concept Results (Synthetic Test Set)

| Class | Precision | Recall | F1 |
|-------|-----------|--------|-----|
| Normal | 0.94 | 0.97 | 0.96 |
| Anomalous | 0.91 | 0.82 | 0.86 |
| Macro avg | 0.93 | 0.90 | 0.91 |

ROC-AUC: 0.92. Precision > recall on the anomalous class — preferred failure mode for ZTA (missed alarm < false alarm trained to ignore).

## Building the Paper

```bash
cd paper_materials
pdflatex paper.tex && pdflatex paper.tex
```

## Limitations

Conceptual framework, not an implemented system. Edge stack is specified, not deployed. Synthetic training data is a bootstrap, not a substitute for real operational logs. Empirical validation, SHAP stability evaluation, and SOC-analyst user study are future work. Details in paper Section VIII.

## License

Academic / research use.
