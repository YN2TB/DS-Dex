---
subject: MLOps
chapter: 03
tags: [ds, mlops, data-engineering, data-quality, governance, scoping]
source: "MLOPs_data.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Data Stage and Scoping

> [!note] Where this sits in the course
> The **second stage of the ML lifecycle** from [[01 - Introduction to MLOps]]. Where [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]] teaches the *techniques* of cleaning and transforming data, this chapter treats data as an **engineering and governance problem** — sourcing, ingestion at scale, lineage, and whether the project should exist at all.

## 📘 Main Knowledge

> Data quality serves as the **foundation that determines whether machine learning systems succeed or fail** in production environments.

### Two parallel pipelines

The full ML lifecycle runs as two pipelines with feedback between them:

- **Data pipeline** — collection → ingestion → analysis → labeling → validation → preparation → ML-ready datasets.
- **Model development pipeline** — training → evaluation → validation → deployment → production system.

> The curved feedback arrows show how **deployment insights trigger data refinements**, creating continuous improvement cycles that distinguish ML from traditional linear development.

### Model-centric vs data-centric AI

**Model-Centric AI** — focuses on choosing a suitable model type, architecture, and hyperparameters.
**Data-Centric AI** — emphasises the **systematic design and engineering of the data**.

| Aspect | Model-Centric | Data-Centric |
|---|---|---|
| **Focus** | Model architectures and algorithms | Data quality, consistency, coverage |
| **Approach** | Iterate on design, hyperparameters, training | Iterate on collection, labeling, cleaning, augmentation |
| **Assumption** | **Data is fixed**; gains come from better models | **Model is relatively fixed**; gains come from better data |
| **Techniques** | Deeper networks, ensembling, architecture search | Cleaning, re-labeling, balancing, augmentation |
| **Scalability** | Limited by model complexity and compute cost | Scales well without increasing model size |

The modern MLOps position — and Andrew Ng's argument — is that in most production settings the **data-centric** route yields more improvement per unit of effort.

### Data and data engineering

**Data** — raw observations, measurements, or records collected from the real world, storable, processable, and analysable.

- **Structured** — tables, databases
- **Semi-structured** — JSON, logs
- **Unstructured** — text, images, audio, video

May be **labeled** (input + target label) or unlabeled. Sourced from sensors, users, systems, or experiments.

> **Data Engineering** — the systematic discipline of designing and maintaining data infrastructure that transforms raw data into **reliable, accessible, and analysis-ready** datasets through principled acquisition, processing, storage, and governance.
>
> **No algorithm can overcome poor data, but excellent data engineering enables even simple models to achieve remarkable results.**

| Aspect | Software Engineering | Data Engineering |
|---|---|---|
| Focus | Building and maintaining applications | Designing and maintaining data pipelines and infrastructure |
| Objective | Reliable, scalable, maintainable software | Reliable, scalable, high-quality **data flow** |
| Artifacts | Source code, APIs, services | Data pipelines, warehouses, lakes, ETL/ELT workflows |
| Inputs | User requirements, business logic | Raw, semi-structured, structured data |
| Outputs | Software products and services | Cleaned, transformed, accessible data |
| Skills | Programming, architecture, testing, version control | Data modeling, ETL, … |

### The four pillars across pipeline stages

**Quality · Reliability · Scalability · Governance** — applied at every stage:

| Stage | Quality | Reliability | Scalability | Governance |
|---|---|---|---|---|
| **Acquisition** | Representative sampling, bias detection | Diverse sources, redundant collection | Web scraping, synthetic data | Consent, anonymization, ethical sourcing |
| **Ingestion** | Schema validation, data profiling | Dead letter queues, graceful degradation | Batch vs stream, autoscaling | Access controls, audit logs, lineage |
| **Processing** | Consistency validation, **training–serving parity** | Idempotent transformations, retries | Distributed frameworks, horizontal scaling | *(truncated in source)* |

Note **training–serving parity** under Processing — the feature store requirement from [[01 - Introduction to MLOps]]'s fraud case study.

### Data cascades

> **Data Cascades** — the phenomenon where poor data quality in early stages **amplifies throughout the entire pipeline**, causing downstream model failures, project termination, and potential user harm.

The term comes from Sambasivan et al. (2021), *"Everyone wants to do the model work, not the data work"*. Recognising cascades is what motivates **proactive** investment in data engineering rather than reactive debugging.

