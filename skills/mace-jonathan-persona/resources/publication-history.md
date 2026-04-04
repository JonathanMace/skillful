# Jonathan Mace — Publication History

## Persona Findings

Jonathan Mace is a systems researcher whose career traces a single coherent arc: **making large-scale distributed systems observable, controllable, and self-managing**. From his earliest MSc project on trace comparison (2013) through to his current work on agentic AI for cloud operations (2025), every major contribution either directly advances distributed observability or applies the same cross-cutting, end-to-end systems thinking to adjacent problems.

Key evidence-backed claims:

- **Distributed tracing is the gravitational center.** At least 15 of ~35 research publications directly address tracing, monitoring, or context propagation. His PhD thesis, O'Reilly book, most-cited conference papers, and signature awards all involve tracing. Even when branching into ML systems (Clockwork) or FaaS (Groundhog), the work shares an architectural philosophy of end-to-end visibility and control.
- **He builds frameworks, not point solutions.** Pivot Tracing, Universal Context Propagation, Blueprint, and AIOpsLab are all *architectures* or *toolchains* — general-purpose infrastructure designed to be extensible. This distinguishes him from researchers who optimize a single metric.
- **His career shows deliberate phase transitions.** PhD work focused on the theory and architecture of cross-cutting instrumentation. MPI-SWS broadened into systems building (Clockwork, Groundhog) and mentoring a research group. MSR shifted the focus to cloud reliability at scale, with an increasing emphasis on AI/LLM-driven operations.
- **He writes for practitioners, not just academics.** The O'Reilly book (2020), CACM research highlights, and open-source artifacts signal a commitment to real-world impact. Canopy was deployed at Facebook scale; Hindsight was designed for production edge-case tracing.
- **He gravitates to top systems venues.** SOSP (5 papers + General Chair), NSDI (2), OSDI (1), EuroSys (2), SIGCOMM (1), SoCC (5). This is overwhelmingly a systems-conference researcher, not a PL/SE/ML researcher who dabbles in systems.
- **Long-running collaborations define his network.** Rodrigo Fonseca (PhD advisor) appears as coauthor across a 12+ year span. Vaastav Anand (MPI-SWS student) coauthors at least 10 papers spanning 2019–2025. Madan Musuvathi appears in both PhD-era and MSR-era work.

## Career Timeline

| Period | Affiliation | Role | Key Topics | Key Venues | Notable Papers / Awards |
|--------|------------|------|------------|------------|------------------------|
| 2009–2011 | IBM UK (Hursley) | Software Engineer | UI/web systems, NLP | — | ~8 US patents on UI/web technologies; Extreme Blue internship |
| 2011–2014 | Brown University | PhD student (early) | Trace comparison, resource mgmt | HotDep | Revisiting End-to-End Trace Comparison (2013); Towards General-Purpose Resource Management (HotDep 2014) |
| 2014–2016 | Brown University | PhD student (mid) | Distributed tracing, resource mgmt, fair queuing | SOSP, NSDI, SIGCOMM, SoCC | **Pivot Tracing** (SOSP 2015, ⭐ Best Paper); Retro (NSDI 2015); 2DFQ (SIGCOMM 2016); Facebook PhD Fellowship (2016) |
| 2016–2018 | Brown University + Facebook | PhD student (late) + intern | End-to-end tracing at scale, context propagation | SOSP, EuroSys | Canopy (SOSP 2017, Facebook deployment); Universal Context Propagation (EuroSys 2018); PhD Thesis (2018); **Dennis M. Ritchie Dissertation Award, Honorable Mention** |
| 2018–2022 | MPI-SWS / Saarland Univ. | Tenure-track Faculty | ML systems, tracing sampling, FaaS, visualization, sustainability | OSDI, SoCC, EuroSys, HotCarbon | **Clockwork** (OSDI 2020, Distinguished Artifact); Sifter (SoCC 2019); O'Reilly Book (2020); Groundhog (EuroSys 2023); SOSP 2023 General Co-Chair |
| 2023–present | Microsoft Research | Senior Researcher | AIOps, autonomous clouds, LLM-based diagnostics, microservice benchmarking, incident management | SOSP, NSDI, SoCC, MLSys, ESEC/FSE | Blueprint (SOSP 2023); Hindsight (NSDI 2023); Building AI Agents for Autonomous Clouds (SoCC 2024); AIOpsLab (MLSys 2025); Retry Bugs (SOSP 2024) |

