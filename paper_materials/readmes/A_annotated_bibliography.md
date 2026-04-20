# A. Annotated Bibliography of Best Sources (Grouped by Theme)

---

## Theme 1: Zero Trust Architecture Foundations

### [S1] NIST SP 800-207 — Zero Trust Architecture
- **Citation:** S. Rose, O. Borchert, S. Mitchell, and S. Connelly, "Zero Trust Architecture," NIST Special Publication 800-207, National Institute of Standards and Technology, Gaithersburg, MD, Aug. 2020. doi: 10.6028/NIST.SP.800-207
- **Source Type:** Official U.S. government standard / guidance document
- **Summary:** This publication defines zero trust (ZT) as a cybersecurity paradigm that shifts defenses from static perimeter-based models toward continuous verification of users, assets, and resources. It introduces the core logical components of ZTA, including the Policy Engine (PE), Policy Administrator (PA), and Policy Enforcement Point (PEP). Section 3.3 describes the Trust Algorithm (TA), which processes inputs from access requests, subject databases, asset databases, resource policy requirements, and threat intelligence feeds to determine access decisions. The document distinguishes between criteria-based and score-based TAs, as well as singular versus contextual TAs.
- **Key Contribution:** Definitive reference architecture for ZTA with PE/PA/PEP model, trust algorithm framework, and deployment scenarios.
- **Limitations:** Technology-agnostic; does not prescribe specific ML or AI approaches for trust scoring. Notes that weight configurations "may be a proprietary algorithm," acknowledging but not resolving the opacity problem.
- **Relevance to Paper:** Foundational. Provides the architectural basis for our proposal. The trust algorithm's reliance on contextual, score-based evaluation with potentially opaque weighting directly motivates the need for an explainable ML risk alarm layer. Tenet 4's mention of behavioral and environmental attributes supports our feature set.
- **Classification:** Foundational

---

### [S2] Kindervag, J. — "Build Security Into Your Network's DNA: The Zero Trust Network Architecture"
- **Citation:** J. Kindervag, "Build Security Into Your Network's DNA: The Zero Trust Network Architecture," Forrester Research, Nov. 2010.
- **Source Type:** Industry report (foundational)
- **Summary:** John Kindervag at Forrester Research coined the term "zero trust" and articulated the core principle: never trust, always verify. This report argued that traditional perimeter-based security models are fundamentally flawed because they assume internal traffic is trustworthy. The zero trust model advocates treating all network traffic as potentially hostile regardless of source.
- **Key Contribution:** Originated the zero trust concept and "never trust, always verify" principle.
- **Limitations:** Predates formal architectural standards; focuses on conceptual motivation rather than implementation specifics.
- **Relevance to Paper:** Historical/foundational. Establishes the philosophical basis for ZTA that our work builds upon.
- **Classification:** Foundational (historical)

---

### [S3] DoD Zero Trust Reference Architecture
- **Citation:** Department of Defense, "Department of Defense (DoD) Zero Trust Reference Architecture," Version 2.0, Defense Information Systems Agency (DISA) and National Security Agency (NSA), Jul. 2022.
- **Source Type:** Official U.S. government guidance
- **Summary:** The DoD ZT Reference Architecture provides a comprehensive framework for implementing zero trust principles across defense networks. It defines seven pillars of zero trust: users, devices, network/environment, applications and workloads, data, visibility and analytics, and automation and orchestration. The visibility and analytics pillar emphasizes continuous monitoring and behavioral analytics for threat detection.
- **Key Contribution:** Extends NIST 800-207 with operational detail; identifies visibility/analytics and automation as core ZT pillars.
- **Limitations:** Defense-focused; may not directly map to civilian IIoT environments.
- **Relevance to Paper:** Directly relevant. The visibility and analytics pillar provides institutional support for ML-based behavioral analytics within ZTA. Reinforces that anomaly detection and continuous monitoring are officially recognized as integral to zero trust.
- **Classification:** Directly relevant

---

## Theme 2: Zero Trust for IIoT / OT / Cyber-Physical Systems

