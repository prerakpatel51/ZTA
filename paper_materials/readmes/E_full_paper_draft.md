# An Explainable ML Risk Alarm Layer to Assist Deterministic Policy Decisions in Zero Trust Architecture for IIoT Security

---

**Abstract** — Zero Trust Architecture (ZTA) enforces continuous verification through a Policy Engine that evaluates access requests against identity, device posture, and contextual signals. While this model is well-suited to Industrial Internet of Things (IIoT) environments where safety and compliance are paramount, the trust scoring mechanisms within the Policy Engine often remain opaque, limiting analyst understanding and audit capability. This paper proposes a two-stage decision framework that preserves deterministic policy enforcement as the sole authorization authority while introducing a lightweight, machine-learning-based risk alarm layer as a secondary, non-authoritative component. The ML layer evaluates contextual signals — including device attestation status, geolocation anomaly, time-of-access deviation, behavioral baseline divergence, and request velocity — to flag potentially anomalous access requests that nonetheless satisfy deterministic policy criteria. To address the interpretability challenge, the framework incorporates SHAP (SHapley Additive exPlanations) for feature-level risk attribution and DiCE (Diverse Counterfactual Explanations) for generating actionable, counterfactual analyses that support post-hoc validation and policy debugging. The explainability components are positioned as offline, analyst-facing tools rather than inline enforcement mechanisms. This design choice reflects both the safety requirements of IIoT systems and the regulatory need for auditable, transparent risk reasoning. The paper synthesizes literature across ZTA foundations, IIoT security, ML-based anomaly detection, and explainable AI to establish the research gap and motivate the proposed architecture. As a conceptual framework paper, it contributes a carefully argued architectural direction grounded in existing standards and research, with future work planned toward empirical validation using realistic access log datasets.

*Keywords* — Zero Trust Architecture, Explainable AI, Industrial IoT, SHAP, Counterfactual Explanations, Risk Scoring, Anomaly Detection, Policy Engine

---

## I. INTRODUCTION

Perimeter-based network security has proven insufficient for modern enterprise environments where users, devices, and applications operate across distributed, heterogeneous, and often untrusted networks [1]. Zero Trust Architecture (ZTA) addresses this shortcoming by adopting the principle that no entity should be implicitly trusted and that every access request must be continuously verified against dynamic policy [2]. The National Institute of Standards and Technology (NIST) formalized this paradigm in Special Publication 800-207, which defines the core logical components — the Policy Engine (PE), Policy Administrator (PA), and Policy Enforcement Point (PEP) — and describes how contextual, behavioral, and environmental signals can inform access decisions [2].

The challenge of implementing robust, adaptive access control becomes especially acute in Industrial Internet of Things (IIoT) environments. IIoT deployments are characterized by device heterogeneity, resource-constrained endpoints, legacy communication protocols, and geographically distributed architectures [3]. These systems frequently operate in safety-critical and compliance-sensitive domains — manufacturing, energy, transportation, and critical infrastructure — where both the consequences of unauthorized access and the regulatory requirements for transparency are heightened [4]. Applying ZTA principles to such environments demands not only rigorous policy enforcement but also intelligent monitoring that accounts for the unique contextual dynamics of industrial operations.

Within the ZTA framework, NIST SP 800-207 describes a Trust Algorithm that processes multiple input sources — access requests, subject attributes and history, asset databases, resource policy requirements, and threat intelligence — to produce access decisions [2]. The specification distinguishes between criteria-based and score-based trust algorithms and between singular and contextual evaluation strategies. A contextual trust algorithm, for instance, might detect that a user who normally accesses a set number of records during business hours is suddenly requesting an anomalous volume of data at an unusual time from an unfamiliar location [2]. These contextual signals are precisely the kind of behavioral and environmental indicators that machine learning (ML) models are well-positioned to evaluate.

However, a tension exists between the potential value of ML-based contextual analysis and the requirements for deterministic, auditable access control. When ML models are used to directly make or override authorization decisions, their opacity introduces risks: security analysts cannot readily understand why a decision was made, compliance auditors cannot trace the reasoning behind access grants, and safety-critical systems face the prospect of unpredictable behavior from models whose internal logic is not inspectable [5]. This is particularly problematic in IIoT, where regulatory frameworks may require documented justification for access control decisions and where the consequences of incorrect access grants — or incorrect denials — can extend to physical safety.