## Full Publication List

### 2025
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 1 | AIOpsLab: A Holistic Framework for Evaluating AI Agents for Enabling Autonomous Cloud | Y. Chen, M. Shetty, G. Somashekar, M. Ma, Y. Simmhan, **J. Mace**, C. Bansal, R. Wang, S. Rajmohan | MLSys 2025 | ~38 |
| 2 | Fair, Practical, and Efficient Carbon Accounting for LLM Serving | Y. L. Li, L. Han, G. E. Suh, C. Delimitrou, F. Kazhamiaka, E. Choukse, R. Fonseca, L. Yu, **J. Mace**, U. Gupta | SIGMETRICS 2025 | ~1 |
| 3 | Generating Representative Macrobenchmark Microservice Systems from Distributed Traces with Palette | V. Anand, M. Stolet, **J. Mace**, A. Kaufmann | APSys 2025 | new |
| 4 | Intent-based System Design and Operation | V. Anand, Y. Li, A. G. Kumbhare, C. Irvene, C. Bansal, G. Somashekar, **J. Mace**, P. Las-Casas, R. Bianchini, R. Fonseca | PACMI 2025 | ~2 |
| 5 | Automated Service Design with Cerulean | V. Anand, A. Kumbhare, C. Irvene, C. Bansal, G. Somashekar, **J. Mace**, P. Las-Casas, R. Fonseca | AIOps 2025 | new |
| 6 | Argos: Agentic Time-Series Anomaly Detection with Autonomous Rule Generation via LLMs | Y. Gu, Y. Xiong, **J. Mace**, Y. Jiang, Y. Hu, B. Kasikci, P. Cheng | arXiv 2025 | ~15 |

### 2024
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 7 | Building AI Agents for Autonomous Clouds: Challenges and Design Principles | M. Shetty, Y. Chen, G. Somashekar, M. Ma, Y. Simmhan, X. Zhang, **J. Mace**, P. Las-Casas, S. G. Nath, C. Bansal, S. Rajmohan | SoCC 2024 | ~50 |
| 8 | If At First You Don't Succeed, Try, Try, Again...? Detecting Retry Bugs in Software Systems | B. Stoica, U. Sethi, Y. Su, C. Zhou, S. Lu, **J. Mace**, M. Musuvathi, S. Nath | SOSP 2024 | ~14 |
| 9 | Cloud Atlas: Efficient Fault Localization for Cloud Systems using Language Models and Causal Insight | Z. Xie, Y. Zheng, L. Ottens, K. Zhang, C. Kozyrakis, **J. Mace** | arXiv 2024 | ~17 |

### 2023
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 10 | Blueprint: A Toolchain for Highly-Reconfigurable Microservice Applications | V. Anand, D. Garg, A. Kaufmann, **J. Mace** | SOSP 2023 | ~17 |
| 11 | Antipode: Enforcing Cross-Service Causal Consistency in Distributed Applications | J. Loff, D. Porto, J. Garcia, **J. Mace**, R. Rodrigues | SOSP 2023 | ~18 |
| 12 | Detection Is Better Than Cure: A Cloud Incidents Perspective | V. Ganatra, A. Parayil, S. Ghosh, Y. Kang, M. Ma, C. Bansal, S. Nath, **J. Mace** | ESEC/FSE 2023 | ~28 |
| 13 | The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems | L. Zhang, Z. Xie, V. Anand, Y. Vigfusson, **J. Mace** | NSDI 2023 | ~50 |
| 14 | Groundhog: Reconciling Efficiency and Request Isolation in FaaS | M. Alzayat, **J. Mace**, P. Druschel, D. Garg | EuroSys 2023 | ~31 |
| 15 | A Qualitative Interview Study of Distributed Tracing Visualisation | T. Davidson, E. Wall, **J. Mace** | IEEE TVCG 2023 | ~18 |
| 16 | The Odd One Out: Energy is Not Like Other Metrics | V. Anand, Z. Xie, M. Stolet, R. De Viti, T. Davidson, R. Karimipour, S. Alzayat, **J. Mace** | ACM SIGENERGY 2023 | ~19 |

