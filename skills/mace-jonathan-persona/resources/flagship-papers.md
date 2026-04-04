# Jonathan Mace — Flagship Papers

## Persona Findings

Jonathan Mace is a systems researcher whose career traces a remarkably coherent arc from **distributed tracing and observability** through **multi-tenant resource management** to **systems infrastructure for cloud reliability and AI operations**. His intellectual identity is defined by several recurring themes:

1. **Cross-cutting concerns in distributed systems** — The unifying thread across nearly all his work is the idea that observability, resource management, and correctness enforcement must cut across component boundaries. His PhD thesis literally formalizes this as "cross-cutting tools" and proposes a universal architecture for them.

2. **Abstractions that compose** — Mace consistently seeks general abstractions (baggage contexts, pivot operators, retroactive sampling) rather than point solutions. He favors layered, decoupled designs where instrumentation is separated from analysis logic.

3. **Practical systems with theoretical grounding** — His papers blend production-scale deployment (Facebook's Canopy, Azure's 2DFQ, Hadoop evaluations) with principled design. He is comfortable operating at the theory-practice boundary.

4. **Intellectual leadership on tracing** — Mace is arguably the most prolific and influential individual researcher in the distributed tracing subfield, spanning foundational work (Pivot Tracing), production systems (Canopy), sampling theory (Weighted Sampling, Sifter, Hindsight), and a practitioner book (Distributed Tracing in Practice).

5. **Characteristic writing voice** — His first-author papers open with crisp problem statements that frame a gap between what practitioners need and what current tools provide. He favors concrete motivating examples, clean system diagrams, and evaluations on real heterogeneous deployments rather than synthetic benchmarks.

6. **Career trajectory** — PhD at Brown University under Rodrigo Fonseca (2013–2018), internships at Microsoft Research, then faculty and group leader at MPI-SWS (2019–2023), now Senior Researcher at Microsoft Research Redmond. The career spans academia and industry, with a consistent pivot toward larger-scale impact.

## Recommended Reading Set

| # | Paper | Year | Venue | Role | Citations | Why Selected |
|---|-------|------|-------|------|-----------|--------------|
| 1 | Pivot Tracing: Dynamic Causal Monitoring for Distributed Systems | 2015 | SOSP | First author | ~403 | Best Paper Award; foundational work defining his research identity |
| 2 | Retro: Targeted Resource Management in Multi-Tenant Distributed Systems | 2015 | NSDI | First author | ~154 | Early PhD work; shows the resource-management side of his research |
| 3 | 2DFQ: Two-Dimensional Fair Queuing for Multi-Tenant Cloud Services | 2016 | SIGCOMM | First author | ~45 | Different venue (networking); shows range beyond tracing |
| 4 | Canopy: An End-to-End Performance Tracing And Analysis System | 2017 | SOSP | Co-author (2nd) | ~256 | Facebook production system; industry-scale tracing |
| 5 | Universal Context Propagation for Distributed System Instrumentation | 2018 | EuroSys | First author | ~79 | Core thesis contribution; the "baggage" abstraction |
| 6 | Sifter: Scalable Sampling for Distributed Traces, without Feature Engineering | 2019 | SoCC | Senior/last author | ~70 | Advisor role; trace sampling line of work |
| 7 | Serving DNNs like Clockwork: Performance Predictability from the Bottom Up | 2020 | OSDI | Senior/last author | ~468 | Highest-cited; shows ML-systems expansion; Distinguished Artifact Award |
| 8 | The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems | 2023 | NSDI | Senior/last author | ~50 | Mature tracing vision; retroactive sampling abstraction |
| 9 | Blueprint: A Toolchain for Highly-Reconfigurable Microservice Applications | 2023 | SOSP | Senior/last author | ~17 | Systems tooling; benchmarking infrastructure for microservices |
| 10 | Groundhog: Efficient Request Isolation in FaaS | 2023 | EuroSys | Co-author (2nd) | ~31 | OS/systems work; FaaS security via snapshot-restore |

## Paper Summaries

### Paper 1: Pivot Tracing: Dynamic Causal Monitoring for Distributed Systems