This paper proposes a conceptual framework that addresses this tension through a hierarchical, two-stage design. In the first stage, a deterministic policy gate evaluates access requests against explicit rules governing identity, credentials, role-based permissions, device compliance, and resource access policies. This stage remains the sole authoritative mechanism for granting or denying access. In the second stage, a lightweight ML-based risk alarm layer evaluates the contextual characteristics of requests that have passed the deterministic gate, flagging those that exhibit anomalous or suspicious patterns. The ML layer does not control access; it serves as an assistive alarm, logging, and audit mechanism that enhances analyst awareness, supports post-incident investigation, and strengthens the overall auditability of the ZTA deployment.

To make the ML layer's risk assessments transparent, the framework incorporates two complementary explainability methods. SHAP (SHapley Additive exPlanations) [6] provides feature-level attribution, enabling analysts to understand which contextual factors contributed most to a risk flag. DiCE (Diverse Counterfactual Explanations) [7] generates counterfactual scenarios that illustrate what minimal realistic changes in the access context would alter the risk classification, supporting policy debugging and root cause analysis. Both explanation methods are positioned as offline or analyst-facing tools rather than components in the real-time enforcement path.

The contributions of this paper are as follows:
1. A synthesis of literature across ZTA, IIoT security, ML-based anomaly detection, and XAI to identify the gap at their intersection.
2. A proposed two-stage architecture that preserves deterministic ZTA policy authority while adding explainable ML-based risk awareness.
3. A detailed description of how SHAP and DiCE serve complementary roles in supporting analyst trust, auditability, and policy debugging.
4. An honest framing of this work as a conceptual framework paper with clearly stated limitations and future evaluation plans.

The remainder of this paper is organized as follows: Section II reviews related work across the relevant themes, Section III describes the proposed framework, Section IV discusses expected outcomes and trade-offs, Section V addresses limitations and future work, and Section VI concludes the paper.

---

## II. RELATED WORK

### A. Zero Trust Architecture Foundations

The concept of zero trust originated with Kindervag at Forrester Research, who argued in 2010 that the traditional perimeter-based security model — in which entities inside the network boundary are trusted by default — is fundamentally flawed [1]. This insight gained institutional backing when NIST published SP 800-207, which provides a formal reference architecture for ZTA [2]. The NIST model defines the Policy Decision Point (PDP), composed of the Policy Engine and Policy Administrator, as the core control-plane mechanism that evaluates access requests and instructs the Policy Enforcement Point to allow or block data-plane communication. The architecture draws on multiple data sources — continuous diagnostics and mitigation (CDM) systems, industry compliance requirements, threat intelligence feeds, network activity logs, and security information and event management (SIEM) systems — to inform the PE's trust evaluation [2].

NIST's specification identifies seven tenets of zero trust. Tenet 4 states that access is determined by dynamic policy that considers "the observable state of client identity, application/service, and the requesting asset" and "may include other behavioral and environmental attributes," explicitly enumerating factors such as time/date of request, previously observed behavior, and measured deviations from usage patterns [2]. Tenet 7 directs enterprises to collect as much information as possible about asset state, network traffic, and access requests, and to use this data for improving security posture [2]. Together, these tenets provide an institutional mandate for the kind of behavioral and contextual analysis that ML-based approaches can deliver.

The Trust Algorithm described in Section 3.3 of NIST SP 800-207 processes inputs from five categories: access requests, subject databases and history, asset databases, resource policy requirements, and threat intelligence [2]. The specification distinguishes between criteria-based trust algorithms, which apply binary pass/fail checks, and score-based algorithms, which compute a weighted confidence level from multiple data sources. It further distinguishes singular trust algorithms, which evaluate each request independently, from contextual algorithms that consider the subject's recent behavioral history [2]. Notably, for score-based approaches, NIST acknowledges that "the weight of importance for each data source may be a proprietary algorithm," implicitly recognizing that the scoring mechanism may not be transparent [2]. This observation is central to the motivation for our proposed explainability layer.

The Department of Defense Zero Trust Reference Architecture extends the NIST model with operational specificity, identifying seven pillars of zero trust implementation, including a dedicated visibility and analytics pillar that emphasizes continuous behavioral monitoring and threat detection [8]. This official recognition of analytics as a core ZT pillar, rather than an optional enhancement, lends institutional support to ML-based behavioral evaluation within ZTA deployments.

### B. Zero Trust in IIoT and Cyber-Physical Systems

Applying zero trust principles to IIoT environments presents distinct challenges that do not arise in conventional enterprise IT. Industrial deployments typically involve large numbers of heterogeneous devices — sensors, actuators, PLCs, and legacy controllers — many of which have limited computational capacity, run proprietary protocols, and cannot support standard authentication agents [3]. The geographic distribution of industrial assets, the presence of legacy systems that predate modern security standards, and the real-time operational constraints of industrial processes all complicate the deployment of continuous verification mechanisms [9].