### Data reliability

> Reliable data produces **stable, accurate, and reproducible** model behaviour. Unreliable data leads to poor performance even from well-designed models, unexpected production behaviour, and loss of trust.
>
> **Good models cannot compensate for bad data.**

**Common issues:** missing data · incorrect data (sensor errors, wrong labels) · inconsistent data (schema or format changes) · duplicates · outdated data.
**Causes:** data integration issues · human errors · system and software limitations · poor data governance.

> These issues can **silently degrade** model performance.

**Label inconsistency** is called out separately (the deeplearning.ai example): different annotators labelling the same input differently. It puts a ceiling on achievable accuracy — a model cannot learn a rule that the labels themselves do not follow consistently.

### Data reliability vs model reliability

| | **Data Reliability** | **Model Reliability (Robustness)** |
|---|---|---|
| **What** | Consistency and stability of data across time and measurements | Consistent, trustworthy predictions on unseen data |
| **Focus** | Data pipelines, completeness, accuracy, freshness | Performance metrics, robustness to drift, validation |
| **Example** | Sales totals remain unchanged when no new sales occur | Fraud model performs reliably across users and days |

> **Data reliability concerns inputs; model reliability concerns outputs.** Unreliable data causes inconsistent results; weak models fail even with good data.

### Types of data problems

| | **Structured** | **Unstructured** |
|---|---|---|
| **Small Data** | Student grades prediction · Credit approval with 100 examples · Sales forecasting for a small shop | Medical image diagnosis · Small fruit-quality image set · Spam detection with 200 examples |
| **Big Data** | E-commerce sales forecasting · Airline demand forecasting · Stock price prediction | Image search over billions of photos · Speech recognition from audio streams · Social media text analysis |

> As data becomes **larger and less structured, both modeling and engineering complexity increase.**

- Creating accurate, well-curated datasets faces inherent **scaling limitations**.
- A cost-effective acquisition strategy at the **thousand**-example scale often becomes prohibitive at the **million**-example scale.
- Production systems often require **continuous** data collection to maintain relevance.

### Acquisition strategies

**Web scraping** — automatically crawl and extract data from websites at scale.
*Constraints:* legal and ethical (terms of service, copyright); technical (rate limiting slows collection, data is inconsistent).

**Crowdsourcing** — distribute microtasks to a large audience.
- **ImageNet** was built by distributing labeling tasks via Amazon Mechanical Turk.
- **Waze** crowdsources real-time traffic, routes, and incident reports from users.
- **Google's reCAPTCHA** verifies human users *while simultaneously labeling training data*.
*Flexibility:* tasks can be adjusted dynamically based on initial results.

**Synthetic data generation** — create unlimited examples algorithmically, removing human labor from acquisition. Modern systems produce data closely resembling real distributions. Particularly valuable where real data is impractical or costly to obtain — the automotive industry is the cited example (rare crash scenarios).

**Comparing strategies** — the speech recognition example:

| Source | Amount | Cost | Time |
|---|---|---|---|
| Owned | 100h | \$0 | 0 |
| Crowdsourced – Reading | 1000h | \$10,000 | 14 days |
| Pay for labels | 100h | \$6,000 | 7 days |
| Purchase data | 1000h | \$10,000 | 1 day |

*Other factors:* data quality, privacy, regulatory constraints.

**Who is qualified to label?** — (1) domain experts, (2) reasonable annotators, (3) almost no one. The answer differs by task: speech recognition, medical image diagnosis, recommendation systems, legal judgments.

### Ingestion: batch vs stream

**Batch ingestion** — collect data in groups over a period, then process. Suits cases where real-time processing is not critical and data can be processed on a schedule; **amortises startup costs across large volumes**.
*Example:* a retailer processes daily sales overnight, updating inventory prediction models each morning.

**Stream ingestion** — process data in real time as it arrives, where data loses value quickly and systems must respond to events immediately.
*Example:* a bank processes each transaction as it occurs to flag fraud immediately.
- Must handle **backpressure** when downstream systems cannot keep pace — a traffic spike producing data faster than processing capacity.
- **Data freshness SLAs** specify the maximum acceptable delay between generation and availability.

