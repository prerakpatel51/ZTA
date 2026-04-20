# G. Strong Claims vs. Cautious Claims Analysis

---

## Claims Strongly Supported by Literature

These claims can be stated confidently with direct citation support:

1. **ZTA is a well-defined architectural paradigm with institutional backing.** NIST SP 800-207 provides a formal specification. The DoD has published its own reference architecture. This is not contested.

2. **NIST SP 800-207 explicitly supports contextual, behavioral trust evaluation.** Tenet 4 enumerates behavioral and environmental attributes. Section 3.3 describes contextual trust algorithms with specific anomaly scenarios (volume spikes, after-hours access, unfamiliar locations). This is directly stated in the standard.

3. **The trust scoring mechanism in ZTA can be opaque.** NIST SP 800-207 acknowledges that weighting "may be a proprietary algorithm." This is a documented gap, not an inference.

4. **ML-based anomaly detection using contextual features is well-established in cybersecurity.** Chandola et al., Sarker et al., Salem et al., and numerous IDS studies validate this. The specific feature categories (device posture, geolocation, timing, velocity, behavioral deviation) are standard in the literature.

5. **SHAP provides theoretically grounded feature attribution.** Lundberg and Lee proved that SHAP values satisfy local accuracy, missingness, and consistency. TreeSHAP enables efficient computation. This is foundational and well-cited.

6. **DiCE generates diverse counterfactual explanations.** Mothilal et al. published the method with formal optimization and evaluation. This is established.

7. **XAI has been successfully applied to cybersecurity models.** Wang et al. demonstrated SHAP for IDS. Nkoro et al. applied SHAP and LIME to zero-trust IoT NIDS. Capuano et al. surveyed the field extensively. These are published results.

8. **Explanation instability is a documented concern.** Alvarez-Melis and Jaakkola, and Slack et al. provide empirical evidence. This is an established finding.

9. **IIoT environments present unique challenges for ZTA.** Device heterogeneity, resource constraints, legacy protocols, geographic distribution, and safety/compliance requirements are well-documented in the IoT security literature.

---

## Claims That Should Be Written Cautiously

These claims are supported by inference, synthesis, or adjacently related literature and should use hedged academic language (e.g., "may," "is expected to," "the literature suggests"):

1. **The proposed two-stage architecture would improve auditability compared to opaque ML-only or deterministic-only approaches.** This is a reasonable inference from the design but has not been empirically validated. *Use: "is expected to" or "the design is intended to."*

2. **SHAP and DiCE explanations would improve analyst trust in risk flags.** Wang et al. showed this for IDS. Transferring the finding to ZTA risk alarms is a reasonable but untested extrapolation. *Use: "prior work suggests" or "based on findings in related contexts."*

3. **The ML layer would be effective at detecting contextual anomalies in IIoT access patterns.** The features are well-motivated and the ML methods are proven for anomaly detection, but the specific performance on IIoT access data is unknown. *Use: "the proposed features are well-established for anomaly detection" without claiming specific detection rates.*

4. **Counterfactual explanations would be useful for policy debugging.** This is a logical argument based on DiCE's design, but no empirical study has tested this in a ZTA context. *Use: "DiCE is designed to support" or "counterfactual analysis could serve."*

5. **The framework is particularly well-suited to IIoT.** This argument draws on the predictability of IIoT access patterns and regulatory requirements, but suitability has not been empirically demonstrated. *Use: "IIoT environments may be particularly well-suited" or "the framework's design choices are motivated by IIoT characteristics."*

6. **TreeSHAP can provide near-real-time explanations for flagged requests.** TreeSHAP is efficient, but "near-real-time" depends on the specific deployment scale and hardware. *Use: "TreeSHAP provides efficient computation that may enable near-real-time explanation generation for tree-based models."*

---

## Claims That Are Conceptual/Speculative and Should Be Framed as Future Work

These should be explicitly framed as open research questions, future directions, or design options:

1. **Explanation stability analysis using Hessian curvature or related methods.** This is an advanced idea with limited direct precedent in cybersecurity applications. *Frame as: "future work may explore" or "an interesting direction for advanced evaluation."*

2. **Step-up authentication triggered by ML risk flags.** While conceptually reasonable, the interaction between ML-triggered step-ups and IIoT operational continuity has not been studied. *Frame as: "a design option that requires careful study" or "one possible response mechanism."*

3. **Effectiveness of synthetic or simulated datasets for evaluation.** Without having conducted the simulation, this is a proposed methodology. *Frame as: "future work plans include" or "evaluation using synthetic or controlled data is planned."*

4. **Adversarial robustness of the ML risk alarm layer.** Important concern but entirely unstudied for this specific design. *Frame as: "adversarial robustness should be assessed in future work."*

5. **Reduction of false positive rates through feature engineering or threshold calibration.** Reasonable goal but no evidence yet. *Frame as: "managing false positive rates through careful feature engineering and threshold calibration will be a critical aspect of future implementation."*

6. **User study results showing analyst preference for SHAP/DiCE explanations.** No user study has been conducted. *Frame as: "future work should include user studies with security analysts to assess explanation utility."*

---

## Summary Rule of Thumb

| Claim Category | How to Write |
|---|---|
| Supported by published evidence | State directly with citation |
| Supported by design logic or adjacent literature | Use "is expected to," "may," "the design is intended to," "prior work in related contexts suggests" |
| Speculative or future-oriented | Use "future work should explore," "an open question is," "one possible direction is" |