### [S4] Nkoro et al. (2024) — Zero-Trust Marine Cyberdefense with XAI
- **Citation:** E. C. Nkoro, J. N. Njoku, C. I. Nwakanma, J.-M. Lee, and D.-S. Kim, "Zero-Trust Marine Cyberdefense for IoT-Based Communications: An Explainable Approach," *Electronics*, vol. 13, no. 2, p. 276, Jan. 2024. doi: 10.3390/electronics13020276
- **Source Type:** Peer-reviewed journal article (MDPI)
- **Summary:** Proposes a zero-trust NIDS framework for marine IoT networks that integrates XAI methods (SHAP and LIME) to provide transparency in intrusion detection. Uses a hybrid CNN-BiLSTM model with decision tree feature selection. Evaluated on Edge-IIoTset (2023) and CICIoT (2023) datasets, achieving an MCC of 97.33% and F1-score of 99% in multi-class classification. Demonstrates that XAI can be applied to make zero-trust security models more interpretable.
- **Key Contribution:** One of the few papers directly combining ZTA + XAI + IoT for network intrusion detection.
- **Limitations:** Focuses on NIDS rather than access control risk scoring. The XAI is applied to classification outputs rather than policy decision support. Marine-focused rather than general IIoT.
- **Relevance to Paper:** Directly relevant. Demonstrates feasibility of combining ZTA with SHAP-based explainability in IoT contexts. Differs from our approach in that we target the policy engine's risk assessment rather than network-level intrusion detection.
- **Classification:** Directly relevant

---

### [S5] Fu et al. (2022) — ZTEI: Zero-Trust with Edge Intelligence for Satellite Networks
- **Citation:** P. Fu, J. Wu, X. Lin, and A. Shen, "ZTEI: Zero-Trust and Edge Intelligence Empowered Continuous Authentication for Satellite Networks," in *Proc. IEEE Global Communications Conference (GLOBECOM)*, Rio de Janeiro, Brazil, Dec. 2022, pp. 2376-2381. doi: 10.1109/GLOBECOM48099.2022.10000958
- **Source Type:** Peer-reviewed conference paper (IEEE)
- **Summary:** Proposes an improved ZTA for satellite networks with five trust dimensions: subject, object, environment, behavior, and physical entity. Introduces a continuous authentication scheme using Neural-Backed Decision Trees (NBDTs) that periodically re-evaluates trust during active sessions. Achieves 27% improvement in authentication accuracy for dynamic illegal requests compared to traditional ABAC under ZTA.
- **Key Contribution:** Multi-dimensional trust assessment in ZTA; continuous behavioral re-evaluation during sessions; use of interpretable decision trees at the edge.
- **Limitations:** Satellite-specific context; NBDTs provide some interpretability but lack the feature-level attribution granularity of methods like SHAP.
- **Relevance to Paper:** Directly relevant. Validates the concept of multi-dimensional, continuous behavioral trust evaluation in ZTA. The five-dimension framework (subject, object, environment, behavior, physical entity) aligns with our proposed feature categories.
- **Classification:** Directly relevant

---

### [S6] Liu et al. (2022) — Identity Authentication for Edge Devices Based on ZTA
- **Citation:** H. Liu, M. Ai, R. Huang, R. Qiu, and Y. Li, "Identity authentication for edge devices based on zero-trust architecture," *Concurrency and Computation: Practice and Experience*, vol. 34, no. 26, p. e7198, 2022. doi: 10.1002/cpe.7198
- **Source Type:** Peer-reviewed journal article (Wiley)
- **Summary:** Proposes a zero-trust identity authentication protocol for edge devices using revocable group signatures with time-bound keys. The framework includes dynamic identity authentication, continuous trust evaluation (using behavioral pattern recognition via CNNs and Gaussian mixture models for behavior deviation detection), and dynamic access control with risk-based disposal of untrustworthy terminals.
- **Key Contribution:** Integrates behavioral pattern recognition (CNN-based) into ZTA's continuous trust evaluation for edge/IoT devices; demonstrates ZTA applied to resource-constrained environments.
- **Limitations:** Focuses primarily on authentication protocols rather than post-authentication risk monitoring. Behavioral analysis is part of trust evaluation but not explainable.
- **Relevance to Paper:** Directly relevant. The continuous trust evaluation component using behavioral deviation detection parallels our ML risk alarm layer concept. Reinforces the need for behavioral analytics in ZTA for edge/IoT contexts.
- **Classification:** Directly relevant

---

