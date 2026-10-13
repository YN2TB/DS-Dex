---
subject: MLOps
chapter: 06
tags: [ds, mlops, deployment, edge-ai, canary, ab-testing, model-risk]
source: "MLOPs_Deployment.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# ML System Deployment

The fourth lifecycle stage. [[05 - Packaging Models with FastAPI and Docker]] put the model in a container; this chapter decides where it runs, when it predicts and how it is released, and covers **model risk**: what happens when it is wrong.

## 📘 Main Knowledge

### Two kinds of challenge

At deployment the model is integrated into production systems and workflows (Paleyes et al., 2022):
- **Software engineering**: compatibility, scalability, operational constraints.
- **Statistical**: data and concept drift, which ordinary software doesn't have.

User requirements drive system design, and system design drives technology choice: compute (CPU/GPU/memory), latency and throughput, logging, privacy and security.

### Cloud vs edge

**Edge AI** runs models on the device, made possible by better power efficiency, more on-device compute and smaller models. It removes network latency: every 100 miles from a datacenter adds more than 1.6 ms (a round trip at the speed of light in fibre).

| | Cloud ML | Edge ML |
|---|---|---|
| Computation | in the cloud, results sent back | on the device |
| Needs | connectivity | enough local compute and memory |
| Benefits | high throughput | low latency, privacy, offline use |
| Examples | chatbots, demand prediction | quality control, autonomous driving |

Hybrids: edge triggers start cloud inference (a smart speaker detects the wake word on-device, understands speech in the cloud); store common predictions locally; use several nearby datacenters.

Three questions: Does latency matter a lot? Is relying on the internet unacceptable? Will users refuse to send data away? Each "yes" points to the edge. Edge deployment needs the quantization, pruning and compression of EdgeOps ([[01 - Introduction to MLOps]]).

### Learning vs prediction modes

**Online learning** updates the model incrementally with each new data point ("data in motion"), instead of in retraining cycles.

Prediction is a separate axis; the most common setup trains offline and predicts online.

| | Batch prediction | Online prediction |
|---|---|---|
| When | recurring schedule | on request, in real time |
| Output | stored in a database | returned immediately |
| Latency | rarely a concern | critical |
| Complexity | lower | higher: feature retrieval, inference time, output validation, web stack |
| Example | recommendations | food-delivery arrival time |

### Big data

Volume (rows and variables), velocity (speed of accumulation), variety (images, audio, text, changing over time). Challenges: storage, compute cost, understanding quality, data too large for memory ([[Big Data Analytics/contents/00-Index|Big Data Analytics]]).

### Preparing for production

Environments: custom services, dedicated platforms (TensorFlow Serving), low-level infrastructure (Kubernetes, [[07 - Kubernetes for ML Deployment]]), embedded systems (JVMs). Validate in an environment that mimics production as closely as possible, not in development (the reason for identical images across environments in [[02 - Environment Setup]]).

### Model risk

**Model risk** arises when a model used for quantitative prediction performs inadequately, leading to regulatory scrutiny, non-compliance, and reputational and financial loss. Ask: what if the model acts in the worst imaginable way? What if someone extracts the training data or the logic?

| Source | Example |
|---|---|
| Data | outdated market data; a hiring model trained on a mostly male workforce favours men |
| Assumptions and variables | unrealistic assumptions; wrong, missing or irrelevant variables; bad calibration |
| Methodology | sampling and standard errors in regression |
| Implementation | programming or approximation errors |
| Interpretation | misread output → wrong decisions |
| Usage | a lung-condition model built for children used on adults |

The last row is the subtle one: model and code are correct, the use is not.

Management: (1) catalogue all models with purpose, data, assumptions, risks; (2) assess quantitatively (simulation, extreme value theory), qualitatively (expert review) and for data quality; (3) mitigate with monitoring, risk limits, user training and governance.

Credit-scoring example:

| Risk | Issue | Evaluation |
|---|---|---|
| Data | outdated data underestimates default in downturns | compare training vs recent distributions |
| Statistical | overfits history | cross-validation, stress tests with synthetic edge cases, stability over time slices |
| Concept drift | behaviour changes after policy or rate changes | default rate by prediction bucket, Population Stability Index (PSI) |
| Operational | training/production feature mismatch: wrong predictions from a good model | training–serving skew checks, end-to-end validation |
| Ethical / compliance | decisions correlate with protected attributes | fairness metrics (disparate impact), SHAP audits |

Model risk goes beyond accuracy to data quality, robustness, deployment and ethics.

### Deployment strategies

| Strategy | How | Best for | Limitations |
|---|---|---|---|
| **Shadow** | new model runs alongside, its output not used | validation; finance, healthcare | no user feedback; doubles inference cost |
| **Canary** | small share of traffic first, then widen | online systems, A/B tests | needs routing and monitoring; some users still hit failures |
| **Blue–green** | two identical environments; switch all traffic at once | zero downtime, instant rollback | duplicate infrastructure; weak for live evaluation |
| **Rolling** | replace instances gradually | large distributed systems, frequent updates | harder rollback; temporary inconsistency |

No strategy is best in general: it depends on risk tolerance, criticality and monitoring maturity.

### A/B testing

Randomly assign users or requests to variants and compare with a hypothesis test ([[Mathematical Statistics/contents/08 - Inferences on Two Samples|Inferences on Two Samples]]):
1. Question: do sites A and B convert at different rates?
2. $H_0$: same rate; $H_1$: different.
3. Test and level: z-test, α = 0.05.
4. Collect data with random assignment.
5. Compute the statistic and p-value.
6. Evaluate.

Random assignment makes the groups differ only by chance, so a significant difference can be attributed to the variant.