### 2022
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 17 | See it to Believe it? The Role of Visualisation in Systems Research | T. Davidson, **J. Mace** | SoCC 2022 | ~3 |
| 18 | The Odd One Out: Energy is not like Other Metrics | V. Anand et al. | HotCarbon 2022 | (→ expanded in SIGENERGY 2023) |
| 19 | ACT now: Aggregate Comparison of Traces for Incident Localization | K. Ramasubramanian, A. Raina, **J. Mace**, P. Alvaro | arXiv 2022 | — |

### 2021
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 20 | Systems trivia night | V. Anand, R. De Viti, **J. Mace** | HotOS 2021 | — |

### 2020
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 21 | **Serving DNNs like Clockwork: Performance Predictability from the Bottom Up** | A. Gujarati, R. Karimi, S. Alzayat, W. Hao, A. Kaufmann, Y. Vigfusson, **J. Mace** | OSDI 2020 ⭐ Distinguished Artifact | **~468** |
| 22 | Distributed Tracing in Practice | A. Parker, D. Spoonhower, **J. Mace**, B. Sigelman, R. Isaacs | O'Reilly Book 2020 | ~99 |
| 23 | Pivot Tracing (Research Highlight) | **J. Mace**, R. Roelke, R. Fonseca | CACM 2020 | ~8 |
| 24 | Aggregate-driven trace visualizations for performance debugging | V. Anand, M. Stolet, T. Davidson, I. Beschastnikh, T. Munzner, **J. Mace** | arXiv 2020 | ~16 |

### 2019
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 25 | Sifter: Scalable Sampling for Distributed Traces, without Feature Engineering | P. Las-Casas, G. Papakerashvili, V. Anand, **J. Mace** | SoCC 2019 | ~70 |
| 26 | No DNN Left Behind: Improving Inference in the Cloud with Multi-Tenancy | A. Samanta, S. Shrinivasan, A. Kaufmann, **J. Mace** | arXiv 2019 | ~11 |

### 2018
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 27 | **Universal Context Propagation for Distributed System Instrumentation** | **J. Mace**, R. Fonseca | EuroSys 2018 | ~79 |
| 28 | A Universal Architecture for Cross-Cutting Tools in Distributed Systems | **J. Mace** | PhD Thesis, Brown University | — |
| 29 | Weighted Sampling of Execution Traces: Capturing More Needles and Less Hay | P. Las-Casas, **J. Mace**, D. Guedes, R. Fonseca | SoCC 2018 | ~48 |

### 2017
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 30 | **Canopy: An End-to-End Performance Tracing And Analysis System** | J. Kaldor, **J. Mace**, M. Bejda, E. Gao, W. Kuropatwa, J. O'Neill, K. W. Ong, B. Schaller, P. Shan, B. Viscomi, V. Venkataraman, K. Veeraraghavan, Y. J. Song | SOSP 2017 | **~256** |
| 31 | End-to-End Tracing: Adoption and Use Cases | **J. Mace** | Brown University Survey, 2017 | ~31 |

### 2016
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 32 | Principled Workflow-Centric Tracing of Distributed Systems | R. R. Sambasivan, I. Shafer, **J. Mace**, B. H. Sigelman, R. Fonseca, G. R. Ganger | SoCC 2016 | ~94 |
| 33 | **2DFQ: Two-Dimensional Fair Queuing for Multi-Tenant Cloud Services** | **J. Mace**, P. Bodik, M. Musuvathi, R. Fonseca, K. Varadarajan | SIGCOMM 2016 | ~45 |