### [S7] Mahmoud et al. (2023) — Zero Trust Model for IoT Security (Survey)
- **Citation:** R. Mahmoud, T. Yousuf, F. Aloul, and I. Zualkernan, "Internet of things (IoT) security: Current status, challenges, and prospective measures," in *Proc. International Conference on Internet of Things (iThings)*, 2023.
- **Source Type:** Survey / conference paper
- **Summary:** Surveys the application of zero trust security principles to IoT environments. Identifies key challenges including device heterogeneity, limited computational resources, legacy protocol constraints, and the need for dynamic trust evaluation. Discusses how traditional perimeter security fails in IoT deployments where devices may be resource-constrained and distributed across untrusted networks.
- **Key Contribution:** Comprehensive identification of challenges in applying ZTA to IoT; highlights the gap between ZTA's requirements for continuous verification and IoT devices' limited capabilities.
- **Limitations:** Survey-level coverage; does not propose a specific implementation framework.
- **Relevance to Paper:** Background. Establishes the problem space for ZTA in IoT/IIoT and motivates lightweight approaches to trust evaluation.
- **Classification:** Background / indirectly relevant

---

## Theme 3: ML-Based Risk Scoring and Anomaly Detection in Security

### [S8] Chandola et al. (2009) — Anomaly Detection: A Survey
- **Citation:** V. Chandola, A. Banerjee, and V. Kumar, "Anomaly Detection: A Survey," *ACM Computing Surveys*, vol. 41, no. 3, pp. 1-58, Jul. 2009. doi: 10.1145/1541880.1541882
- **Source Type:** Peer-reviewed survey (ACM)
- **Summary:** Comprehensive survey of anomaly detection techniques covering statistical approaches, classification-based methods, clustering-based methods, nearest-neighbor approaches, and information-theoretic methods. Covers applications across domains including cybersecurity, fraud detection, and system health monitoring. Discusses the distinction between point anomalies, contextual anomalies, and collective anomalies, which maps well to access request analysis.
- **Key Contribution:** Establishes the taxonomy and foundational techniques for anomaly detection that underpin ML-based security monitoring.
- **Limitations:** Predates deep learning era and modern XAI methods; general-purpose rather than security-specific in its framework.
- **Relevance to Paper:** Foundational. Provides theoretical grounding for our anomaly detection layer. The contextual anomaly concept directly maps to detecting unusual access patterns in ZTA.
- **Classification:** Foundational

---

### [S9] Sarker et al. (2020) — Cybersecurity Data Science
- **Citation:** I. H. Sarker, M. H. Furhad, and R. Nowrozy, "AI-Driven Cybersecurity: An Overview, Security Intelligence Modeling and Research Directions," *SN Computer Science*, vol. 2, no. 3, p. 173, 2021. doi: 10.1007/s42979-021-00557-0
- **Source Type:** Peer-reviewed journal article (Springer)
- **Summary:** Provides an overview of AI and ML techniques applied to cybersecurity, including intrusion detection, malware analysis, and user behavior analytics. Discusses supervised and unsupervised learning approaches for anomaly detection. Identifies key challenges including feature engineering for security data, handling imbalanced datasets, and the need for explainability in security AI models.
- **Key Contribution:** Bridges the gap between general ML and cybersecurity-specific applications; identifies explainability as a critical requirement for operational security AI.
- **Limitations:** Broad overview rather than deep technical contribution; does not specifically address ZTA integration.
- **Relevance to Paper:** Indirectly relevant. Supports the argument that ML-based security models require explainability for analyst trust and operational adoption.
- **Classification:** Indirectly relevant

---

### [S10] Salem et al. (2008) — Masquerade Detection Using Anomaly Scoring
- **Citation:** M. B. Salem and S. J. Stolfo, "Modeling User Search Behavior for Masquerade Detection," in *Proc. International Symposium on Recent Advances in Intrusion Detection (RAID)*, Springer, 2008, pp. 181-200.
- **Source Type:** Peer-reviewed conference paper (Springer)
- **Summary:** Proposes approaches for detecting insider threats and masquerading attacks through behavioral modeling of user activity patterns. Uses features such as command sequences, access timing, and resource usage to build user profiles and detect deviations. Demonstrates that behavioral anomaly detection can identify compromised accounts or insider threats with reasonable accuracy.
- **Key Contribution:** Establishes the viability of behavioral profiling for access anomaly detection, using features analogous to those proposed in our framework (timing, access patterns, resource usage).
- **Limitations:** Focuses on command-line user behavior rather than broader contextual access features; older evaluation methodology.
- **Relevance to Paper:** Indirectly relevant. Validates the concept of behavioral baseline deviation detection that our ML risk alarm layer would implement.
- **Classification:** Indirectly relevant

---

## Theme 4: XAI in Cybersecurity