| Aspect | Batch | Stream |
|---|---|---|
| Basic idea | Processed in groups | Processed continuously as it arrives |
| Timing | Periodic (hourly, daily, weekly) | Real-time or near real-time |
| Data volume | Large chunks at once | Small events, one by one |
| **Latency** | High (minutes to hours) | **Low (ms to seconds)** |
| Use cases | Reports, analytics, model training | Fraud detection, monitoring, alerts |
| Complexity | Easier to build and maintain | More complex to design and operate |
| Tools | SQL, Hadoop, Spark | **Kafka**, Spark Streaming, Flink |
| Failure handling | Easy to retry whole batches | Requires careful handling of lost/delayed data |

### Distributed data processing

Split large datasets and computations across multiple nodes for speed, scalability, and fault tolerance — used when a single machine cannot handle the volume.

> Instead of one computer processing 1 TB in 10 hours, **10 computers process 100 GB each in about 1 hour.** A coordinator/master assigns tasks and collects results.

**Challenges:** partitioning introduces **coordination overhead**, and performance is limited by **network round-trip times** — local operations complete in *microseconds* while network coordination requires *milliseconds*, a thousand-fold difference.

**Technologies:** *Batch* — Hadoop, Spark. *Streaming* — Kafka, Spark Streaming, Flink. *Cloud* — AWS EMR, Google Dataflow, Azure Databricks.

### Data governance

**Principles:**
- Understand **what data flows** through the system, how it transforms, and **who accesses it**.
- Ensure systems operate within **ethical, legal, and business constraints**.
- Maintain **transparency and accountability**.
- Protect user **privacy and security** throughout the ML lifecycle.

> These are **foundational requirements that shape every technical decision from the outset, not afterthoughts to be applied later.**

**Data lineage** captures the complete **provenance** of every dataset:
- Which **raw sources** contributed data
- What **transformations** were applied, and when
- What **version of the processing code** executed

> Data lineage is essential for **debugging model behavior and ensuring reproducibility**.

**Audit trails** complement lineage by recording **who accessed data and when** — required for GDPR and CCPA compliance, and protecting reputation, avoiding legal consequences, and building stakeholder trust.

---

### Problem definition and scoping

**Problem vs solution** — a distinction that prevents building the wrong thing:

| Problem (What to achieve) | Solution (How to achieve) |
|---|---|
| Increase conversion | Search, recommendations |
| Reduce inventory | Demand prediction, marketing |
| Increase margin (profit per item) | Optimising what to sell (merchandising), recommend bundles |

**Feasibility** — *is this project technically possible?* Use **external benchmarks** (literature, competitors, other companies).

| | **Structured Data** | **Unstructured Data** |
|---|---|---|
| **New project** | Availability of predictive features | **HLP** |
| **Existing project** | New predictive features, history of project | HLP, history of project |

**HLP = Human-Level Performance** — for unstructured data (images, audio, text), humans set the benchmark, because a human can do the task and their accuracy is measurable. For structured data there is often no human baseline, so feasibility rests on whether **predictive features exist**.

**Do we have predictive features?**
- Given past purchases, predict future purchases ✓
- Given weather data, predict shopping mall foot traffic ✓
- Given DNA information, predict heart disease **?**
- Given social media chatter, predict demand for a clothing style **?**
- Given a stock's price history, predict its future price ✗

*Discussion points:* Do we have sufficient **signal** in the data? Is the problem **stable over time**? Are there **ethical or causal** limitations?

### Development stages

**PoC (Proof-of-Concept)** — early discovery, before significant investment.
*Goal:* validate whether the application is possible and worth building. *Focus:* technical feasibility, core mechanics, tech stack choice. *Output:* a simple, often non-visual demonstration; internal-facing.

> **PoC is only about 20% of the total journey. The real engineering effort begins thereafter.**

**Prototype** — refine design and test user interaction once feasibility is confirmed.
*Goal:* show how the final product will look, feel, and function. *Focus:* UI, user flow, design, early feedback.

| Feature | **PoC** | **Prototype** |
|---|---|---|
| Primary question | **Can it be built?** (Feasibility) | **How does it work/look?** (Usability) |
| Purpose | Verify technical viability | Visualize functionality, test UX, gather feedback |
| Audience | Internal team, technical stakeholders | Users, investors, broader stakeholders |
| Complexity | Low; core functionality | Medium; design and interaction flow |
| Stage | Early discovery (pre-prototype) | Early/seeding phase (post-PoC) |