- **Full citation**: Jonathan Mace, Ryan Roelke, Rodrigo Fonseca. "Pivot Tracing: Dynamic Causal Monitoring for Distributed Systems." Proceedings of the 25th ACM Symposium on Operating Systems Principles (SOSP), 2015.
- **URL/DOI**: https://sigops.org/s/conferences/sosp/2015/current/2015-Monterey/122-mace-online.pdf
- **Abstract summary**: Introduces Pivot Tracing, a monitoring framework that combines dynamic instrumentation with a "happened-before join" relational operator. Users can define metrics at one point in a distributed system and filter/group by events at other points — even across component or machine boundaries — at runtime without redeploying. Evaluated on a heterogeneous Hadoop cluster (HDFS, HBase, MapReduce, YARN), demonstrating identification of diverse root causes with low overhead.
- **Why it's representative**: This is the paper that established Mace's reputation. It won Best Paper at SOSP 2015, one of the most competitive venues in systems. It encapsulates his core research vision: dynamic, cross-cutting observability for distributed systems.
- **What it reveals about the author's style**: Clean formulation of a new operator (the happened-before join), strong motivation from real operational pain points, and a practical evaluation on production-like heterogeneous systems rather than toy benchmarks. The paper introduces a novel conceptual vocabulary ("pivot") that reframes how practitioners think about monitoring.

### Paper 2: Retro: Targeted Resource Management in Multi-Tenant Distributed Systems

- **Full citation**: Jonathan Mace, Peter Bodik, Rodrigo Fonseca, Madanlal Musuvathi. "Retro: Targeted Resource Management in Multi-Tenant Distributed Systems." 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2015.
- **URL/DOI**: https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/mace
- **Abstract summary**: Retro is a resource management framework for shared distributed systems that monitors per-tenant resource usage across distributed components and exposes it through a high-level API to centralized policies. Policies can shape tenant resource consumption via control points enforcing fairness and rate-limiting. Evaluated across five distributed systems (HBase, YARN, MapReduce, HDFS, ZooKeeper) with three policies: bottleneck fairness, dominant resource fairness, and latency guarantees.
- **Why it's representative**: Shows the resource-management side of Mace's research, complementing his tracing work. Written during Microsoft Research internship. Demonstrates his early ability to build cross-system infrastructure that spans multiple distributed components.
- **What it reveals about the author's style**: Emphasis on multi-system evaluation rather than single-system microbenchmarks. The paper shares Pivot Tracing's cross-cutting philosophy but applies it to resource management rather than monitoring — revealing the deeper architectural vision that unifies both.

### Paper 3: 2DFQ: Two-Dimensional Fair Queuing for Multi-Tenant Cloud Services

- **Full citation**: Jonathan Mace, Peter Bodik, Madanlal Musuvathi, Rodrigo Fonseca, Krishnan Varadarajan. "2DFQ: Two-Dimensional Fair Queuing for Multi-Tenant Cloud Services." Proceedings of the ACM SIGCOMM 2016 Conference, 2016.
- **URL/DOI**: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/08/mace162dfq.pdf
- **Abstract summary**: Proposes Two-Dimensional Fair Queuing to address fairness in multi-tenant cloud services where tenants share thread pools. Traditional fair schedulers (WFQ, WF2Q) suffer from bursty schedules when request costs are unknown and high-variance. 2DFQ spreads requests of different costs across threads, reducing burstiness by several orders of magnitude. Evaluated on production Azure Storage workloads.
- **Why it's representative**: Published at SIGCOMM (networking), showing Mace's range beyond the systems/tracing venues. The only paper in the set from a networking conference. Demonstrates his ability to contribute algorithmic solutions to scheduling problems, not just systems infrastructure.
- **What it reveals about the author's style**: More algorithmically focused than his tracing work, yet still motivated by a concrete production problem (Azure Storage). Shows comfort working at the intersection of theory (scheduling algorithms) and practice (production cloud workloads).

### Paper 4: Canopy: An End-to-End Performance Tracing And Analysis System

- **Full citation**: Jonathan Kaldor, Jonathan Mace, Michał Bejda, Edison Gao, Wiktor Kuropatwa, Joe O'Neill, Kian Win Ong, Bill Schaller, Pingjia Shan, Brendan Viscomi, Vinod Venkataraman, Kaushik Veeraraghavan, Yee Jiun Song. "Canopy: An End-to-End Performance Tracing And Analysis System." Proceedings of the 26th Symposium on Operating Systems Principles (SOSP), 2017.
- **URL/DOI**: https://jonathanmace.github.io/papers/kaldor2017canopy.pdf
- **Abstract summary**: Presents Facebook's end-to-end performance tracing infrastructure. Canopy records causally related performance data across browsers, mobile apps, and backend services, processing traces in near real-time. It derives user-specified features and outputs to performance datasets aggregating across billions of requests. Processes over 1 billion traces per day.
- **Why it's representative**: Shows Mace operating at maximum industrial scale during his Facebook internship/collaboration. The paper demonstrates that his tracing research vision works at planetary scale — a crucial validation of the ideas from Pivot Tracing.
- **What it reveals about the author's style**: Though not first author, this paper reflects Mace's deep influence on the design. It shares his characteristic concern with end-to-end causality, real-time analysis, and customizability. The industrial co-authorship context (many Facebook engineers) shows his ability to translate research ideas into production systems.