Several recent studies have begun addressing this intersection. Nkoro et al. proposed a zero-trust network intrusion detection system (NIDS) for maritime IoT communications that integrates SHAP and LIME to provide explainability for detected cyberattacks [4]. Their work demonstrates that XAI methods can be effectively applied within a ZT-oriented IoT security context, though their approach operates at the network intrusion detection level rather than at the policy engine's risk assessment layer. Fu et al. extended the ZTA model for satellite networks by introducing a multi-dimensional trust framework with five assessment dimensions — subject, object, environment, behavior, and physical entity — and implementing continuous authentication through Neural-Backed Decision Trees at edge nodes [10]. Their multi-dimensional trust concept aligns with the contextual signal categories relevant to our proposed risk alarm layer, though their work focuses on authentication accuracy rather than explainability. Liu et al. proposed an identity authentication protocol for edge devices within a ZTA framework that incorporates continuous trust evaluation using behavioral pattern recognition through convolutional neural networks and Gaussian mixture models [11]. Their work validates the use of behavioral deviation detection in ZTA for resource-constrained environments, though without addressing the explainability of the behavioral analysis.

These studies collectively demonstrate growing interest in extending ZTA to non-traditional environments and in leveraging ML for trust evaluation. However, they share a common characteristic: the ML components are either embedded directly in the authentication or detection decision pipeline or focused on network-level classification, rather than being positioned as a separate, interpretable risk advisory layer alongside a deterministic policy gate.

### C. Machine Learning for Risk Scoring and Anomaly Detection

Machine learning approaches to anomaly detection in cybersecurity are well-established. Chandola et al. provided a comprehensive taxonomy distinguishing point anomalies (individual data instances deviating from normal), contextual anomalies (instances anomalous within a specific context), and collective anomalies (groups of related instances that are jointly anomalous) [12]. This taxonomy is particularly relevant to access request analysis, where a given request may be normal in isolation but anomalous in the context of the requesting user's historical behavior, the time of day, or the device's posture.

Sarker et al. surveyed AI-driven cybersecurity applications including intrusion detection, malware analysis, and user behavior analytics, identifying both supervised and unsupervised learning methods that have shown promise for behavioral anomaly detection [13]. They also noted that the lack of explainability in ML-based security tools is a significant barrier to operational adoption, as security analysts require confidence in the model's reasoning before acting on its outputs [13].

The features relevant to contextual access risk are well-characterized in the literature. Device posture and attestation status reflect whether an endpoint meets security compliance requirements. Geolocation anomaly captures whether an access request originates from an unexpected location relative to the user's or device's baseline. Time-of-access deviation measures whether requests fall outside normal operating patterns. Behavioral baseline divergence captures changes in access patterns, resource usage, or interaction sequences. Request velocity and burstiness detect unusual spikes in access volume. Session context encompasses characteristics of the current session relative to historical norms [2], [12], [14].

These features correspond directly to the contextual trust algorithm inputs described in NIST SP 800-207, which provides examples such as detecting that access requests "suddenly exceed 100 records in a day" or that "someone is making access requests after normal business hours" from "an unrecognizable location" [2]. The literature therefore provides strong support for the feasibility and relevance of ML-based contextual risk scoring using these features. What has been less explored is the architectural positioning of such a model as a secondary, non-authoritative layer alongside deterministic policy, and the application of structured explainability methods to its outputs.

### D. Explainable AI in Cybersecurity

The field of explainable AI (XAI) for cybersecurity has grown substantially in recent years. Capuano et al. conducted a comprehensive survey categorizing XAI approaches in cybersecurity applications, covering model-specific methods (attention mechanisms, rule extraction) and model-agnostic methods (SHAP, LIME, and partial dependence plots) [5]. Their survey identifies significant gaps: most XAI-cybersecurity work focuses on intrusion detection and malware classification, with limited attention to access control, policy support, or ZTA-specific applications [5]. The survey also notes that domain-specific explanation interfaces designed for security analysts remain underdeveloped [5].

Wang et al. applied SHAP values to an ML-based intrusion detection framework evaluated on the NSL-KDD and UNSW-NB15 datasets, demonstrating that feature-level explanations improve analyst confidence in detection outputs without meaningfully degrading detection accuracy [15]. Their finding that explanations can enhance analyst trust and operational willingness to act on model recommendations is directly relevant to our proposed framework, where risk flags accompanied by SHAP-based explanations would serve a similar trust-building function.

The connection between XAI and governance requirements is also relevant. Wachter et al. argued that counterfactual explanations are particularly appropriate for regulatory compliance because they provide actionable information about what would need to change to alter a decision, without requiring full model transparency [16]. This legal and governance perspective supports the use of counterfactual explanations (as in DiCE) for the compliance and audit documentation that IIoT Zero Trust deployments require.