**MVP (Minimum Viable Product)** — the simplest version with core features, to test assumptions and gather rapid feedback.
*Goal:* validate core hypotheses, assess market demand, learn from real users quickly. *Focus:* core features solving the primary problem — **maximum learning with minimum effort**.

**Production** — a complete, high-quality, scalable solution meeting broad market needs, with a full feature set, robust performance, security, and scalability.

| Feature | **MVP** | **Production System** |
|---|---|---|
| Purpose | Learn and validate assumptions | Deliver value and scale |
| Scope | Minimal core features | Full feature set |
| Target users | Early adopters and testers | Broad market |
| Quality | Functional, potentially basic | Polished, robust, reliable |
| Effort | Low initial investment | High development and maintenance cost |
| Risk | Low; testing hypotheses | Higher; market launch and scaling |

## ✏️ Exercises

**1.** *(Slide 21 quiz)* For each scenario, decide whether the problem is mainly **Data** or **Model**:
> (1) A face recognition model suddenly performs poorly after a camera upgrade. (2) A spam classifier predicts "not spam" for almost all emails. (3) A credit risk model trained last year underestimates default rates this year. (4) A model performs well on training data but poorly on test data. (5) An image classifier fails when images are rotated or poorly lit.

> [!example]- Solution
> | # | Scenario | Verdict |
> |---|---|---|
> | 1 | Camera upgrade | **Data** — data drift |
> | 2 | Predicts "not spam" for everything | **Data** — class imbalance |
> | 3 | Underestimates default rates a year later | **Data** — concept drift |
> | 4 | Good on train, poor on test | **Model** — overfitting |
> | 5 | Fails on rotated/dark images | **Data** — insufficient coverage |
>
> **(1) Data drift.** A new camera changes resolution, colour profile, and noise characteristics, so $P(X)$ shifts. Nothing is wrong with the model; it is receiving inputs unlike its training distribution. *Fix:* retrain or fine-tune on new-camera images.
>
> **(2) Class imbalance** — a data problem, though it *looks* like a model failure. If 98% of training emails are not spam, predicting the majority class achieves 98% accuracy. The same trap as the fraud example in [[01 - Introduction to MLOps]]. *Fix:* rebalance, use class weights, and change the metric to PR-AUC.
>
> **(3) Concept drift.** Features are unchanged in distribution, but the *relationship* $P(Y \mid X)$ shifted with the economy. The mapping the model learned no longer holds. *Fix:* retrain on recent data; establish a retraining cadence.
>
> **(4) Overfitting — the only genuine model problem here.** The model memorised training data rather than generalising. *Fix:* regularisation, simpler architecture, more data, cross-validation — see [[Data Preparation and Visualization/contents/09 - Building Pipelines|Building Pipelines]].
>
> **(5) Insufficient data coverage.** The training set lacked rotated and poorly lit examples, so the model never learned invariance. *Fix:* **data augmentation** — rotate, adjust brightness. This is a data-centric fix to what is often mistaken for a model weakness.
>
> **Four of five are data problems.** That ratio is the lecture's argument for data-centric AI: most production failures trace to data, yet most effort goes to models — precisely the finding of the *Data Cascades* paper.

**2.** *(Slides 45–46 quiz)* Classify each feature as **Highly Predictive**, **Weakly Predictive**, or **Not Predictive / Leaky**, and identify data leakage.
> *House prices:* house size (m²) · wall color · ZIP code
> *Student exam performance:* hours studied · student ID number · attendance rate
> *Credit default:* past repayment history · browser type · credit utilization rate
> *Fraudulent transactions:* transaction amount · time of day · label added after investigation