### Paper 5: Universal Context Propagation for Distributed System Instrumentation

- **Full citation**: Jonathan Mace, Rodrigo Fonseca. "Universal Context Propagation for Distributed System Instrumentation." Proceedings of the 13th EuroSys Conference, 2018.
- **URL/DOI**: http://static.cs.brown.edu/people/jcmace/papers/mace18universal.pdf
- **Abstract summary**: Proposes a layered architecture that separates the generic concern of context propagation from the specific logic of cross-cutting tools. At its heart is the "baggage context" — a general, opaque format that encapsulates all request-associated metadata, enabling complete decoupling of system instrumentation from tool logic. Implemented in Java and Go, with several cross-cutting tools ported to demonstrate the architecture.
- **Why it's representative**: This is the capstone of Mace's PhD work and the paper most directly expressing his architectural vision. The "baggage" concept has influenced the design of OpenTelemetry and other production tracing systems. Received Honorable Mention for the ACM Dennis M. Ritchie Doctoral Dissertation Award.
- **What it reveals about the author's style**: Maximum intellectual ambition — seeking not just a new tool but a universal architecture. The layered decomposition and emphasis on decoupling reveal a systems thinker who prioritizes composability and separation of concerns. The paper is written with unusual clarity for such an ambitious scope.

### Paper 6: Sifter: Scalable Sampling for Distributed Traces, without Feature Engineering

- **Full citation**: Pedro Las-Casas, Giorgi Papakerashvili, Vaastav Anand, Jonathan Mace. "Sifter: Scalable Sampling for Distributed Traces, without Feature Engineering." Proceedings of the ACM Symposium on Cloud Computing (SoCC), 2019.
- **URL/DOI**: https://jonathanmace.github.io/papers/lascasas2019sifter.pdf
- **Abstract summary**: Sifter is a general-purpose framework for biased trace sampling that favors edge-case code paths, infrequent request types, and anomalous events. It builds an unbiased low-dimensional model from the incoming trace stream, approximating typical behavior, then biases sampling toward traces that deviate from this model. Automatic, requires no feature engineering.
- **Why it's representative**: First paper where Mace appears as senior/advisor author (at MPI-SWS). Shows his ability to guide students on the trace sampling problem that would later culminate in Hindsight. The "needles in haystacks" framing is characteristic of his practical sensibility.
- **What it reveals about the author's style**: Mace as research leader rather than sole implementer. The problem framing — making tracing useful without requiring practitioners to know what to look for in advance — is quintessentially his concern.

### Paper 7: Serving DNNs like Clockwork: Performance Predictability from the Bottom Up

- **Full citation**: Arpan Gujarati, Reza Karimi, Safya Alzayat, Wei Hao, Antoine Kaufmann, Ymir Vigfusson, Jonathan Mace. "Serving DNNs like Clockwork: Performance Predictability from the Bottom Up." 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI), 2020.
- **URL/DOI**: https://arxiv.org/abs/2006.02464
- **Abstract summary**: Clockwork is a DNN serving system built on the insight that DNN inference times are inherently deterministic when isolated from external interference. By leveraging this predictability bottom-up, Clockwork provides tight end-to-end latency guarantees, supporting thousands of concurrent models while meeting 100ms latency targets for 99.9999% of requests. Distinguished Artifact Award.
- **Why it's representative**: Most highly cited paper (~468 citations). Demonstrates Mace's expansion beyond tracing into ML systems and performance engineering. Shows he can lead a research group producing impactful work in adjacent domains.
- **What it reveals about the author's style**: The "bottom-up" framing — building predictability from first principles rather than papering over unpredictability with over-provisioning — is characteristic of Mace's engineering philosophy. Distinguished Artifact Award reflects his emphasis on reproducible, well-engineered systems.

### Paper 8: The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems

