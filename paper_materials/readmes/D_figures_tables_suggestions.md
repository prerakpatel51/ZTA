# D. Figure, Flowchart, and Table Suggestions

---

## Figure 1: Flowchart — Two-Stage Zero Trust Decision Process

**Type:** Flowchart (suitable for draw.io, Lucidchart, or LaTeX TikZ)

**Description:**

```
[Access Request Arrives]
        |
        v
+----------------------------------+
|  STAGE 1: Deterministic Policy   |
|        Evaluation                |
|  (PE evaluates identity,         |
|   credentials, role, resource    |
|   policy, device compliance)     |
+----------------------------------+
        |
    +---+---+
    |       |
 [DENY]  [ALLOW]
    |       |
    v       v
 [Block  +----------------------------------+
  Access] |  STAGE 2: ML Risk Alarm Layer    |
          |  (Lightweight contextual         |
          |   anomaly evaluation)            |
          |  Features: device posture,       |
          |  geolocation, time-of-access,    |
          |  behavioral deviation,           |
          |  request velocity, session       |
          |  context                         |
          +----------------------------------+
                    |
              +-----+-----+
              |           |
         [NORMAL]    [RISKY FLAG]
              |           |
              v           v
         [Access     +---------------------------+
          Proceeds]  | Risk Response Actions:    |
                     | - Log to SIEM             |
                     | - Alert analyst           |
                     | - Flag for audit          |
                     | - Optional: step-up       |
                     |   challenge or reduced    |
                     |   privileges (if design   |
                     |   permits)                |
                     +---------------------------+
                              |
                              v
                     [Access proceeds with
                      enhanced monitoring
                      and audit trail]
```

**Key design notes:**
- Deterministic policy DENY is final — ML layer is never consulted for denied requests
- ML layer only evaluates requests that pass Stage 1
- ML layer does NOT override the deterministic ALLOW — it supplements with risk awareness
- All outcomes are logged; risky flags trigger additional audit/alert actions
- Use color coding: green for normal path, amber/orange for risky path, red for deny path

---

## Figure 2: Conceptual Architecture Diagram

**Type:** Block diagram (suitable for draw.io, Lucidchart, PowerPoint, or LaTeX)

**Description:**

```
+=====================================================+
|                   CONTROL PLANE                      |
|                                                      |
|  +----------------+    +------------------------+    |
|  | Deterministic  |    |    ML Risk Alarm       |    |
|  | Policy Engine  |<-->|    Layer               |    |
|  | (PE)           |    |  +------------------+  |    |
|  |                |    |  | Feature          |  |    |
|  | - Identity     |    |  | Extraction:      |  |    |
|  | - Role/RBAC    |    |  | - Device posture |  |    |
|  | - Resource     |    |  | - Geolocation    |  |    |
|  |   policy       |    |  | - Time-of-access |  |    |
|  | - Compliance   |    |  | - Behavior dev.  |  |    |
|  |   rules        |    |  | - Req. velocity  |  |    |
|  +-------+--------+    |  | - Session ctx    |  |    |
|          |              |  +------------------+  |    |
|          |              |  | ML Model         |  |    |
|          |              |  | (e.g., XGBoost,  |  |    |
|          |              |  |  Random Forest,   |  |    |
|          |              |  |  or lightweight   |  |    |
|          |              |  |  ensemble)        |  |    |
|          |              |  +------------------+  |    |
|  +-------+--------+    |  | Risk Score +     |  |    |
|  | Policy          |    |  | Flag Output      |  |    |
|  | Administrator   |    |  +------------------+  |    |
|  | (PA)            |    +------------------------+    |
|  +-------+--------+                |                  |
|          |                         |                  |
+=========|=========================|==================+
          |                         |
          |              +----------+---------+
          |              | Explanation Module  |
          |              | (Offline/Analyst)   |
          |              |                     |
          |              | - SHAP: feature     |
          |              |   attribution       |
          |              | - DiCE: counter-    |
          |              |   factual "what-if" |
          |              +----------+----------+
          |                         |
+=========|=========================|==================+
|                   DATA PLANE                         |
|                                                      |
|  +----------+     +----+     +------------------+    |
|  | Subject/ |---->| PEP|---->| Enterprise       |    |
|  | Device   |     |    |     | Resource         |    |
|  +----------+     +----+     +------------------+    |
|                                                      |
+=========================|============================+
                          |
                          v
               +--------------------+
               | Audit / SIEM /     |
               | Logging Pipeline   |
               | (risk flags,       |
               |  explanations,     |
               |  access records)   |
               +--------------------+
```