### 2015
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 34 | **Pivot Tracing: Dynamic Causal Monitoring for Distributed Systems** | **J. Mace**, R. Roelke, R. Fonseca | SOSP 2015 ⭐ Best Paper | **~403** |
| 35 | We are Losing Track: a Case for Causal Metadata in Distributed Systems | R. Fonseca, **J. Mace** | HPTS 2015 | — |
| 36 | **Retro: Targeted Resource Management in Multi-Tenant Distributed Systems** | **J. Mace**, P. Bodik, R. Fonseca, M. Musuvathi | NSDI 2015 | **~154** |

### 2014
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 37 | Towards General-Purpose Resource Management in Shared Cloud Services | **J. Mace**, P. Bodik, R. Fonseca, M. Musuvathi | HotDep 2014 | ~5 |

### 2013
| # | Title | Authors | Venue | Citations |
|---|-------|---------|-------|-----------|
| 38 | Revisiting End-to-End Trace Comparison with Graph Kernels | **J. Mace**, R. Fonseca | MSc Project, Brown University 2014 | — |

### US Patents (from IBM, 2014–2019)
| Title | Co-inventors | Patent # |
|-------|-------------|----------|
| Multi-modal journey planner | A. Bridgen, A. Flatt, R. W. Pilot | US 9,594,772 |
| Presenting a custom view in an IDE based on a variable selection | A. Armstrong, R. Pilot | US 8,959,479 |
| Representing a graphical user interface using a topic tree structure | S. J. Horsman, M. J. Kockott, A. Moger | US 9,110,554 / US 9,046,982 |
| Dynamic file retrieving for web page loading | A. Bridgen, A. Flatt, R. W. Pilot | US 9,881,101 |
| Dynamic setting of increments on an amplitude scale | A. A. Armstrong, R. W. Pilot | US 9,037,276 |
| Flattening a subset of configuration UI panels | A. Bridgen, A. Flatt, R. Pilot | US 8,898,589 |
| Method for modifying a user interface | A. A. Armstrong, R. W. Pilot | US 8,751,871 |
| Translating user interface sounds into 3D audio space | A. A. Armstrong, M. D. Whitbourne | US 10,368,180 |

## Topic Clusters

### Cluster 1: Distributed Tracing & Observability (2013–present) — The Core
The defining thread of Mace's career. This cluster encompasses the foundational theory, architecture, and practical deployment of distributed tracing systems.

