---
subject: MLOps
chapter: 03
tags: [ds, mlops, data-engineering, data-quality, governance, scoping]
source: "MLOPs_data.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Data in MLOps: Data Stage and Scoping

The second lifecycle stage from [[01 - Introduction to MLOps]]. [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]] covers cleaning techniques; this chapter treats data as an engineering and governance problem, and asks whether the project should exist at all.

## 📘 Main Knowledge

### Two pipelines

- **Data pipeline**: collection → ingestion → analysis → labeling → validation → preparation → ML-ready data.
- **Model pipeline**: training → evaluation → validation → deployment → production.

Deployment insights feed back into data refinement.

### Model-centric vs data-centric AI

| Aspect | Model-centric | Data-centric |
|---|---|---|
| Focus | architectures, algorithms | data quality, consistency, coverage |
| Iterate on | design, hyperparameters | collection, labeling, cleaning, augmentation |
| Assumes | data fixed | model roughly fixed |
| Techniques | deeper networks, ensembles, architecture search | cleaning, relabeling, balancing, augmentation |
| Scales | limited by model size and compute | without growing the model |

In most production settings the data-centric route gives more improvement per unit of effort (Andrew Ng's argument).

### Data and data engineering

Data is structured (tables), semi-structured (JSON, logs) or unstructured (text, images, audio, video), labeled or not, from sensors, users, systems or experiments.

**Data engineering** designs and maintains the infrastructure that turns raw data into reliable, accessible, analysis-ready datasets. "No algorithm can overcome poor data, but excellent data engineering enables even simple models to achieve remarkable results." Software engineering produces code, APIs and services; data engineering produces pipelines, warehouses, lakes and ETL/ELT workflows.

### Four pillars at each stage

| Stage | Quality | Reliability | Scalability | Governance |
|---|---|---|---|---|
| Acquisition | representative sampling, bias detection | diverse, redundant sources | scraping, synthetic data | consent, anonymization, ethical sourcing |
| Ingestion | schema validation, profiling | dead letter queues, graceful degradation | batch vs stream, autoscaling | access control, audit logs, lineage |
| Processing | consistency checks, **training–serving parity** | idempotent transforms, retries | distributed frameworks | (truncated in source) |

Training–serving parity is the feature-store requirement from the fraud case in ch. 01.

### Data cascades and reliability

**Data cascades** (Sambasivan et al., 2021, "Everyone wants to do the model work, not the data work"): poor data quality early on amplifies through the pipeline into model failures, cancelled projects and user harm. This argues for investing in data work up front.

Reliable data gives stable, accurate, reproducible models; good models can't compensate for bad data. Common issues: missing, incorrect (sensor errors, wrong labels), inconsistent (schema changes), duplicated, outdated data. Causes: integration problems, human error, system limits, poor governance. These degrade models silently. **Label inconsistency** (annotators labelling the same input differently) caps achievable accuracy.

| | Data reliability | Model reliability |
|---|---|---|
| What | consistency of data over time | trustworthy predictions on unseen data |
| Focus | completeness, accuracy, freshness | metrics, robustness to drift |
| Example | sales totals unchanged when no new sales occur | fraud model reliable across users and days |

### Types of data problems

| | Structured | Unstructured |
|---|---|---|
| Small data | grades, credit approval with 100 examples, small-shop sales | medical images, small fruit-image set, spam with 200 examples |
| Big data | e-commerce or airline demand, stock prices | image search over billions of photos, speech streams, social media text |

Complexity grows with size and lack of structure. A strategy that works for thousands of examples can be unaffordable for millions, and production often needs continuous collection.

### Acquisition

- **Web scraping**: large scale; limited by terms of service, copyright, rate limits, inconsistent data.
- **Crowdsourcing**: ImageNet (Mechanical Turk), Waze (traffic reports), reCAPTCHA (verifies humans while labeling data). Tasks can be adjusted as results come in.
- **Synthetic data**: unlimited examples without human labor; useful where real data is rare or costly (e.g. car crashes).

Speech recognition example:

| Source | Amount | Cost | Time | Cost per hour |
|---|---|---|---|---|
| owned | 100 h | \$0 | 0 | \$0 |
| crowdsourced reading | 1000 h | \$10,000 | 14 days | \$10 |
| paid labels | 100 h | \$6,000 | 7 days | \$60 |
| purchased | 1000 h | \$10,000 | 1 day | \$10 |

Also weigh quality, privacy and regulation. Who can label: domain experts, reasonable annotators, or almost no one, depending on the task (speech, medical images, recommendations, legal judgments).

### Ingestion: batch vs stream

**Batch**: collect, then process on a schedule; amortizes startup cost (a retailer updates inventory models overnight). **Stream**: process events as they arrive when data loses value quickly (a bank flags each transaction). Streams must handle **backpressure** (data arriving faster than it can be processed) and meet **freshness SLAs** (maximum delay from generation to availability).

| Aspect | Batch | Stream |
|---|---|---|
| Timing | periodic | real time |
| Latency | minutes to hours | ms to seconds |
| Uses | reports, training | fraud, monitoring, alerts |
| Complexity | lower | higher |
| Tools | SQL, Hadoop, Spark | Kafka, Spark Streaming, Flink |
| Failures | rerun the batch | handle lost or late events |

### Distributed processing

Split data and computation across nodes: 1 TB in 10 hours on one machine becomes 100 GB each on 10 machines in about an hour, with a coordinator assigning tasks. Costs: coordination overhead and network latency (local operations take microseconds, network coordination milliseconds). Tools: Hadoop, Spark; Kafka, Flink; AWS EMR, Google Dataflow, Azure Databricks. More in [[Big Data Analytics/contents/00-Index|Big Data Analytics]].

### Governance

Know what data flows through the system, how it is transformed and who accesses it; stay within ethical, legal and business limits; be transparent and accountable; protect privacy. These shape design from the start.

- **Lineage**: the provenance of each dataset: raw sources, transformations and when, processing code version. Needed for debugging and reproducibility, and to know what breaks when upstream data changes.
- **Audit trails**: who accessed data and when; required by GDPR and CCPA.

### Scoping

Separate the **problem** (what to achieve) from the **solution** (how):

| Problem | Solutions |
|---|---|
| increase conversion | search, recommendations |
| reduce inventory | demand prediction, marketing |
| increase margin | merchandising, bundles |

**Feasibility** uses external benchmarks:

| | Structured | Unstructured |
|---|---|---|
| New project | are predictive features available? | human-level performance (HLP) |
| Existing project | new features, project history | HLP, project history |

For images, audio and text, humans can do the task, so HLP is a benchmark. Structured problems often have no human baseline, so ask whether predictive features exist: past purchases → future purchases ✓; weather → mall traffic ✓; DNA → heart disease ?; social media → clothing demand ?; a stock's price history → its future price ✗. Ask also about signal, stability over time and ethical or causal limits.

**Stages:**

| Stage | Question | Audience | Output |
|---|---|---|---|
| PoC | can it be built? | internal, technical | simple demo; about 20% of the journey |
| Prototype | how does it work and look? | users, investors | UI, user flow, feedback |
| MVP | do the core assumptions hold? | early adopters | minimal core features, fast learning |
| Production | deliver value at scale | broad market | full features, robust, secure, scalable |

## ✏️ Exercises

**1.** (Slide 21 quiz) Data or model problem? (1) Face recognition degrades after a camera upgrade. (2) A spam classifier predicts "not spam" for almost everything. (3) Last year's credit model underestimates defaults this year. (4) Good on training data, poor on test. (5) An image classifier fails on rotated or dark images.

> [!example]- Solution
> 1. Data: data drift (new camera, new $P(X)$); fine-tune on new images.
> 2. Data: class imbalance; reweight or rebalance, and use PR-AUC.
> 3. Data: concept drift ($P(Y\mid X)$ moved with the economy); retrain on recent data.
> 4. Model: overfitting; regularize, simplify, cross-validate.
> 5. Data: missing coverage; augment with rotations and brightness changes.
>
> Four of five are data problems, which is the case for data-centric AI.

**2.** (Slides 45–46 quiz) Highly predictive, weakly predictive, or not predictive/leaky? Houses: size, wall colour, ZIP code. Students: hours studied, student ID, attendance. Credit: repayment history, browser type, utilization. Fraud: amount, time of day, label added after investigation.

> [!example]- Solution
> | Feature | Verdict |
> |---|---|
> | house size, ZIP code | highly predictive |
> | wall colour | not predictive |
> | hours studied, attendance | highly predictive |
> | student ID | not predictive (an identifier) |
> | repayment history, utilization | highly predictive |
> | browser type | weak at best |
> | amount, time of day | weak to moderate |
> | label added after investigation | **leaky** |
>
> The investigation label exists only after the outcome is known, so the model looks excellent in testing and is useless in production. Test: would I have this value when I need to predict? Unlike the fit-before-split leakage of [[Data Preparation and Visualization/contents/04 - Foundations of Data Preparation for ML|Foundations of Data Preparation]], this target leakage is inside the feature, and no split discipline catches it.
> ZIP code can proxy race and income, and browser type device cost (income): whether to use them is a governance question.

**3.** What are data cascades, and why is the paper titled "Everyone wants to do the model work, not the data work"?

> [!example]- Solution
> An early data defect amplifies downstream. Example: an ambiguous labeling guideline → annotators disagree → the model plateaus → the team tunes architectures for months with little gain → the system fails in production on the ambiguous cases → the project is cancelled. Each stage hides the cause further, and nothing raises an error.
> The authors found data work undervalued: model work is visible (papers, leaderboards), data work (guidelines, label audits, schema changes) is not, though it has the most leverage. A guideline fixed before annotation costs an afternoon; after deployment it costs re-annotation and retraining. Hence quality checks at every stage.

**4.** A team needs 1,000 hours of labeled speech. Using the table, recommend a strategy, looking beyond cost and time.

> [!example]- Solution
> Purchasing is cheapest and fastest (\$10/h, 1 day), but other factors matter:
> - Distribution: purchased data was collected for another purpose (e.g. podcast audio for a call-centre product). The 100 owned hours are the only data known to match deployment; keep them as the test set.
> - Crowdsourced reading produces clear read speech, unlike noisy spontaneous speech, and the bias also sits in its validation split.
> - Paid labels cost 6× more per hour but give control over guidelines and edge cases; speech needs only reasonable annotators.
> - Speech is biometric data: without a documented consent trail, a dataset is a liability.
>
> Plan: buy data to start, evaluate on owned data, then spend paid labeling on the failure modes found by error analysis.

**5.** (Advanced) What do lineage and audit trails each capture, and what breaks without them?

> [!example]- Solution
> Lineage answers "where did this data come from?" (sources, transformations, code version); audit trails answer "who accessed it, and when?".
> Without lineage: precision drops 8% overnight and you can only guess. With lineage you trace model → dataset version → transformation code → raw source, and find that an upstream team changed a currency field three days ago. It is the data-side counterpart of model reproducibility (ch. 01).
> Without audit trails: a GDPR erasure request requires deleting a user's data from every derived dataset and model, which you can't even list; a breach notification requires stating what was accessed and by whom.
> You need both, captured as pipelines run. They can't be reconstructed after the job finishes.

## 📝 Summary

- Data and model pipelines run in parallel with feedback.
- Data-centric AI improves the data with the model held fixed; in production this usually pays more.
- Four pillars at every stage: quality, reliability, scalability, governance.
- Data cascades amplify early defects silently.
- Acquisition: scraping, crowdsourcing, synthetic data; weigh cost, time, quality, privacy.
- Batch is simple with high latency; stream is low-latency and must handle backpressure and freshness SLAs.
- Lineage tracks provenance, audit trails track access; both from the start.
- Scoping: problem vs solution, feasibility (HLP or predictive features), PoC → prototype → MVP → production.

## ⚠️ Important Notes

1. Most production failures are data problems.
2. Label inconsistency caps accuracy; measure annotator agreement before blaming the model.
3. Target leakage is invisible to train/test splits.
4. Predictive is not the same as permissible (ZIP code, browser type).
5. "Data is fixed" is an assumption.
6. Missing, stale or duplicated data degrades models without errors.
7. Purchased and crowdsourced data may not match deployment.
8. Keep a small in-distribution sample as a test set.
9. Distributing a job that fits on one machine can make it slower.
10. Lineage can't be added afterwards.
11. A PoC is about 20% of the work.
12. Capture consent at acquisition.

> [!warning] Gaps in the source slides
> - Slides 4, 7, 14, 22, 35, 41 have no text; slide 3 (two-pipeline diagram), 11 (data scientist time allocation), 12 (pillars diagram), 19 (label inconsistency figure), 33 (distributed processing), 36 and 38 (governance diagram, pipeline example) are images. Slide 16 ("Data Quality") has only a title.
> - Slide 13's pillars table is cut off in the Processing row.
> - Tables cut mid-cell on slides 6, 10, 32, 49, 51 were completed from context.
> - Assignment (slide 53): work through Géron's end-to-end project notebook (*Hands-On ML* 3rd ed., ch. 2), log the best model, load it to predict a house price, print its parameters.
> - References: Sambasivan et al., CHI 2021; Treveil et al., *Introducing MLOps*; Gift & Deza, *Practical MLOps*.

**Previous:** [[02 - Environment Setup]] · **Next:** [[04 - Model Development]]