> [!example]- Solution
> | Feature | Verdict |
> |---|---|
> | **House size (m²)** | Highly predictive — the single strongest price driver |
> | **Wall color** | Not predictive — cosmetic and cheaply changed |
> | **ZIP code** | Highly predictive — proxies location, schools, amenities ⚠️ |
> | **Hours studied** | Highly predictive |
> | **Student ID number** | Not predictive — a nominal identifier ([[Mathematical Statistics/contents/01 - Introduction to Statistics|Introduction to Statistics]]) |
> | **Attendance rate** | Highly predictive |
> | **Past repayment history** | Highly predictive — the strongest credit signal |
> | **Browser type** | Weakly predictive at best — may proxy device cost, i.e. income |
> | **Credit utilization rate** | Highly predictive |
> | **Transaction amount** | Weakly to moderately predictive |
> | **Time of day** | Weakly predictive |
> | **Label added after investigation** | **🚩 LEAKY** |
>
> **The leakage is the last one.** *"Label added after investigation"* is information that **only exists after the outcome is known**. A transaction is investigated *because* it was flagged as suspicious, so this feature encodes the answer. The model will score near-perfectly in testing and be **useless in production**, where no investigation has yet occurred.
>
> The slide's definition covers two senses: unintentional exposure of sensitive information, **or** including future/target information in training data, "causing it to perform well in testing but poorly in reality."
>
> **The diagnostic question: would I actually have this value at the moment I need to predict?** Compare the leakage discussion in [[Data Preparation and Visualization/contents/04 - Foundations of Data Preparation for ML|Foundations of Data Preparation]] — that chapter's leakage is procedural (fit before split); this is **target leakage**, baked into the feature itself, and no split discipline detects it.
>
> **Two subtler cases worth flagging.** **ZIP code** is highly predictive but a **proxy for race and income** in many countries — a fairness and legal problem, not a statistical one. **Browser type** is the classic "weakly predictive but ethically fraught" feature: it may correlate with default through device cost, meaning the model penalises poorer applicants for owning cheaper hardware. Both belong to the governance question of whether a feature *should* be used, not merely whether it works.

**3.** Explain data cascades and why the paper is titled *"Everyone wants to do the model work, not the data work"*.

> [!example]- Solution
> **A data cascade** is poor data quality in an early stage **amplifying** through the pipeline into downstream failure.
>
> **A concrete cascade:** an annotation guideline is ambiguous about whether a partially visible object counts → annotators split roughly 50/50 → the model learns an incoherent boundary and plateaus at 82% → the team assumes a model problem and spends three months on architecture search, gaining 0.5% → the system ships and fails in production on exactly those ambiguous cases → users lose trust and the project is cancelled.
>
> **The amplification is what makes it a cascade.** The root cause was one under-specified sentence in a labeling guideline. Every stage after it inherited the defect, and each stage made the cause **harder to see** — by the time it manifests as production failure, it is three steps and several months removed from its origin. The slides call this *silent degradation*: nothing errors, no test fails.
>
> **Why the title.** Sambasivan et al. found practitioners systematically **undervalue data work**. Model work is visible and prestigious — a new architecture is a publication, a leaderboard score, a demo. Data work is invisible and low-status: writing annotation guidelines, auditing label consistency, chasing schema changes. It has no leaderboard.
>
> The perverse consequence is that the highest-leverage work is the least rewarded. The lecture's own claim — *"no algorithm can overcome poor data, but excellent data engineering enables even simple models to achieve remarkable results"* — inverts the incentive.
>
> **Why cascades justify proactive investment.** Fixing a labeling guideline before annotation costs an afternoon. Discovering it after deployment costs the retraining, the re-annotation of the whole dataset, and the institutional trust. Cost grows by orders of magnitude with each stage — the same economics as bug-fixing in software engineering, but worse, because ML failures are silent rather than loud.
>
> The chapter's structural answer is the four pillars applied **at every stage** — quality checks at acquisition, schema validation at ingestion, parity checks at processing — so defects are caught where they arise rather than where they surface.

**4.** A team must acquire 1,000 hours of labeled speech data. Using the sourcing table, recommend a strategy and justify it beyond cost and time.