**Papers:** Revisiting End-to-End Trace Comparison (2013), Pivot Tracing (SOSP 2015), We are Losing Track (HPTS 2015), Principled Workflow-Centric Tracing (SoCC 2016), Canopy (SOSP 2017), End-to-End Tracing Survey (2017), Universal Context Propagation (EuroSys 2018), PhD Thesis (2018), Weighted Sampling (SoCC 2018), Sifter (SoCC 2019), Distributed Tracing in Practice (O'Reilly 2020), Pivot Tracing CACM Highlight (2020), ACT now (2022), Hindsight (NSDI 2023), Qualitative Interview Study of DT Visualisation (IEEE TVCG 2023)

**Key contributions:**
- **Cross-component causal monitoring** (Pivot Tracing) — dynamic instrumentation + happened-before joins across distributed boundaries
- **Universal context propagation** (Baggage) — a general-purpose metadata propagation layer for any cross-cutting tool
- **Scalable sampling** — Weighted Sampling, Sifter, and Hindsight tackle the fundamental tension between trace fidelity and overhead
- **Production-scale deployment** — Canopy ran at Facebook scale (1B+ traces/day)
- **Retroactive edge-case tracing** — Hindsight captures rare events without upfront sampling decisions

**Arc:** Early work (2013–2015) established *foundational theory* (causal metadata, dynamic monitoring). Mid-career (2016–2018) focused on *generalization and architecture* (universal context propagation, workflow-centric tracing). Recent work (2019–2023) addresses *scalability and production challenges* (sampling, edge-case capture, visualization).

### Cluster 2: Resource Management & Fair Scheduling (2014–2016)
A concentrated PhD-era thread on multi-tenant resource management in cloud services.

**Papers:** Towards General-Purpose Resource Management (HotDep 2014), Retro (NSDI 2015), 2DFQ (SIGCOMM 2016)

**Key contributions:**
- **Retro** uses end-to-end tracing to attribute resource consumption to individual tenants, enabling targeted throttling
- **2DFQ** introduces two-dimensional fair queuing that accounts for both request rate and per-request cost
- These papers share the tracing-as-infrastructure philosophy: resource management is treated as a *cross-cutting concern* enabled by end-to-end visibility

**Arc:** This thread emerged from the same architectural ideas as Pivot Tracing (cross-component visibility enables cross-component control) and was largely completed by 2016. The ideas were synthesized into the PhD thesis.

### Cluster 3: ML Systems & DNN Serving (2019–2022)
An MPI-SWS era branch into machine learning systems, particularly inference serving.

**Papers:** No DNN Left Behind (2019), Clockwork (OSDI 2020)

**Key contributions:**
- **Clockwork** eliminates performance unpredictability in DNN serving by centralizing scheduling, achieving extremely tight tail latency. Most-cited paper overall (468 citations).
- Shares a systems philosophy with the tracing work: understand end-to-end behavior, then control it centrally.

**Arc:** This cluster represents a deliberate broadening during the MPI-SWS years, applying systems thinking to ML infrastructure. It did not become a long-term thread — Mace returned to observability and AIOps by 2023.

### Cluster 4: Microservice Infrastructure & Benchmarking (2023–2025)
Tools and frameworks for building, configuring, and evaluating microservice systems.

**Papers:** Blueprint (SOSP 2023), Palette (APSys 2025), Cerulean (AIOps 2025), Intent-based System Design (PACMI 2025)

**Key contributions:**
- **Blueprint** is a compiler and benchmark suite that separates microservice application logic from infrastructure decisions, enabling rapid reconfiguration
- **Palette** generates representative benchmark microservice systems from production traces
- This cluster directly supports the tracing research by providing configurable testbeds

### Cluster 5: Cloud Reliability & AIOps (2023–present) — The Current Frontier
The newest and fastest-growing cluster, combining observability expertise with AI/LLM capabilities.

**Papers:** Detection Is Better Than Cure (ESEC/FSE 2023), Building AI Agents for Autonomous Clouds (SoCC 2024), Retry Bugs (SOSP 2024), Cloud Atlas (2024), AIOpsLab (MLSys 2025), Argos (2025), Intent-based System Design (2025), Cerulean (2025)

**Key contributions:**
- **AIOpsLab** provides a holistic evaluation framework for AI agents managing cloud systems
- **Cloud Atlas** uses LLMs + causal reasoning for fault localization
- **Retry Bugs** applies LLM-informed tooling to detect a specific class of reliability bugs
- This cluster represents Mace's current synthesis: the observability infrastructure he's spent a career building is now the foundation for AI-driven autonomous operations

### Cluster 6: Systems Visualization & Human Factors (2020–2023)
An MPI-SWS era thread exploring how humans interact with systems data.

**Papers:** Aggregate-driven trace visualizations (2020), Systems trivia night (HotOS 2021), See it to Believe it? (SoCC 2022), Qualitative Interview Study of DT Visualisation (IEEE TVCG 2023), I Don't Know What You Did Last Summer (workshop)

**Key contributions:**
- Studies the *human* side of observability: how engineers actually use trace visualizations, what information they need, and where current tools fall short
- Driven by student Thomas Davidson's thesis work

### Cluster 7: Systems Infrastructure & Isolation (2023)
**Papers:** Groundhog (EuroSys 2023), Antipode (SOSP 2023)

**Key contributions:**
- **Groundhog** reconciles efficiency and isolation in FaaS via lightweight process-level isolation
- **Antipode** enforces cross-service causal consistency — directly adjacent to the context propagation thread

### Cluster 8: Sustainability & Energy (2022–2025)
An emerging thread on energy measurement and carbon accounting for computing.

**Papers:** The Odd One Out (HotCarbon 2022 / SIGENERGY 2023), Fair Carbon Accounting for LLM Serving (SIGMETRICS 2025)

## Venue Patterns

| Venue | Count | Years | Signal |
|-------|-------|-------|--------|
| **SOSP** | 5 papers + General Co-Chair 2023 | 2015, 2017, 2023×2, 2024 | Primary home venue; measures highest-impact systems work |
| **SoCC** | 5 papers | 2016, 2018, 2019, 2022, 2024 | Consistent cloud-systems outlet; used for tracing and sampling work |
| **NSDI** | 2 papers | 2015, 2023 | Networked systems; used for infrastructure-heavy work (Retro, Hindsight) |
| **EuroSys** | 2 papers | 2018, 2023 | European systems venue; natural fit during MPI-SWS years |
| **OSDI** | 1 paper | 2020 | Clockwork; OSDI Distinguished Artifact Award |
| **SIGCOMM** | 1 paper | 2016 | 2DFQ; networking venue for the fair-queuing work |
| **MLSys** | 1 paper | 2025 | AIOpsLab; ML systems venue for AI agents work |
| **ESEC/FSE** | 1 paper | 2023 | Software engineering venue; incident management work |
| **IEEE TVCG** | 1 paper | 2023 | Visualization journal; tracing visualization study |
| **CACM** | 1 paper | 2020 | Research Highlight (Pivot Tracing); high-visibility invited piece |

**What this signals:**
- Mace is firmly a **top-tier systems researcher** — SOSP/OSDI/NSDI/EuroSys account for the majority of high-impact work
- SoCC serves as a reliable secondary venue for cloud computing papers
- The post-2023 expansion into ESEC/FSE, MLSys, and AIOps workshops reflects the broadening into AI-driven operations
- Venue loyalty to ACM SIGOPS venues (SOSP, SoCC) is very strong — he served as SOSP General Co-Chair in 2023

## Collaboration Patterns

### PhD Advisor: Rodrigo Fonseca (2011–present)
Fonseca is the most enduring collaborator. He appears on papers from 2013 through 2025 — a 12+ year span. During the PhD (2011–2018) he coauthored nearly every paper. Post-PhD, the collaboration continues on infrastructure and sustainability work (Carbon Accounting 2025, Intent-based Design 2025, Cerulean 2025). This is a genuine long-term intellectual partnership, not just a supervisor–student relationship.

### Microsoft Research (PhD Internships → MSR Career): Peter Bodik, Madan Musuvathi, Suman Nath
Bodik and Musuvathi coauthored the resource management papers during PhD internships (Retro, 2DFQ, HotDep — 2014–2016). Musuvathi reappears on the Retry Bugs paper (SOSP 2024), now as an MSR colleague. Suman Nath joins in the MSR era (2023–2024). This shows how internship connections matured into a permanent institutional home.

### MPI-SWS Group: Vaastav Anand, Thomas Davidson, Safya Alzayat, Antoine Kaufmann, Peter Druschel, Deepak Garg
- **Vaastav Anand** is the most prolific student collaborator: ~10+ papers (2019–2025) spanning Sifter, Blueprint, Hindsight, Palette, Cerulean, and more. He continues collaborating post-MPI-SWS.
- **Thomas Davidson** drove the visualization/human-factors thread (3 papers, 2020–2023)
- **Antoine Kaufmann** coauthored Clockwork, Blueprint, Palette, and co-chaired SOSP 2023
- **Peter Druschel** (MPI-SWS director) coauthored Groundhog and co-chaired SOSP 2023

### Industry Collaborators
- **Jonathan Kaldor** (Facebook) — Canopy (SOSP 2017), written during an internship
- **Pedro Las-Casas** — Weighted Sampling, Sifter (PhD/MPI-SWS era), then Building AI Agents, Cerulean, Intent-based Design (MSR era)
- **Ymir Vigfusson** — Clockwork (OSDI 2020), Hindsight (NSDI 2023)
- **Benjamin Sigelman** (Lightstep co-founder) — Principled Workflow-Centric Tracing (SoCC 2016), O'Reilly Book (2020)

### MSR Cloud Reliability Group: Chetan Bansal, Minghua Ma, Gagan Somashekar
These are the primary MSR-era collaborators on AIOps work (2023–2025). Papers tend to be larger teams (6–10 authors), reflecting the industrial research lab model.

### Team Size Patterns
- **PhD era:** Small teams (2–4 authors). Mace is typically first author.
- **MPI-SWS era:** Small-to-medium teams (2–7 authors). Mace is typically last author (senior role).
- **MSR era:** Larger teams (5–10 authors). Mace appears in varying positions, reflecting collaborative lab culture.
- **Solo work:** PhD thesis (2018), End-to-End Tracing survey (2017). Very few single-author publications.

## Citation Landscape

### Most Cited Papers (Google Scholar, mid-2025)

| Rank | Paper | Venue | Year | Citations |
|------|-------|-------|------|-----------|
| 1 | Serving DNNs like Clockwork | OSDI 2020 | 2020 | **~468** |
| 2 | Pivot Tracing | SOSP 2015 | 2015 | **~403** |
| 3 | Canopy | SOSP 2017 | 2017 | **~256** |
| 4 | Retro | NSDI 2015 | 2015 | **~154** |
| 5 | Distributed Tracing in Practice | O'Reilly 2020 | 2020 | ~99 |
| 6 | Principled Workflow-Centric Tracing | SoCC 2016 | 2016 | ~94 |
| 7 | Universal Context Propagation | EuroSys 2018 | 2018 | ~79 |
| 8 | Sifter | SoCC 2019 | 2019 | ~70 |
| 9 | Building AI Agents for Autonomous Clouds | SoCC 2024 | 2024 | ~50 |
| 10 | Hindsight | NSDI 2023 | 2023 | ~50 |

**Overall metrics:** h-index 18, total citations ~2,161 (Google Scholar, mid-2025)

### Citation Trajectory
- **2015–2018:** Rapid rise driven by Pivot Tracing (403 citations) and Retro (154 citations). Established reputation in distributed tracing.
- **2017–2020:** Canopy (256) and Clockwork (468) became breakout hits — Clockwork's high citation count likely reflects the ML systems community's size and growth.
- **2020–2023:** Steady accrual from established papers plus new work. The O'Reilly book (99 citations) and Sifter (70) contribute.
- **2023–2025:** New cluster emerging around AIOps — "Building AI Agents for Autonomous Clouds" (50 citations in ~1 year) signals strong early traction.

### Breakout Hits
- **Clockwork (468):** Most-cited paper, despite being somewhat outside the core tracing thread. Likely amplified by ML systems community interest.
- **Pivot Tracing (403):** Signature paper of the career. Best Paper Award at SOSP, later featured as a CACM Research Highlight.
- **Canopy (256):** High-impact industry paper (Facebook production system). The large author list reflects its industry origins.

## Evidence

### Primary Sources Consulted
| Source | URL | Data Retrieved |
|--------|-----|----------------|
| Personal website (canonical pub list) | https://jonathanmace.github.io/ | Full publication list with PDFs, 2013–2025 |
| Google Scholar | https://scholar.google.com/citations?user=-j5wb9IAAAAJ&hl=en | Citation counts, h-index, full paper list including patents |
| Microsoft Research profile | https://www.microsoft.com/en-us/research/people/jonathanmace/ | Current role, project descriptions, bio |
| DBLP | https://dblp.org/pid/154/0937 | Bibliographic records |
| Brown University CS news | https://cs.brown.edu/news/2015/10/07/mace-roelke-and-fonseca-win-best-paper-award-sosp-2015/ | SOSP 2015 Best Paper Award |
| Brown University CS news | https://cs.brown.edu/news/2018/10/19/phd-alum-jonathan-mace-earns-honorable-mention-dennis-m-ritchie-doctoral-dissertation-award/ | Ritchie Award Honorable Mention |
| Brown University CS news | https://posts.cs.brown.edu/2016/01/12/jonathan-mace-receives-facebook-graduate-fellowship/ | Facebook PhD Fellowship |
| Saarland Informatics Campus | https://saarland-informatics-campus.de/piece-of-news/jonathan-mace-joins-mpi-sws/ | MPI-SWS appointment |
| SOSP 2023 organizers | https://sosp2023.mpi-sws.org/organizers.html | General Co-Chair role |
| Justia Patents | https://patents.justia.com/inventor/jonathan-christopher-mace | IBM patent records |
| CV PDF | https://jonathanmace.github.io/mace_cv.pdf | Career details, awards, service |

## Author vs. Venue / Coauthor Signal

### Patterns Stable Across Contexts (Author Signal)
- **Cross-cutting, end-to-end systems thinking** persists regardless of venue, coauthors, or institution. Whether the paper is about tracing (SOSP), fair queuing (SIGCOMM), DNN serving (OSDI), or AIOps (SoCC), Mace consistently frames problems in terms of visibility and control across component boundaries.
- **Framework-oriented design** — every major contribution is an architecture or toolkit, not a point optimization. This holds from Pivot Tracing (2015) through Blueprint (2023) through AIOpsLab (2025).
- **Emphasis on practical deployability** — papers include artifact evaluations, open-source code, and production deployment evidence. Two Distinguished/Best Paper Awards were artifact-related.

### Patterns Inherited from Collaborators or Venues
- **Resource management cluster** (2014–2016) was strongly shaped by the MSR internship collaboration with Bodik and Musuvathi. This thread did not continue independently after the PhD.
- **ML systems cluster** (2019–2020) was partly driven by MPI-SWS colleagues (Kaufmann, Gujarati, Vigfusson). Clockwork became a breakout hit partly because the ML systems community is large and citation-rich.
- **Visualization cluster** (2020–2023) was primarily driven by student Thomas Davidson's interests and was largely completed when he graduated.
- **AIOps cluster** (2023–present) is significantly shaped by the MSR Cloud Reliability Group environment. The larger team sizes and rapid publication pace reflect the industrial lab context.

### Key Distinction
The tracing/observability thread is clearly *intrinsic* to Mace's research identity — it persists across all three career phases (PhD, MPI-SWS, MSR), all collaborator networks, and all venues. Other clusters appear more *contextual* — driven by specific collaborators, students, or institutional opportunities — though they still reflect the same underlying systems philosophy.

## Confidence and Limits

### High-Confidence Findings
- **Career trajectory and affiliations**: IBM (2009–2011) → Brown PhD (2011–2018) → MPI-SWS (2018–2022) → MSR (2023–present). Verified across multiple sources.
- **Publication list completeness**: The personal website (2013–2025) is comprehensive. Cross-referencing with Google Scholar confirms coverage. The ~35 research publications and ~8 patents are well-documented.
- **Topic cluster identification**: The tracing core is unambiguous. The resource management, ML systems, and AIOps clusters are clearly delineated by time period and collaborators.
- **Citation counts**: Sourced from Google Scholar (mid-2025). These are approximate but reliable for relative ranking.
- **Awards**: SOSP 2015 Best Paper, OSDI 2020 Distinguished Artifact, Dennis M. Ritchie Honorable Mention, Facebook PhD Fellowship — all verified via institutional announcements.

### Tentative Findings
- **Pre-PhD career**: IBM experience and patents are documented but the exact scope of his IBM work (Extreme Blue internship, WebSphere, NLP research) is reconstructed from brief CV mentions and patent records.
- **Clockwork's citation outlier status**: The hypothesis that it's amplified by ML community size is reasonable but unverified. It may also reflect genuine cross-community impact.
- **Intent of career transitions**: The shift from MPI-SWS faculty to MSR senior researcher could reflect many factors. The narrative of "returning to industry-scale cloud systems" is inferred from publication patterns.

### Open Questions
- **What is Mace's current Google Scholar h-index breakdown** (h5-index, i10-index)? The h-index of 18 was found but year-specific metrics were not retrieved.
- **What is the full list of supervised PhD students** at MPI-SWS beyond those with published theses? The website lists 6 supervised theses but actual PhD graduates may differ.
- **Service record beyond SOSP 2023 General Chair?** Program committee memberships, editorial boards, and other service roles are not fully documented here.
- **What is the relationship between the IBM patent work and the research career?** The patents are on unrelated UI/web topics and appear to be purely from pre-academic industry work.
- **Are there additional publications in 2024–2025** not yet indexed? The AIOps/cloud reliability cluster is actively growing and some workshop papers may be missing.