### E. SHAP and Counterfactual Explanation Methods

SHAP, introduced by Lundberg and Lee [6], provides a unified framework for feature-level attribution grounded in Shapley values from cooperative game theory. SHAP values satisfy three desirable properties — local accuracy, missingness, and consistency — making them theoretically well-founded for explaining individual predictions [6]. Efficient implementations such as TreeSHAP enable practical computation for tree-based models, which are commonly used in tabular security data contexts [6].

DiCE, proposed by Mothilal et al. [7], generates diverse counterfactual explanations through optimization that seeks input modifications that are minimal (close to the original instance), feasible (respecting domain constraints on features), and diverse (covering qualitatively different explanation paths) [7]. For a security risk assessment, a DiCE counterfactual might indicate that a risky request would be classified as normal if the access time were during business hours and the geolocation were domestic — providing a concrete, interpretable path for understanding the model's boundary.

These two methods offer complementary capabilities. SHAP answers "which features contributed most to this risk score?" while DiCE answers "what minimal realistic changes would alter this classification?" Together, they provide analysts with both a backward-looking explanation of why a flag was raised and a forward-looking characterization of the decision boundary, supporting triage, debugging, and root cause investigation.

### F. Explanation Robustness and Stability

An emerging concern in the XAI literature is the stability of post-hoc explanations. Alvarez-Melis and Jaakkola demonstrated that small perturbations in input can produce substantially different explanations, particularly near decision boundaries [17]. Slack et al. further showed that SHAP and LIME can be adversarially manipulated to produce misleading explanations [18]. These findings are relevant to any system that relies on explanations for operational decision-making.

For the proposed framework, explanation stability is especially important in boundary cases where a request's risk score is near the threshold between normal and risky classifications. However, since the ML layer in our design is non-authoritative — it does not control access — the consequences of an unstable explanation are less severe than in systems where the explanation directly justifies an access denial. Explanation stability and robustness analysis are therefore positioned as important future evaluation tasks rather than blocking requirements for the proposed architecture.

### G. Research Gap

The preceding review reveals that several relevant research areas have matured independently: ZTA provides a well-defined architectural model with explicit support for contextual and behavioral trust evaluation; ML-based anomaly detection has demonstrated the ability to identify unusual access patterns using contextual features; and XAI methods such as SHAP and DiCE offer complementary mechanisms for making model reasoning transparent. However, the integration of these areas — specifically, the design of an explainable ML risk layer that operates alongside, rather than in place of, deterministic ZTA policy enforcement — has received limited direct attention.

Most ML-augmented security architectures position the ML component as a primary decision-maker or as a direct replacement for traditional rules, rather than as a secondary alarm and audit layer that respects the authority of deterministic policy. In IIoT and cyber-physical system contexts, where both deterministic control assurance and operational transparency are essential, this architectural distinction is consequential. The proposed framework addresses this gap by defining a layered architecture that maintains deterministic policy authority while adding explainable ML-based risk awareness as a supporting capability.

---

## III. PROPOSED FRAMEWORK

### A. Design Philosophy

The proposed framework rests on a fundamental architectural principle: deterministic policy must remain the sole authoritative mechanism for granting or denying access. This principle reflects several practical realities of IIoT and security-critical environments. First, deterministic rules are auditable — every access decision can be traced to an explicit policy statement. Second, deterministic behavior is predictable — operators can reason about system behavior without accounting for model drift, retraining, or statistical uncertainty. Third, regulatory and compliance frameworks in industrial sectors typically require that access control decisions be justifiable in terms that do not depend on opaque model internals.

The ML risk alarm layer is therefore explicitly positioned as a secondary, assistive component. It does not grant access. It does not deny access. It evaluates the contextual characteristics of requests that have already passed the deterministic gate and produces a risk assessment that is logged, can trigger alerts, and can inform analyst investigation — but that does not alter the enforcement decision.

### B. Two-Stage Decision Architecture

The framework implements a two-stage decision process aligned with the NIST SP 800-207 logical component model.

**Stage 1: Deterministic Policy Evaluation.** When an access request arrives at the Policy Enforcement Point, it is forwarded to the Policy Engine for evaluation. The PE applies the enterprise's deterministic access policies, checking the requesting subject's identity and authentication credentials, role-based or attribute-based permissions, device compliance status (as reported by CDM systems), and resource-specific access rules. If any deterministic criterion is not met, the request is denied. This denial is final; the ML layer is not consulted for denied requests, as there is no benefit in risk-scoring a request that will not be granted.