> [!example]- Solution
> | Source | Amount | Cost | Time | \$/hour |
> |---|---|---|---|---|
> | Owned | 100h | \$0 | 0 | \$0 |
> | Crowdsourced – Reading | 1000h | \$10,000 | 14 days | \$10 |
> | Pay for labels | 100h | \$6,000 | 7 days | **\$60** |
> | Purchase data | 1000h | \$10,000 | 1 day | \$10 |
>
> **Recommendation: start with the 100h owned, purchase 1000h to move immediately, and reserve budget for targeted paid labeling of hard cases.**
>
> **Why not simply the cheapest-and-fastest (purchase)?** The lecture's "other factors" — data quality, privacy, regulatory constraints — decide this, and they cut differently:
>
> **Distribution match matters more than volume.** Purchased data was collected for someone else's purpose. If your product serves Vietnamese call-centre audio and the vendor supplies American podcast audio, 1000 hours of it may help less than 100 hours of your own. **The owned data is the only sample guaranteed to match your deployment distribution**, which makes it invaluable as a *test set* even though it is too small to train on. Never spend it on training.
>
> **Crowdsourced reading has a systematic bias.** Volunteers reading prompts produce *read* speech — clearly enunciated, low background noise, no interruptions. Deployment is *spontaneous* speech with disfluencies, overlap, and noise. This is a built-in train/serve mismatch, and it is invisible in validation because the validation set shares the bias.
>
> **Paid labeling is 6× the unit cost but buys control** — your annotation guidelines, your quality bar, your edge cases. Per slide 29's question, speech transcription needs *reasonable annotators* rather than domain experts, which keeps this viable; medical imaging would not have that luxury.
>
> **Privacy and regulation may eliminate options outright.** Speech is biometric data. Under GDPR, purchased recordings need documented consent for *your* use, and crowdsourced data needs consent capture in the collection flow. A cheap dataset without a consent trail is a liability, not an asset — which is why the pillars table lists *"Consent, anonymization, ethical sourcing"* under Acquisition.
>
> **The sequencing logic:** purchase to unblock development on day one, hold owned data as the trustworthy evaluation set, then use error analysis to direct paid labeling at the specific failure modes. That is the data-centric loop — spend the expensive budget where the model is actually failing, rather than uniformly.

**5.** (Advanced) Explain data lineage and audit trails: what each captures, why both are needed, and what breaks without them.

> [!example]- Solution
> **Lineage answers "where did this data come from?"; audit trails answer "who touched it?"** Different questions, different failure modes.
>
> **Data lineage** captures provenance: which **raw sources** contributed, what **transformations** were applied and when, and what **version of the processing code** executed.
>
> **Audit trails** record **who accessed data and when**.
>
> **What breaks without lineage — a debugging story.** A fraud model's precision drops 8% overnight. Without lineage you can only guess: new code? new data? a drifted distribution? With lineage you query the model version, see which dataset version trained it, see which transformation code produced that dataset, and see which raw sources fed it — and discover that an upstream team changed a currency field from USD to local currency three days ago. **Without lineage this is days of archaeology; with it, minutes.**
>
> That is why the slides tie lineage to **reproducibility**: reproducing a result means reconstructing an exact combination of raw data, transformation code, and parameters. The MLflow reproducibility problem in [[01 - Introduction to MLOps]] is the same requirement viewed from the model side; lineage is its data-side counterpart. Slide 38's point is that lineage is *"essential when upstream data must be changed"* — it lets you answer **"what breaks if I change this?"** *before* changing it.
>
> **What breaks without audit trails — a compliance story.** Under **GDPR** a user exercises the right to erasure. You must delete their data everywhere — including every derived dataset and every model trained on it. Without an access and lineage record you cannot even enumerate where it went. Under a breach-notification obligation you must state what was accessed and by whom; "we don't know" is itself a violation.
>
> The slides list the stakes plainly: compliance with GDPR and CCPA, protecting reputation, avoiding financial and legal consequences, increasing stakeholder trust.
>
> **Why both, and why from the start.** Lineage without audit means you can reproduce a result but cannot prove who saw the underlying personal data. Audit without lineage means you know who ran a query but not what the data became downstream. Together they answer *what happened* and *who did it* — the two halves of accountability.
>
> Retrofitting is close to impossible: lineage must be **captured as the pipeline runs**, since the information — which code version, which source file, which timestamp — is gone once the job finishes. Hence the slides' framing: governance requirements are *"foundational requirements that shape every technical decision from the outset, not afterthoughts to be applied later."*

## 📝 Summary

- **The data stage is two pipelines with feedback** — data (collect → ingest → analyse → label → validate → prepare) and model development (train → evaluate → validate → deploy).
- **Model-centric assumes data is fixed; data-centric assumes the model is.** In production, data-centric usually yields more per unit of effort.
- **Data engineering** turns raw data into reliable, accessible, analysis-ready datasets. *No algorithm overcomes poor data.*
- **Four pillars at every stage:** Quality, Reliability, Scalability, Governance.
- **Data cascades** amplify early defects into downstream failure — and do so silently.
- **Data reliability concerns inputs; model reliability concerns outputs.**
- **Complexity grows with size and lack of structure**; strategies that work at thousands of examples fail at millions.
- **Acquisition:** web scraping (legal/technical limits), crowdsourcing (ImageNet, Waze, reCAPTCHA), synthetic generation (where real data is impractical).
- **Batch vs stream:** batch is simpler with high latency; stream is low-latency, complex, and must handle **backpressure** and **freshness SLAs**.
- **Distributed processing** trades coordination overhead and network latency (ms vs µs) for parallelism.
- **Lineage tracks provenance; audit trails track access.** Both are foundational, not retrofittable.
- **Scoping:** separate problem from solution, assess feasibility (HLP for unstructured, predictive features for structured), and progress **PoC → Prototype → MVP → Production**.