- **Full citation**: Lei Zhang, Zhiqiang Xie, Vaastav Anand, Ymir Vigfusson, Jonathan Mace. "The Benefit of Hindsight: Tracing Edge-Cases in Distributed Systems." 20th USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2023.
- **URL/DOI**: https://www.usenix.org/system/files/nsdi23-zhang-lei.pdf
- **Abstract summary**: Hindsight implements "retroactive sampling" — trace data is always generated but not eagerly ingested. When edge-case symptoms are detected, Hindsight retroactively retrieves and persists trace data from all involved nodes. Analogized to a car dash-cam that saves footage only after detecting a collision. Scales to millions of requests per second with nanosecond-level overhead.
- **Why it's representative**: The mature culmination of the trace sampling line (Weighted Sampling → Sifter → Hindsight). Represents Mace's MPI-SWS period and shows the evolution of his thinking on the fundamental tracing problem.
- **What it reveals about the author's style**: The dash-cam analogy is classic Mace — making a systems concept immediately intuitive through a vivid metaphor. The "retroactive" framing elegantly resolves the tension between overhead and completeness that has haunted distributed tracing since its inception.

### Paper 9: Blueprint: A Toolchain for Highly-Reconfigurable Microservice Applications

- **Full citation**: Vaastav Anand, Deepak Garg, Antoine Kaufmann, Jonathan Mace. "Blueprint: A Toolchain for Highly-Reconfigurable Microservice Applications." Proceedings of the 29th Symposium on Operating Systems Principles (SOSP), 2023.
- **URL/DOI**: https://vaastavanand.com/assets/pdf/anand2023blueprint.pdf
- **Abstract summary**: Blueprint is a microservice development toolchain enabling rapid Configure-Build-Deploy cycles. With a few lines of code, users can reconfigure an application's design; Blueprint generates a fully functioning variant under the new design. Extensible, open-source, and supports all major microservice benchmarks.
- **Why it's representative**: Shows Mace's systems-building and tooling sensibility applied to experimental methodology. Rather than just studying microservices, he builds infrastructure to make microservice research itself more rigorous and reproducible.
- **What it reveals about the author's style**: Meta-level systems thinking — building tools for building tools. The emphasis on reconfigurability and rapid experimentation reflects an engineer-researcher who cares about the experimental methodology of the field, not just individual results.

### Paper 10: Groundhog: Efficient Request Isolation in FaaS

- **Full citation**: Mohamed Alzayat, Jonathan Mace, Peter Druschel, Deepak Garg. "Groundhog: Efficient Request Isolation in FaaS." Proceedings of the 18th European Conference on Computer Systems (EuroSys), 2023.
- **URL/DOI**: https://arxiv.org/pdf/2205.11458.pdf
- **Abstract summary**: Groundhog enforces strict sequential request isolation in FaaS by reverting execution environments to clean snapshots after each invocation. The approach is language/runtime-agnostic, requires no code modifications, and achieves strong isolation with modest overhead (1.5% median latency, 2.5% throughput). Implemented in OpenWhisk.
- **Why it's representative**: Shows Mace working in OS/systems territory (process isolation, snapshot-restore) distinct from his tracing work. Collaboration with Peter Druschel at MPI-SWS demonstrates his breadth in the systems community.
- **What it reveals about the author's style**: The pragmatic emphasis on "no modifications required" is characteristic — Mace consistently seeks solutions that are deployable without invasive changes to existing systems. The snapshot-restore approach is elegant in its simplicity.

## Papers Considered but Not Selected

- **Weighted Sampling of Execution Traces (SoCC 2018)** — Important precursor to Sifter and Hindsight, but the ideas are better represented by those later papers. Co-authored with Pedro Las-Casas and Rodrigo Fonseca; bridges the PhD and MPI-SWS periods. (~48 citations)

- **Principled Workflow-Centric Tracing of Distributed Systems (SoCC 2016)** — Collaborative work with Raja Sambasivan and Ben Sigelman on tracing methodology. Important for the tracing community but Mace is a middle author and the voice is more Sambasivan's. (~94 citations)

