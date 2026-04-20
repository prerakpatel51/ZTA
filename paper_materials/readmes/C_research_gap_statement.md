# C. Research Gap Statement

---

## Full Version (1 paragraph)

While Zero Trust Architecture provides a well-defined framework for continuous, policy-driven access control, and NIST SP 800-207 explicitly acknowledges the role of contextual and behavioral signals in trust evaluation, the internal mechanisms by which these signals are weighted and scored within the Policy Engine remain largely opaque. Existing research has advanced ML-based anomaly detection for network intrusion detection and user behavior analytics, and explainable AI methods such as SHAP and counterfactual explanations have been applied to cybersecurity classification tasks. However, the intersection of these three areas — the integration of an explainable, ML-based risk assessment layer that operates alongside (rather than in place of) the deterministic policy gate within a ZTA decision workflow — has received limited attention. In particular, few studies propose architectures where ML serves strictly as an assistive alarm and audit layer, with deterministic policy retaining full authorization authority, while explainability methods support analyst trust, compliance documentation, and post-hoc policy debugging. This gap is especially pronounced in IIoT and cyber-physical system contexts, where device heterogeneity, safety constraints, and regulatory compliance requirements make both transparency and deterministic assurance critical. The present work addresses this gap by proposing a two-stage framework that preserves deterministic ZTA policy as the authoritative control mechanism while introducing a lightweight, explainable ML risk alarm layer to enhance auditability, anomaly awareness, and analyst decision support.

---

## Condensed Version (2-3 sentences)

Despite growing interest in both ML-augmented Zero Trust and explainable AI for cybersecurity, the literature lacks frameworks that position explainable ML specifically as a non-authoritative risk alarm layer alongside deterministic ZTA policy enforcement. This gap is particularly critical in IIoT environments, where compliance mandates demand both transparent risk reasoning and predictable, policy-governed access control. Our work targets this underexplored intersection.

---

## Alternative Wordings

### Alternative 1 (emphasis on the hierarchy)
Current literature has not adequately explored hierarchical ZTA designs in which a deterministic policy gate retains sole authorization authority while a secondary ML layer operates exclusively in an advisory and auditing capacity, with its risk assessments made interpretable through methods such as SHAP feature attribution and counterfactual analysis. This represents a meaningful architectural gap, particularly for high-assurance IIoT systems where black-box risk scoring raises compliance and safety concerns.

### Alternative 2 (emphasis on explainability gap)
While XAI methods have been applied to network intrusion detection and malware classification within security contexts, their application to the trust evaluation process within ZTA — specifically to provide feature-level risk attribution and counterfactual debugging for access decisions — remains largely unexplored. Bridging this gap is essential for IIoT environments where security analysts must understand not merely that a request was flagged, but why it was flagged and what minimal contextual changes would alter the risk assessment.

### Alternative 3 (emphasis on practical deployment gap)
Existing work on ML-augmented Zero Trust tends to position ML as a direct decision-making component rather than as a secondary, explainable alarm layer that supports but does not override deterministic policy. For safety-critical IIoT deployments, this design choice is consequential: an opaque ML model that directly controls access introduces risks that a transparent, assistive layer deliberately avoids. The literature has not sufficiently addressed this distinction, nor has it explored how SHAP and counterfactual explanations could specifically serve the audit and compliance workflows that IIoT Zero Trust deployments require.
