# B. Thematic Literature Review Outline

---

## Section II: Related Work — Structural Flow

### II-A. Zero Trust Architecture: Foundations and Core Components
- Origin of the zero trust paradigm (Kindervag, Forrester 2010) [S2]
- NIST SP 800-207 as the definitive reference architecture [S1]
  - PE/PA/PEP model
  - Seven tenets of ZT, particularly Tenet 4 (dynamic policy with behavioral/environmental attributes) and Tenet 7 (collect and use security posture data)
  - Trust Algorithm: criteria-based vs. score-based; singular vs. contextual
  - Input sources: CDM, threat intelligence, activity logs, SIEM
- DoD Zero Trust Reference Architecture and the analytics/visibility pillar [S3]
- **Synthesis point:** ZTA is well-defined architecturally, and contextual trust evaluation using multiple behavioral signals is an explicit design principle. However, the internal mechanisms for weighting and scoring remain underspecified, with NIST acknowledging that weights "may be a proprietary algorithm."

### II-B. Zero Trust in IIoT and Cyber-Physical System Environments
- Challenges of applying ZTA to IoT/IIoT (device heterogeneity, resource constraints, legacy protocols, distributed geography) [S7]
- Zero-trust marine cyberdefense for IoT communications [S4]
- Multi-dimensional trust assessment for satellite/edge networks (subject, object, environment, behavior, physical entity) [S5]
- Identity authentication for edge devices with continuous behavioral trust evaluation [S6]
- **Synthesis point:** Several efforts extend ZTA to non-traditional environments (satellite, marine, edge), but these largely focus on authentication mechanisms and network-level intrusion detection. The policy-engine-level risk assessment layer and its interpretability in IIoT contexts remain underexplored.

### II-C. Machine Learning for Risk Scoring and Anomaly Detection in Security
- Anomaly detection foundations: taxonomy of point, contextual, and collective anomalies [S8]
- AI-driven cybersecurity overview: supervised/unsupervised learning for anomaly detection, feature engineering, behavioral analytics [S9]
- User behavior analytics and masquerade detection through behavioral profiling [S10]
- Contextual features for access anomaly detection: timing, geolocation, device posture, access velocity, session context
- Connection to NIST 800-207 Trust Algorithm: the contextual TA concept (Section 3.3.1 of NIST 800-207) explicitly describes anomaly scenarios (unusual access volume, after-hours access, unfamiliar locations)
- **Synthesis point:** ML-based behavioral analytics and anomaly detection are mature research areas. The features relevant to contextual access risk (device posture, geolocation, timing, velocity) are well-established. However, most work integrates ML directly into detection or access control decisions rather than positioning it as an auxiliary alarm and audit layer alongside deterministic policy.

### II-D. Explainable AI in Cybersecurity
- Survey of XAI methods in cybersecurity: SHAP, LIME, attention, rule extraction [S11]
- Explainable ML for intrusion detection with SHAP-based feature attribution [S12]
- The analyst trust problem: black-box models reduce operator confidence and hinder incident investigation
- Gap: XAI in cybersecurity has focused primarily on intrusion detection and malware classification; limited work applies XAI to access control risk scoring within ZTA workflows
- **Synthesis point:** XAI is increasingly recognized as essential for operational security AI, but the connection between explainability and the ZTA policy decision process is not well-established in the literature. Existing XAI-cybersecurity work targets network-level detection, not policy-engine-level risk support.

### II-E. SHAP and Counterfactual Explanation Methods
- SHAP: Shapley values for feature-level attribution with theoretical guarantees [S13]
  - Strengths: local accuracy, consistency, missingness properties; both local and global explanations
  - Application in security: feature attribution for anomaly flags
- DiCE: diverse counterfactual explanations for actionable understanding [S14]
  - Strengths: answers "what minimal changes would alter the risk classification?"; supports diversity of explanations
  - Application in security: policy debugging, post-hoc validation
- Legal and governance case for counterfactual explanations (GDPR compliance, auditability) [S15]
- **Synthesis point:** SHAP and counterfactual methods offer complementary explanation capabilities. SHAP reveals why a risk score was assigned; DiCE reveals what would need to change. Together, they provide a comprehensive explanation toolkit suitable for analyst-facing risk support in ZTA.

### II-F. Robustness and Stability of Explanations (Brief Treatment)
- Explanation instability near decision boundaries [S16]
- Adversarial vulnerabilities of SHAP and LIME [S17]
- **Synthesis point:** Explanation robustness is a recognized concern but remains largely unaddressed in cybersecurity applications. For our proposed framework, this is acknowledged as an important consideration for future validation, particularly in boundary cases where a request is near the risky/normal threshold.

### II-G. Research Gap Statement (concluding the Related Work section)
- Transition from synthesis to identified gap
- Clear articulation of what is missing
- Natural lead-in to the Proposed Framework (Section III)