**Stage 2: ML Risk Alarm Evaluation.** For requests that satisfy all deterministic policy criteria, the ML risk alarm layer performs a secondary contextual evaluation. This evaluation does not re-adjudicate the access decision. Instead, it assesses whether the request's contextual characteristics deviate from expected patterns in ways that might indicate compromise, misuse, or anomalous activity that merits further attention.

The ML layer produces a risk score and, when the score exceeds a configured threshold, generates a risk flag. The possible actions following a risk flag are:
- **Logging:** The risk flag, risk score, and associated contextual features are recorded in the SIEM pipeline for audit trail purposes.
- **Analyst alerting:** A notification is sent to the security operations center (SOC) or designated analyst for review.
- **Enhanced monitoring:** The session may be marked for elevated monitoring, with subsequent access requests from the same subject or device receiving closer scrutiny.
- **Optional step-up challenge:** Depending on the deployment configuration, the system may request additional authentication (e.g., multifactor step-up) before proceeding. This is a conceptual design option that would require careful implementation to avoid disrupting legitimate IIoT operations.

Importantly, even when a risk flag is raised, access proceeds (because the deterministic policy has already authorized it). The risk flag creates a record and triggers human-in-the-loop or automated monitoring responses, but it does not override the policy decision.

### C. Feature Set and Signal Categories

The ML risk alarm layer evaluates the following categories of contextual signals, selected based on their alignment with the NIST SP 800-207 Trust Algorithm inputs and the IIoT-specific literature:

1. **Device posture and attestation status:** Whether the device meets security compliance baselines (OS version, patch level, approved software, configuration integrity). In IIoT, this extends to firmware versions, protocol compliance, and hardware attestation.

2. **Geolocation anomaly:** Whether the request originates from a location that deviates from the subject's or device's established baseline. For IIoT, this includes whether a device is communicating from its expected physical location within a facility.

3. **Time-of-access deviation:** Whether the request occurs during expected operational hours relative to the subject's or device's historical access patterns. IIoT devices often have highly predictable access schedules tied to industrial processes.

4. **Behavioral baseline divergence:** Whether the nature, volume, or pattern of access deviates from the subject's or device's established behavioral profile. This captures anomalies such as a sensor controller suddenly requesting access to administrative resources.

5. **Request velocity and burstiness:** Whether the rate of access requests deviates from expected patterns. Unusual spikes may indicate automated scanning, credential stuffing, or exfiltration attempts.

6. **Session context:** Characteristics of the current session relative to historical session profiles, including session duration, sequence of accessed resources, and inter-request timing.

These features are not novel in isolation — they correspond to established behavioral analytics and contextual risk signals in the security literature [2], [12], [13]. The contribution lies in their structured integration within a layered ZTA framework designed for IIoT contexts.

### D. ML Model Considerations

The specific ML model used in the risk alarm layer is a design choice that should be guided by the deployment context. For the proposed framework, lightweight, tabular-data-friendly models such as gradient-boosted trees (XGBoost, LightGBM), random forests, or logistic regression ensembles are appropriate candidates. These models are computationally efficient, compatible with TreeSHAP for fast explanation generation, and well-suited to the structured, feature-engineered data that characterizes access log analysis.

Deep learning approaches, while potentially more powerful for raw data processing, introduce additional latency, complexity, and explanation challenges that may not be justified for a secondary alarm layer. The model selection trade-off between detection capability and operational overhead should be evaluated empirically in future work.

### E. Explainability Components

The framework incorporates two complementary XAI methods, positioned primarily as offline, analyst-facing tools.

**SHAP for feature-level attribution.** When the ML layer produces a risk flag, SHAP values are computed for the flagged instance. These values indicate the contribution of each contextual feature to the risk score. For example, a SHAP analysis might reveal that a particular risk flag was driven 42% by geolocation anomaly, 28% by time-of-access deviation, and 18% by device posture concerns. This feature attribution enables analysts to quickly prioritize investigation, focusing on the aspects of the request that are most anomalous.

For tree-based models, TreeSHAP provides exact Shapley values in polynomial time, making near-real-time SHAP computation feasible for flagged requests [6]. For non-flagged (normal) requests, SHAP computation can be performed in batch during periodic model evaluation cycles.

**DiCE for counterfactual analysis.** DiCE generates diverse counterfactual explanations that describe what minimal, feasible changes in the access context would alter the risk classification. For example, a DiCE analysis might indicate that a risky request would be reclassified as normal if: (a) the access time were shifted to 10:00 AM instead of 2:30 AM, or (b) the geolocation were domestic and the device posture were compliant rather than degraded. These counterfactuals support several use cases:
- **Policy debugging:** Understanding whether a risk flag reflects a genuine anomaly or a gap in the deterministic policy rules.
- **Post-incident analysis:** Reconstructing what contextual factors distinguished a malicious access event from normal operations.
- **Policy refinement:** Identifying feature combinations that frequently trigger risk flags for legitimate operations, enabling targeted policy adjustments.