## ✏️ Exercises

**1.** (Slide 15 quiz) Cloud or edge? (1) drone navigation; (2) face recognition on a phone; (3) a chatbot for millions; (4) industrial robot collision avoidance; (5) monthly sales trend analysis.

> [!example]- Solution
> Edge: 1, 2, 4. Cloud: 3, 5.
> (1) and (4) are safety-critical control loops: a robot at 2 m/s moves 4 mm in 2 ms of round trip, and both must work when the network drops. (2) is biometric data, a privacy question. (3) needs a large model and elastic throughput, and a few hundred ms is fine in conversation. (5) is a monthly batch job.
> Latency, connectivity and privacy push to the edge; model size and throughput pull to the cloud.

**2.** (Slide 24 quiz) Batch or online prediction? (1) real-time fraud detection; (2) autonomous vehicle perception; (3) daily sales forecasting; (4) voice assistants; (5) YouTube recommendations.

> [!example]- Solution
> Online: 1, 2, 4 (the input arrives with the request). Batch: 3 (compute overnight; batch is simpler, so prefer it when possible). (5) is mostly batch: candidates are precomputed per user, then a light online layer re-ranks them with session context, a hybrid.
> The axes are independent: (2) is online and edge, (1) online and cloud.

**3.** (Slides 50–51 quizzes) (a) Is deployment a high-stakes event to get right at once, or an iterative process? (b) A bank logs a loan model's output but a human officer decides. Which deployment type is this?

> [!example]- Solution
> (a) Iterative: expect to adjust monitored metrics and traffic shares. Production reveals the real distribution and edge cases, which is why canary and shadow exist.
> (b) Shadow: the model runs in parallel and its output drives no decision. Lending is the risk-sensitive case it suits, and the officers' decisions become labels. The cost: you never see whether the model's approvals would have been repaid.

**4.** In the credit example, how can operational risk defeat a model that passes every statistical check?

> [!example]- Solution
> Validation uses features from the training pipeline; the defect lives in the serving pipeline. Example: training computes debt-to-income from annual income, the live API supplies monthly income, so production ratios are 12× larger than anything seen in training. Other cases: different category encodings, a 30-day vs 7-day window, median vs zero imputation.
> It fails silently and can look like drift, so the team retrains for nothing. Defences: skew checks (run the same input through both pipelines and compare feature vectors), end-to-end validation, a feature store or a single packaged preprocessor ([[05 - Packaging Models with FastAPI and Docker]]).

**5.** (Advanced) Design a release plan for a new credit model at a regulated bank.

> [!example]- Solution
> 1. **Shadow** (weeks): the new model scores every live application; the incumbent decides. Exit when agreement is within tolerance, no skew, fairness passes, latency within SLA.
> 2. **A/B test on a 5% canary**, randomly assigned (assigning by branch or time would confound region or season). Two-proportion z-test on default rates. Size it in advance: detecting 3.0% vs 3.5% at α = 0.05 with 80% power needs about 19,700 applications per arm. Defaults take months or years to appear, so use 30/60/90-day delinquency, approval rate and PSI as leading indicators, and analyse true outcomes later.
> 3. **Widen gradually** (25% → 50% → 100%) with automatic rollback on approval-rate or fairness deviations.
> 4. **Blue–green cutover**, keeping the old environment warm for slow-emerging problems.
>
> Throughout: a model catalogue entry, SHAP explanations for rejections, disparate-impact monitoring at every stage, and documented sign-off before each traffic increase ([[09 - CI-CD with GitHub Actions]]). Each stage buys information at a bounded risk.

## 📝 Summary

- Deployment has software and statistical challenges; requirements → design → technology.
- Edge for latency, privacy, offline use; cloud for throughput and large models.
- Batch vs online prediction is separate from offline vs online learning; prefer batch when possible.
- Validate in a production-like environment.
- Model risk: data, assumptions, methodology, implementation, interpretation, usage.
- Shadow, canary, blue–green, rolling: choose by risk tolerance and monitoring maturity.
- A/B testing is hypothesis testing with random assignment.
- Deployment is iterative.

## ⚠️ Important Notes

1. Don't plan for a perfect launch; plan to adjust.
2. Most systems train offline and predict online.
3. Online serving adds feature retrieval, latency budgets and output validation.
4. Shadow gives no feedback on whether disagreements were right, and doubles cost.
5. Canary failures still reach some users.
6. Rolling deployments are hard to roll back.
7. Training–serving mismatch defeats statistically sound models.
8. A model used outside its population is a risk in itself.
9. A/B tests need random assignment and a sample size fixed in advance; stopping when results look good inflates Type 1 error.
10. Delayed labels can outlast the test; use leading indicators.
11. Monitor fairness at every rollout stage.
12. Network latency matters for control loops, not chatbots.

> [!warning] Gaps in the source slides
> - Slides 3, 27, 31, 39 have no text. Slides 7, 8, 10 (system design and edge examples), 16 and 22 (learning and prediction comparisons; the batch/online table above is rebuilt from the bullets), 28 (preparing for production, after Treveil 2020) and 40 (deployment approaches) are images or titles only. Slides 12, 13, 17, 18, 23 are figures.
> - Truncated: slides 32–35, and slide 53, where A/B step 6 is cut off.
> - Slide 54's demo notebook is not in `documents/`.
> - Exercise 5's plan and its sample size (two-proportion formula, verified with scipy) are mine.
> - References: Treveil et al.; Gift & Deza; Paleyes, Urma & Lawrence (2022), *ACM Computing Surveys* 55(6).

**Previous:** [[05 - Packaging Models with FastAPI and Docker]] · **Next:** [[07 - Kubernetes for ML Deployment]]