- **Distributed Tracing in Practice (O'Reilly, 2020)** — Co-authored book on practical tracing. Valuable for understanding Mace's practitioner-facing communication style, but it is a book rather than a research paper, and the voice is shared across five co-authors. (~99 citations)

- **Building AI Agents for Autonomous Clouds (SoCC 2024)** — Recent work on AI agents for cloud operations. Represents Mace's current research direction at Microsoft Research, but he is a middle author and the paper is very new. (~50 citations, rapidly growing)

- **Antipode: Enforcing Cross-Service Causal Consistency (SOSP 2023)** — Interesting causal consistency work, but Mace is a middle co-author and the lead voice is João Loff and Rodrigo Rodrigues. (~18 citations)

- **A Qualitative Interview Study of Distributed Tracing Visualisation (IEEE TVCG 2023)** — Unusual for Mace — a qualitative/HCI study. Shows breadth but less representative of his core systems voice. (~18 citations)

- **Towards General-Purpose Resource Management in Shared Cloud Services (HotDep 2014)** — Early workshop paper that previewed Retro. The ideas are fully subsumed by the NSDI 2015 paper.

- **Revisiting End-to-End Trace Comparison with Graph Kernels (MSc 2013/2014)** — Earliest research work; historically interesting as the seed of the tracing agenda but not published at a major venue.

- **AIOpsLab: A Holistic Framework for Evaluating AI Agents for Enabling Autonomous Clouds (MLSys 2025)** — Very recent, rapidly accumulating citations (~38), but Mace is a middle author and the work is still establishing itself.

- **Detection Is Better Than Cure: A Cloud Incidents Perspective (ESEC/FSE 2023)** — Applied cloud reliability work at Microsoft; Mace is last author but the paper's voice is more shaped by the software engineering venue norms.

- **If At First You Don't Succeed, Try, Try, Again...? (SOSP 2024)** — Retry bug detection using LLMs; interesting direction but Mace is a middle author.

## Author vs. Venue / Coauthor Signal

### Strongest author voice (prioritize for persona):
1. **Pivot Tracing (SOSP 2015)** — First-author, Best Paper; this is the definitive Mace paper
2. **Universal Context Propagation (EuroSys 2018)** — First-author, PhD capstone; pure expression of his architectural philosophy
3. **Retro (NSDI 2015)** — First-author; early but fully formed systems thinking
4. **2DFQ (SIGCOMM 2016)** — First-author; shows algorithmic range

### Strong author signal through advisory role:
5. **Hindsight (NSDI 2023)** — Senior/last author; the research vision is clearly Mace's even though students led execution
6. **Sifter (SoCC 2019)** — Senior author; early MPI-SWS advising work
7. **Clockwork (OSDI 2020)** — Senior/last author; group-led work but reflects his emphasis on performance predictability
8. **Blueprint (SOSP 2023)** — Senior/last author; tooling philosophy consistent with his broader vision

### Collaborative signal (useful but harder to isolate Mace's voice):
9. **Canopy (SOSP 2017)** — Co-author in large industry team; Mace's tracing expertise clearly shaped the design but the writing reflects Facebook's house style
10. **Groundhog (EuroSys 2023)** — Co-author with MPI-SWS colleagues; OS-flavored work with Druschel influence

### Venue effects to note:
- **SOSP/OSDI papers** tend to be longer, more thorough, with comprehensive evaluations — matches Mace's natural style
- **SIGCOMM (2DFQ)** has a more networking-oriented, algorithm-focused style — useful for separating Mace's voice from systems venue norms
- **NSDI papers** are shorter and more systems-focused — good medium for Mace's concise problem-solution framing
- **SoCC papers** are the most informal of the top venues — Sifter shows a more relaxed, practitioner-oriented voice

## Confidence and Limits

### High-confidence selections:
- **Pivot Tracing** — Undeniably the signature paper; must be included in any reading set
- **Universal Context Propagation** — The intellectual thesis statement; essential for understanding his architectural vision
- **Retro** — Core early work, first-author, complements the tracing side
- **Clockwork** — Highest impact, demonstrates breadth beyond tracing
- **Hindsight** — Mature statement of the tracing research program

### Moderate-confidence selections:
- **2DFQ** — Important for showing range but less cited; could be swapped for Weighted Sampling if more tracing depth is desired
- **Canopy** — Essential for the industry-scale perspective but Mace's individual voice is harder to isolate
- **Blueprint** — Important for the "meta-systems" tooling angle but relatively new
- **Sifter** — Important waypoint in the sampling line; could be omitted if Weighted Sampling + Hindsight cover the arc

### Tentative selection:
- **Groundhog** — Included for OS/systems breadth and MPI-SWS collaboration context, but could be replaced by Antipode (for causal consistency breadth) or the Tracing Visualisation paper (for methodological breadth)

### Open questions:
- **PhD Thesis vs. Individual Papers** — The thesis ("A Universal Architecture for Cross-Cutting Tools in Distributed Systems") is the most complete statement of Mace's vision, unifying Retro, Pivot Tracing, and Baggage. It could replace 2–3 individual papers for persona construction, but it is not a peer-reviewed publication at a conference. The Ritchie Award Honorable Mention validates its quality.
- **Recent AI/Cloud direction** — Mace's 2024–2025 work on AI agents for cloud operations (Building AI Agents, AIOpsLab, Cloud Atlas) represents a significant new research direction. These are too new to assess long-term impact but may become central to his identity. A persona built today should note this trajectory without over-weighting it.
- **Book inclusion** — "Distributed Tracing in Practice" is the clearest window into Mace's practitioner communication style. It is excluded from the academic reading set but should be consulted separately for persona voice calibration.