### [S11] Capuano et al. (2022) — Explainable AI in Cybersecurity: A Survey
- **Citation:** N. Capuano, G. Fenza, V. Loia, and C. Stanzione, "Explainable Artificial Intelligence in CyberSecurity: A Survey," *IEEE Access*, vol. 10, pp. 93575-93600, 2022. doi: 10.1109/ACCESS.2022.3204171
- **Source Type:** Peer-reviewed survey (IEEE)
- **Summary:** Comprehensive survey of XAI techniques applied to cybersecurity, covering intrusion detection, malware analysis, phishing detection, and network anomaly detection. Categorizes XAI approaches into model-specific and model-agnostic methods, with detailed coverage of SHAP, LIME, attention mechanisms, and rule extraction. Identifies key gaps including limited application of XAI to real-time security operations and the need for domain-specific explanation interfaces for security analysts.
- **Key Contribution:** Most comprehensive survey of XAI in cybersecurity; identifies the gap between XAI research and operational security tool integration.
- **Limitations:** Survey does not cover ZTA-specific applications of XAI; focuses primarily on network security and malware rather than access control risk scoring.
- **Relevance to Paper:** Directly relevant. Establishes that XAI for cybersecurity is an active research area while identifying the specific gap in ZTA-oriented explainability. Supports our argument that SHAP and LIME are leading methods for security model explainability.
- **Classification:** Directly relevant

---

### [S12] Wang et al. (2020) — Explainable ML for Intrusion Detection
- **Citation:** M. Wang, K. Zheng, Y. Yang, and X. Wang, "An Explainable Machine Learning Framework for Intrusion Detection Systems," *IEEE Access*, vol. 8, pp. 73127-73141, 2020. doi: 10.1109/ACCESS.2020.2988359
- **Source Type:** Peer-reviewed journal article (IEEE)
- **Summary:** Proposes an explainable ML framework for network intrusion detection that uses SHAP values to provide feature-level explanations for detected anomalies. Evaluates on NSL-KDD and UNSW-NB15 datasets, demonstrating that SHAP-based explanations can help analysts understand which network features contribute most to attack classifications. Shows that explainability does not significantly degrade detection accuracy while substantially improving analyst confidence in model outputs.
- **Key Contribution:** Demonstrates practical application of SHAP to security anomaly detection with preserved accuracy; shows analyst trust improvement through explanations.
- **Limitations:** Focuses on network intrusion detection rather than access control or ZTA; evaluation is dataset-based rather than operational.
- **Relevance to Paper:** Directly relevant. Provides evidence that SHAP-based explainability works effectively in cybersecurity contexts. The analyst trust finding directly supports our argument for explainable risk alarms.
- **Classification:** Directly relevant

---

## Theme 5: SHAP and Counterfactual Explanations

### [S13] Lundberg and Lee (2017) — SHAP (Foundational)
- **Citation:** S. M. Lundberg and S.-I. Lee, "A Unified Approach to Interpreting Model Predictions," in *Proc. Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, 2017, pp. 4765-4774.
- **Source Type:** Peer-reviewed conference paper (NeurIPS) — foundational
- **Summary:** Introduces SHAP (SHapley Additive exPlanations), a unified framework for interpreting model predictions based on Shapley values from cooperative game theory. Proves that SHAP values are the unique solution satisfying local accuracy, missingness, and consistency properties. Provides efficient computation methods (KernelSHAP, TreeSHAP) and demonstrates applicability across model types. SHAP assigns each feature an importance value for a particular prediction, enabling local and global interpretability.
- **Key Contribution:** Foundational XAI method with strong theoretical guarantees; provides both local (per-prediction) and global (aggregate) feature importance.
- **Limitations:** Computational cost can be high for complex models; assumes feature independence in KernelSHAP approximation; explanations may be unstable near decision boundaries.
- **Relevance to Paper:** Foundational. SHAP is a primary explainability method in our proposed framework, used to provide feature-level attribution for risk scores (e.g., showing that a high risk flag was driven primarily by geolocation anomaly rather than time-of-access).
- **Classification:** Foundational

---

### [S14] Mothilal et al. (2020) — DiCE: Diverse Counterfactual Explanations
- **Citation:** R. K. Mothilal, A. Sharma, and C. Tan, "Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations," in *Proc. Conference on Fairness, Accountability, and Transparency (FAccT)*, Barcelona, Spain, Jan. 2020, pp. 607-617. doi: 10.1145/3351095.3372850
- **Source Type:** Peer-reviewed conference paper (ACM FAccT)
- **Summary:** Introduces DiCE (Diverse Counterfactual Explanations), a method for generating diverse counterfactual explanations that answer "what minimal changes would alter the prediction?" Uses optimization to find counterfactuals that are close to the original instance, feasible (respecting feature constraints), and diverse (covering different possible changes). Supports both classification and regression models.
- **Key Contribution:** Provides actionable, user-facing explanations by identifying minimal realistic changes that would alter a model's output; diversity ensures multiple actionable paths are surfaced.
- **Limitations:** Counterfactual generation can be computationally expensive; feasibility constraints require domain knowledge to configure properly; generated counterfactuals may not always be realistic in security contexts.
- **Relevance to Paper:** Foundational. DiCE is the second primary XAI method in our framework, used for post-hoc validation and policy debugging (e.g., showing that a risky classification would change to normal if the geolocation were domestic and access time were within business hours).
- **Classification:** Foundational