DiCE computation is more expensive than SHAP and is therefore positioned as a primarily offline tool for analyst investigation and periodic model review, rather than a real-time component.

### F. Integration with ZTA Components

The proposed ML risk alarm layer integrates with the NIST SP 800-207 component model as follows:

- The ML layer receives the same contextual data that feeds the PE's Trust Algorithm (subject attributes, asset state, threat intelligence, activity logs).
- Risk scores and flags are published to the SIEM system, creating a unified audit trail alongside the PE's deterministic access decisions.
- SHAP-based feature attributions for flagged requests are stored as structured metadata in the audit log, enabling later querying (e.g., "show all flags driven primarily by geolocation anomaly in the past week").
- DiCE counterfactual reports are generated on demand by analysts or through scheduled batch analysis.
- The Explanation Module does not introduce additional latency into the enforcement path, as it operates asynchronously with respect to the PE's access decision.

---

## IV. EXPECTED OUTCOMES AND DISCUSSION

### A. Anticipated Benefits

The proposed framework is designed to provide several categories of benefit, each of which should be understood as a reasoned expectation based on the literature rather than an empirically validated result.

**Improved auditability.** By generating structured, explainable risk flags alongside deterministic access decisions, the framework produces a richer audit trail than either deterministic policy alone or opaque ML-based risk scoring. SHAP-based feature attributions provide a machine-readable record of why each flag was generated, supporting compliance documentation and regulatory review.

**Enhanced analyst trust.** The XAI literature consistently identifies model opacity as a barrier to analyst adoption of ML-based security tools [5], [13]. By providing feature-level explanations (SHAP) and actionable counterfactual analyses (DiCE), the framework addresses this barrier, enabling analysts to understand and critically evaluate risk flags rather than accepting or ignoring them as black-box outputs.

**Stronger policy debugging.** DiCE counterfactuals provide a direct mechanism for understanding the ML layer's decision boundary. When a risk flag appears incorrect, the counterfactual analysis can reveal which feature combinations are driving the flag, enabling targeted adjustments to either the ML model's training or the deterministic policy rules.

**Better post-incident analysis.** In the event of a security incident, the combination of deterministic access logs, ML risk scores, SHAP attributions, and DiCE counterfactuals provides a multi-layered forensic record that supports root cause investigation and helps identify what contextual signals, in retrospect, indicated anomalous activity.

**Contextual awareness for IIoT.** IIoT environments exhibit predictable operational patterns (device schedules, process cycles, geographic stability) that create strong baselines for contextual anomaly detection. The ML risk alarm layer is particularly well-suited to these environments because deviations from established patterns — a device communicating at an unexpected time, from an unexpected location, or with an unexpected access pattern — are often operationally significant.

### B. Trade-offs and Practical Considerations

**Latency.** The ML risk alarm layer adds computational overhead. For the proposed design, this overhead is minimized by positioning the ML evaluation asynchronously (or in parallel) with the deterministic decision, so that it does not add latency to the enforcement path. However, if step-up challenges or privilege reduction are triggered by risk flags, these actions do introduce user-visible latency.

**Operational complexity.** Deploying and maintaining an ML layer alongside deterministic policy adds operational burden: the model requires training data, periodic retraining, monitoring for model drift, and tuning of risk thresholds. In IIoT environments where operational stability is valued, this added complexity must be carefully managed.

**False positive burden.** ML-based anomaly detection inherently produces false positives. If risk flags are too frequent and predominantly incorrect, analysts will develop alert fatigue, reducing the effectiveness of the alarm layer. Threshold calibration and feature engineering are critical to managing this trade-off.

**Data availability.** Training a meaningful contextual risk model requires access to representative access log data with sufficient diversity of normal and anomalous patterns. In many IIoT deployments, such data may be limited, proprietary, or difficult to label. This is a significant practical constraint, particularly for initial deployment.

### C. Why This Architecture Is Safer Than Black-Box ML Authorization

A key argument for the proposed architecture is that it is strictly safer than designs in which an ML model directly controls authorization. When ML models grant or deny access:
- A false negative (missed anomaly) results in unauthorized access going unchecked.
- A false positive (incorrect anomaly flag) results in legitimate access being denied, potentially disrupting safety-critical industrial operations.
- The model's reasoning is not inspectable, making it difficult to diagnose errors or satisfy compliance auditors.