## ⚠️ Important Notes

**Most production ML failures are data problems, not model problems** — four of the five quiz scenarios. Yet effort skews toward models, which is the *Data Cascades* finding.

**Label inconsistency caps achievable accuracy.** If annotators disagree, no model can learn the rule, and architecture work cannot recover it. Measure inter-annotator agreement before blaming the model.

**Target leakage is invisible to train/test splits.** A feature computed *after* the outcome (an investigation label, a cancellation date) makes test performance excellent and production performance worthless. Ask: *would I have this at prediction time?*

**Highly predictive is not the same as permissible.** ZIP code predicts house prices well and proxies protected attributes; browser type may proxy income. Governance decides whether a feature should be used, not just whether it works.

**"Data is fixed" is an assumption, not a fact.** Treating the dataset as immutable and iterating only on models forecloses the cheaper improvement path.

**Silent degradation is the defining hazard.** Missing, duplicated, stale, and inconsistent data produce no errors — only quietly worse predictions. Only explicit validation catches them.

**Purchased and crowdsourced data carry distribution bias.** Read speech ≠ spontaneous speech; someone else's dataset was collected for someone else's problem. Volume does not compensate for mismatch.

**Guard your in-distribution data as a test set.** A small sample that genuinely matches deployment is more valuable for *evaluation* than for training.

**Stream ingestion must handle backpressure.** A traffic spike that outpaces processing capacity silently drops or delays events, and delayed data corrupts time-sensitive features.

**Network latency dominates distributed processing.** Local operations take microseconds, coordination milliseconds — a 1000× gap. Distributing a job that fits on one machine makes it *slower*.

**Lineage cannot be added retrospectively.** It must be captured as pipelines run; afterwards, the information is gone.

**A PoC is ~20% of the journey.** A working demo is not evidence that a production system is close — most of the engineering follows.

**Consent must be captured at acquisition.** A dataset without a documented consent trail is a legal liability regardless of how cheaply it was obtained.

> [!warning] Gaps in the source slides
> LaTeX Beamer, mostly clean extraction. Missing:
> - **Slides 4, 7, 14, 22, 35, 41** produced no text — section dividers or full-page figures.
> - **Slide 3** — the two-pipeline lifecycle diagram is a figure; only the caption survived.
> - **Slide 11 — "Data scientist time allocation"** is entirely an image. (The commonly cited figure is ~80% of time on data preparation.)
> - **Slide 12** — the pillars diagram is an image; slide 13's table is the recoverable version, and it is **truncated mid-row** at Processing/Governance.
> - **Slide 16 — "Data Quality"** has a title only, no content.
> - **Slide 19** — the label-inconsistency figure (deeplearning.ai) is an image.
> - **Slide 33** — the distributed processing diagram is a figure.
> - **Slides 36, 38** — the data governance diagram (blue/green layers) and the data pipeline example are images; only the legends extracted.
> - **Several tables truncate mid-cell** where the PDF layout cut them: slide 6 (Robustness row), slide 10 (Skills row), slide 32 (Cost row), slide 49 (Prototype output), slide 51 (Production focus). Completed from context above.
>
> **Assignment (slide 53):** work through [Géron's end-to-end ML project notebook](https://github.com/ageron/handson-ml3/blob/main/02_end_to_end_machine_learning_project.ipynb) (Ch. 2 of *Hands-On Machine Learning*, 3rd ed.). Log the best model, load it to predict a house price, and print the model's parameters.
>
> **References:** Sambasivan et al. (2021), *"Everyone wants to do the model work, not the data work": Data Cascades in High-Stakes AI*, CHI 2021 · Treveil et al., *Introducing MLOps* · Gift & Deza, *Practical MLOps*.

---
**Previous:** [[02 - Environment Setup]] · **Next:** [[04 - Model Development]]