**Key design notes:**
- The PE (deterministic) is the authoritative decision-maker
- The ML Risk Alarm Layer operates in parallel or post-decision, NOT as a gate
- The Explanation Module (SHAP/DiCE) is positioned as offline/analyst-facing, not in the enforcement path
- All risk flags and explanations flow to the Audit/SIEM pipeline
- Color suggestions: blue for deterministic policy, orange for ML alarm, green for explanation module, gray for data plane

---

## Table I: Comparison of Access Control Approaches

**Type:** Comparison table (suitable for IEEE paper, Word, or LaTeX)

| Characteristic | Deterministic Policy Only | Black-Box ML Decision | Proposed: Deterministic + Explainable ML Alarm |
|---|---|---|---|
| Authorization authority | Deterministic rules | ML model output | Deterministic rules (sole authority) |
| Risk awareness | Limited to predefined rules | Contextual, adaptive | Contextual, adaptive (via ML layer) |
| Explainability | High (rules are inspectable) | Low (opaque model) | High (rules + SHAP/DiCE explanations) |
| Adaptability to novel threats | Low (requires rule updates) | High (learns patterns) | Moderate-High (ML detects, rules control) |
| Auditability | High (deterministic trace) | Low (black-box log) | High (deterministic trace + explained risk flags) |
| Compliance readiness | High | Low (difficult to justify) | High (deterministic decisions + transparent risk rationale) |
| Risk of false ML authorization | None | High (ML errors grant access) | None (ML cannot grant access) |
| Analyst support | Minimal | Minimal (no explanation) | Strong (SHAP attribution + counterfactual debugging) |
| Suitability for IIoT/safety-critical | Moderate (limited adaptability) | Low (unacceptable opacity) | High (deterministic safety + adaptive awareness) |

---

## Table II: Roles of SHAP and DiCE in the Proposed Framework

**Type:** Comparison table

| Aspect | SHAP (Feature Attribution) | DiCE (Counterfactual Explanations) |
|---|---|---|
| Primary question answered | "Why was this request flagged as risky?" | "What minimal changes would make this request appear normal?" |
| Explanation type | Feature importance values per prediction | Alternative input scenarios that flip the prediction |
| Example output | "Risk driven 42% by geolocation anomaly, 28% by time-of-access, 18% by device posture" | "Request would be classified as normal if: (a) access time were 09:00-17:00, or (b) geolocation were domestic + device posture compliant" |
| Primary use case | Analyst alerting, audit logging, risk triage | Policy debugging, post-incident analysis, root cause investigation |
| Timing | Near-real-time (for flagged requests) or batch | Primarily offline (post-hoc analysis) |
| Computational cost | Moderate (TreeSHAP is efficient for tree models) | Higher (optimization-based counterfactual search) |
| Theoretical basis | Shapley values (cooperative game theory) | Constrained optimization with diversity |

---

## Optional Figure 3: Conceptual Benefit Comparison (Bar Chart Idea)

**Type:** Conceptual bar chart — NOT based on empirical data, for illustration purposes only

**Label:** "Fig. 3. Qualitative comparison of expected benefits across access control approaches (conceptual illustration, not empirical data)"

**X-axis categories:** Auditability, Analyst Trust, Interpretability, Adaptability, Compliance Readiness

**Series:**
- Deterministic-Only: High, Low, High, Low, High
- Black-Box ML: Low, Low, Low, High, Low
- Proposed Framework: High, High, High, Moderate-High, High

**Use:** Likert-style qualitative ratings (e.g., 1=Low, 2=Moderate, 3=High) to create a simple grouped bar chart

**Important note:** This figure must be clearly labeled as a conceptual/qualitative illustration. Do not present it as based on empirical measurements.

---

## Optional Figure 4: Literature Theme Taxonomy (Tree Diagram)

**Type:** Simple tree/taxonomy diagram

```
                    Literature Themes
                          |
          +---------------+----------------+
          |               |                |
    Zero Trust       ML for Security    XAI Methods
    Architecture         |                |
          |         +----+----+       +---+---+
     +----+----+    |         |       |       |
     |         |  Anomaly   User    SHAP   Counter-
   NIST    ZTA in Detection Behavior        factual
  800-207  IIoT/           Analytics       (DiCE)
           OT/CPS                            |
                                        Robustness/
                                        Stability
```

**Use:** Visual summary of how the literature themes connect and where the gap lies (at the intersection of all three branches)