In the proposed design, false negatives result in a missed alarm rather than a missed access control failure (the deterministic policy still governs access). False positives result in an unnecessary alert rather than an access denial (the user's access is not blocked). The model's reasoning is inspectable via SHAP and DiCE. The overall risk profile of the system is therefore bounded by the deterministic policy, with the ML layer providing supplemental awareness.

---

## V. LIMITATIONS AND FUTURE WORK

This paper presents a conceptual framework grounded in literature synthesis rather than an implemented and evaluated system. Several significant limitations should be acknowledged.

**Lack of empirical evaluation.** The framework has not been implemented or tested against real or synthetic access log data. The expected benefits described in Section IV are grounded in the supporting literature but have not been empirically validated for the specific architectural configuration proposed. Future work should include implementation of the framework using realistic enterprise or IIoT access logs, with evaluation of detection accuracy, false positive rates, explanation quality, and latency impact.

**Data constraints.** At the current stage of this research, a complete labeled dataset of IIoT access requests with known anomalies is not available. Acquiring or constructing such a dataset — whether through access to enterprise logs, synthetic data generation, or controlled simulation — is a prerequisite for empirical evaluation. Publicly available datasets (e.g., enterprise authentication logs, IIoT traffic captures) may serve as proxies, though they may not perfectly represent the access-level signals proposed in the framework.

**False positive and false negative analysis.** The practical utility of the ML risk alarm layer depends critically on its precision-recall characteristics. High false positive rates would generate alert fatigue; high false negative rates would reduce the layer's value as an anomaly warning mechanism. Empirical characterization of these rates under realistic operating conditions is essential.

**Adversarial robustness.** The ML layer, like any ML component, is potentially vulnerable to adversarial manipulation. A sophisticated attacker who understands the model's features could craft access patterns that avoid triggering risk flags while still pursuing malicious objectives. Adversarial robustness testing should be part of future evaluation.

**Explanation stability.** As noted in Section II-F, SHAP and LIME explanations can be unstable near decision boundaries [17] and can be adversarially manipulated [18]. For the proposed framework, boundary cases — where a request is near the risky/normal threshold — are precisely the cases where explanations are most needed and potentially least stable. Future work should evaluate explanation stability across the risk score distribution and explore robustness-aware explanation methods, such as those informed by Hessian curvature analysis of the explanation function's sensitivity.

**Scalability.** IIoT environments may generate high volumes of access requests. The ML evaluation and SHAP computation must scale to handle these volumes without introducing bottlenecks. TreeSHAP provides efficient computation for tree-based models, but scalability under realistic IIoT traffic loads should be empirically assessed.

**Future work directions include:**
- Implementation of the two-stage framework using a tree-based ML model (e.g., XGBoost) with TreeSHAP and DiCE.
- Evaluation on publicly available enterprise authentication datasets or synthetically generated IIoT access logs.
- User study with security analysts to assess the usefulness and usability of SHAP and DiCE explanations in a ZTA risk alarm context.
- Comparative analysis of the proposed layered architecture against direct ML authorization and deterministic-only approaches.
- Investigation of simulation-based or synthetic dataset generation approaches for controlled evaluation.

---

## VI. CONCLUSION

This paper has examined the intersection of Zero Trust Architecture, machine learning-based risk evaluation, and explainable AI in the context of Industrial IoT security. The literature synthesis reveals that while each of these areas has matured considerably, their integration — specifically, the design of an explainable, non-authoritative ML risk alarm layer that operates alongside deterministic ZTA policy enforcement — has not been adequately addressed.

The proposed two-stage framework offers a carefully reasoned architectural direction: deterministic policy retains sole authorization authority, ensuring auditability, predictability, and compliance readiness. A lightweight ML alarm layer evaluates contextual anomalies — device posture, geolocation, timing, behavioral deviation, request velocity, and session context — to flag requests that merit closer attention. SHAP provides feature-level attribution that helps analysts understand risk flags, while DiCE generates counterfactual analyses that support policy debugging and forensic investigation. Both explanation methods are positioned as offline, analyst-facing tools, reflecting the practical realities of latency constraints and the principle that explanations should inform rather than automate operational decisions.

This framework is particularly suited to IIoT environments, where device heterogeneity, safety requirements, and regulatory compliance create overlapping demands for both adaptive monitoring and transparent, deterministic control. As a conceptual contribution, the paper establishes a well-grounded direction for future empirical work, including implementation, dataset construction, and evaluation of detection accuracy, explanation quality, and analyst utility. By keeping the ML layer in an assistive role and making its reasoning inspectable, the proposed architecture seeks to capture the benefits of contextual intelligence without sacrificing the assurance properties that make Zero Trust effective.

---

## REFERENCES

[1] J. Kindervag, "Build Security Into Your Network's DNA: The Zero Trust Network Architecture," Forrester Research, Nov. 2010.

[2] S. Rose, O. Borchert, S. Mitchell, and S. Connelly, "Zero Trust Architecture," NIST Special Publication 800-207, National Institute of Standards and Technology, Aug. 2020. doi: 10.6028/NIST.SP.800-207.

[3] R. Mahmoud, T. Yousuf, F. Aloul, and I. Zualkernan, "Internet of Things (IoT) Security: Current Status, Challenges, and Prospective Measures," in *Proc. Int. Conf. Internet of Things (iThings)*, 2023.

[4] E. C. Nkoro, J. N. Njoku, C. I. Nwakanma, J.-M. Lee, and D.-S. Kim, "Zero-Trust Marine Cyberdefense for IoT-Based Communications: An Explainable Approach," *Electronics*, vol. 13, no. 2, p. 276, Jan. 2024. doi: 10.3390/electronics13020276.

[5] N. Capuano, G. Fenza, V. Loia, and C. Stanzione, "Explainable Artificial Intelligence in CyberSecurity: A Survey," *IEEE Access*, vol. 10, pp. 93575-93600, 2022. doi: 10.1109/ACCESS.2022.3204171.

[6] S. M. Lundberg and S.-I. Lee, "A Unified Approach to Interpreting Model Predictions," in *Proc. Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, 2017, pp. 4765-4774.

[7] R. K. Mothilal, A. Sharma, and C. Tan, "Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations," in *Proc. Conf. Fairness, Accountability, and Transparency (FAccT)*, Jan. 2020, pp. 607-617. doi: 10.1145/3351095.3372850.

[8] Department of Defense, "Department of Defense (DoD) Zero Trust Reference Architecture," Version 2.0, DISA and NSA, Jul. 2022.

[9] I. H. Sarker, M. H. Furhad, and R. Nowrozy, "AI-Driven Cybersecurity: An Overview, Security Intelligence Modeling and Research Directions," *SN Computer Science*, vol. 2, no. 3, p. 173, 2021. doi: 10.1007/s42979-021-00557-0.

[10] P. Fu, J. Wu, X. Lin, and A. Shen, "ZTEI: Zero-Trust and Edge Intelligence Empowered Continuous Authentication for Satellite Networks," in *Proc. IEEE GLOBECOM*, Dec. 2022, pp. 2376-2381. doi: 10.1109/GLOBECOM48099.2022.10000958.

[11] H. Liu, M. Ai, R. Huang, R. Qiu, and Y. Li, "Identity Authentication for Edge Devices Based on Zero-Trust Architecture," *Concurrency and Computation: Practice and Experience*, vol. 34, no. 26, p. e7198, 2022. doi: 10.1002/cpe.7198.

[12] V. Chandola, A. Banerjee, and V. Kumar, "Anomaly Detection: A Survey," *ACM Computing Surveys*, vol. 41, no. 3, pp. 1-58, Jul. 2009. doi: 10.1145/1541880.1541882.

[13] I. H. Sarker, M. H. Furhad, and R. Nowrozy, "AI-Driven Cybersecurity: An Overview, Security Intelligence Modeling and Research Directions," *SN Computer Science*, vol. 2, no. 3, p. 173, 2021.

[14] M. B. Salem and S. J. Stolfo, "Modeling User Search Behavior for Masquerade Detection," in *Proc. Int. Symp. Recent Advances in Intrusion Detection (RAID)*, Springer, 2008, pp. 181-200.

[15] M. Wang, K. Zheng, Y. Yang, and X. Wang, "An Explainable Machine Learning Framework for Intrusion Detection Systems," *IEEE Access*, vol. 8, pp. 73127-73141, 2020. doi: 10.1109/ACCESS.2020.2988359.

[16] S. Wachter, B. Mittelstadt, and C. Russell, "Counterfactual Explanations Without Opening the Black Box: Automated Decisions and the GDPR," *Harvard Journal of Law & Technology*, vol. 31, no. 2, pp. 841-887, 2018.

[17] D. Alvarez-Melis and T. Jaakkola, "On the Robustness of Interpretability Methods," in *Proc. ICML Workshop on Human Interpretability in Machine Learning*, 2018.

[18] D. Slack, S. Hilgard, E. Jia, S. Singh, and H. Lakkaraju, "Fooling LIME and SHAP: Adversarial Attacks on Post Hoc Explanation Methods," in *Proc. AAAI/ACM Conf. AI, Ethics, and Society (AIES)*, 2020, pp. 180-186. doi: 10.1145/3375627.3375830.