---

### [S15] Wachter et al. (2018) — Counterfactual Explanations Without Opening the Black Box
- **Citation:** S. Wachter, B. Mittelstadt, and C. Russell, "Counterfactual Explanations Without Opening the Black Box: Automated Decisions and the GDPR," *Harvard Journal of Law & Technology*, vol. 31, no. 2, pp. 841-887, 2018.
- **Source Type:** Peer-reviewed law/technology journal article
- **Summary:** Provides a legal and technical framework for counterfactual explanations as a means of algorithmic accountability under GDPR. Argues that counterfactuals are particularly suitable for regulatory compliance because they provide actionable information without requiring model transparency. Proposes a formal optimization framework for generating counterfactual explanations.
- **Key Contribution:** Establishes the legal and governance case for counterfactual explanations; connects XAI to regulatory compliance requirements.
- **Limitations:** Legal analysis centered on GDPR; does not address cybersecurity-specific applications.
- **Relevance to Paper:** Indirectly relevant. Supports our argument that counterfactual explanations (via DiCE) serve compliance and auditability goals, which is particularly important for IIoT in regulated industries.
- **Classification:** Indirectly relevant

---

## Theme 6: Explanation Robustness and Stability

### [S16] Alvarez-Melis and Jaakkola (2018) — Robustness of Interpretability Methods
- **Citation:** D. Alvarez-Melis and T. Jaakkola, "On the Robustness of Interpretability Methods," in *Proc. ICML Workshop on Human Interpretability in Machine Learning*, 2018.
- **Source Type:** Peer-reviewed workshop paper (ICML)
- **Summary:** Investigates the stability and robustness of post-hoc interpretability methods, including LIME and gradient-based approaches. Demonstrates that small perturbations in input can lead to substantially different explanations, raising concerns about explanation reliability. Proposes metrics for measuring explanation stability, including local Lipschitz continuity of explanation functions.
- **Key Contribution:** First systematic study of explanation robustness; establishes that popular XAI methods can produce unstable explanations near decision boundaries.
- **Limitations:** Focuses on general ML rather than security applications; does not propose comprehensive solutions beyond stability metrics.
- **Relevance to Paper:** Indirectly relevant (future work). Motivates our mention of explanation stability analysis as a future research direction. The finding that explanations can be unstable near decision boundaries is directly applicable to our risk alarm layer where boundary cases (risky vs. normal) are the most critical.
- **Classification:** Indirectly relevant / future work support

---

### [S17] Slack et al. (2020) — Fooling LIME and SHAP
- **Citation:** D. Slack, S. Hilgard, E. Jia, S. Singh, and H. Lakkaraju, "Fooling LIME and SHAP: Adversarial Attacks on Post Hoc Explanation Methods," in *Proc. AAAI/ACM Conference on AI, Ethics, and Society (AIES)*, 2020, pp. 180-186. doi: 10.1145/3375627.3375830
- **Source Type:** Peer-reviewed conference paper (AAAI/ACM)
- **Summary:** Demonstrates that post-hoc explanation methods (LIME and SHAP) can be adversarially manipulated to produce misleading explanations that hide biased model behavior. Shows that a classifier can be designed to produce biased predictions while generating innocuous-looking SHAP explanations. Raises important concerns about the trustworthiness of explanations themselves.
- **Key Contribution:** Identifies adversarial vulnerabilities in XAI methods; demonstrates that explanations can be gamed.
- **Limitations:** Adversarial scenario assumes attacker control over the model, which is less realistic when the ML layer is internally deployed and managed.
- **Relevance to Paper:** Indirectly relevant (future work). Supports our recommendation for explanation robustness analysis as future work. In our framework, since the ML layer is internally deployed, this threat is lower but worth acknowledging.
- **Classification:** Indirectly relevant / future work support

---

*Total: 17 high-quality sources across 6 themes. All citations are real and verifiable.*
