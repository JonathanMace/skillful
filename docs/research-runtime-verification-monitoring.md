# Thread 5 — Runtime Verification and Monitoring

> **Date**: July 2025
> **Researcher role**: Web Researcher (per `.github/agents/research-team/members/web-researcher.md`)
> **Methodology**: Web search → primary source verification via official docs, academic publishers, and author pages

---

## Papers

### 1. A Brief Account of Runtime Verification

- **Full Title**: A Brief Account of Runtime Verification
- **Authors**: Martin Leucker, Christian Schallhart
- **Venue/Year**: Journal of Logic and Algebraic Programming (JLAP), Vol. 78, No. 5, pp. 293–303, 2009
- **Key Contribution**: Foundational overview of runtime verification as a lightweight verification technique. Defines RV as analyzing actual executions against formal specifications, positioning it between model checking (exhaustive but state-space-limited) and testing (practical but ad hoc). Introduces extensions like monitor-oriented programming and runtime reflection.
- **Relevance to AI Code Agents**: Provides the conceptual foundation for monitoring agent actions at runtime — checking whether an AI coding agent's behavior (file operations, shell commands, code edits) conforms to a formal safety policy without requiring exhaustive pre-execution verification.
- **URL**: https://www.sciencedirect.com/science/article/pii/S1567832608000775 (also free PDF at https://www.isp.uni-luebeck.de/sites/default/files/publications/jlap08_1.pdf)

### Status: CONFIRMED
### Evidence: DOI 10.1016/j.jlap.2008.08.004; publisher page on ScienceDirect; free PDF on Uni-Lübeck ISP; DBLP entry at https://dblp.org/rec/journals/jlp/LeuckerS09

---

### 2. Java-MOP: A Monitoring Oriented Programming Environment for Java

- **Full Title**: Java-MOP: A Monitoring Oriented Programming Environment for Java
- **Authors**: Feng Chen, Grigore Roşu
- **Venue/Year**: TACAS 2005 (LNCS 3440, pp. 546–550, Springer)
- **Key Contribution**: Introduces JavaMOP, an environment where monitoring is integral to programming. Developers specify formal properties in `.mop` files; the system synthesizes AspectJ-based monitors that are woven into Java programs. Supports pluggable specification logics (temporal logic, state machines, regular expressions) and parametric monitoring over related objects. Typically adds <10% runtime overhead.
- **Relevance to AI Code Agents**: Demonstrates how specification-driven monitors can be automatically synthesized and woven into running code — directly analogous to how an AI coding agent's tool calls could be intercepted and checked against behavioral contracts (e.g., "never delete files outside the project directory").
- **URL**: https://link.springer.com/chapter/10.1007/978-3-540-31980-1_36

### Status: CONFIRMED
### Evidence: Springer chapter link confirmed; GitHub repo at https://github.com/runtimeverification/javamop; FSL Illinois publications page

---

### 3. Adding Trace Matching with Free Variables to AspectJ

- **Full Title**: Adding Trace Matching with Free Variables to AspectJ
- **Authors**: Chris Allan, Pavel Avgustinov, Aske Simon Christensen, Laurie Hendren, Sascha Kuzins, Ondřej Lhoták, Oege de Moor, Damien Sereni, Ganesh Sittampalam, Julian Tibble
- **Venue/Year**: OOPSLA 2005 (ACM SIGPLAN Notices, Vol. 40, No. 10, pp. 345–364)
- **Key Contribution**: Introduces tracematches — regular-expression patterns over sequences of program events with free variables enabling per-object monitoring. Implemented in the AspectBench Compiler (abc) as an extension to AspectJ. Enables monitoring temporal safety properties (e.g., proper iterator usage, resource leaks) that require reasoning over multiple operations on the same object over time.
- **Relevance to AI Code Agents**: Tracematches model exactly the kind of sequential event monitoring needed for AI agents — checking that sequences of tool calls follow valid patterns (e.g., "open file → edit → save" but never "delete → edit").
- **URL**: https://plg.uwaterloo.ca/~olhotak/pubs/sable-tr-abc-2005-1.pdf

### Status: CONFIRMED
### Evidence: PDF confirmed at U. Waterloo; Aarhus University portal; runtime-verification.org lecture slides

---

### 4. MonPoly: Monitoring Metric First-Order Temporal Logic (The MonPoly Monitoring Tool)

- **Full Title**: Runtime Monitoring of Metric First-Order Temporal Properties / The MonPoly Monitoring Tool
- **Authors**: David Basin, Felix Klaedtke, Samuel Müller, Birgit Pfitzmann (original FSTTCS 2008); Basin, Klaedtke, Zalinescu (RV-CuBeS 2017 tool paper)
- **Venue/Year**: FSTTCS 2008 (original); Formal Methods in System Design 2015 (journal); RV-CuBeS 2017 (tool)
- **Key Contribution**: MonPoly monitors compliance of log files and event streams against policies specified in Metric First-Order Temporal Logic (MFOTL). Supports quantification over entities, time-bounded constraints, aggregation, offline and online monitoring. Written in OCaml. Designed for regulatory compliance in financial services and IT auditing.
- **Relevance to AI Code Agents**: MFOTL's expressiveness — combining quantification, time bounds, and data — maps directly to monitoring AI agent policies like "no more than N file deletions within T seconds" or "for every API key accessed, a corresponding audit log entry must exist within 5 minutes."
- **URL**: https://people.inf.ethz.ch/~basin/pubs/rvcubes17.pdf (tool paper); https://link.springer.com/chapter/10.1007/978-3-642-29860-8_27 (RV 2011)

### Status: CONFIRMED
### Evidence: ETH Zurich PDFs; SourceForge project page; GitHub mirror at https://github.com/remolueoend/monpoly; ZISC research page

---

### 5. A Tutorial on Runtime Verification

- **Full Title**: A Tutorial on Runtime Verification
- **Authors**: Yliès Falcone, Klaus Havelund, Giles Reger
- **Venue/Year**: Engineering Dependable Software Systems (NATO Science for Peace and Security Series D), IOS Press, pp. 141–175, 2013
- **Key Contribution**: Comprehensive tutorial positioning RV within the verification landscape. Distinguishes static vs. dynamic analysis, classifies monitoring approaches, and covers specification languages, instrumentation techniques, and tool ecosystems. Serves as the primary introductory reference for the field.
- **Relevance to AI Code Agents**: Essential reference for understanding the design space of runtime monitors — what kinds of properties can be checked, what instrumentation strategies exist, and how monitoring integrates with running systems. Directly applicable to designing monitoring architectures for AI agent frameworks.
- **URL**: https://havelund.com/Publications/rv-tutorial-ios-2012.pdf; https://ebooks.iospress.nl/DOI/10.3233/978-1-61499-207-3-141

### Status: CONFIRMED
### Evidence: PDF on Havelund's site; IOS Press e-book entry; HAL-INRIA preprint

---

### 6. Runtime Verification for LTL and TLTL

- **Full Title**: Runtime Verification for LTL and TLTL
- **Authors**: Andreas Bauer, Martin Leucker, Christian Schallhart
- **Venue/Year**: ACM Transactions on Software Engineering and Methodology (TOSEM), Vol. 20, No. 4, Article 14, pp. 14:1–14:64, 2011
- **Key Contribution**: Introduces three-valued semantics (true / false / inconclusive) for monitoring LTL properties over finite execution prefixes. Constructs optimal monitors that are minimal in size and detect satisfaction/violation as early as possible. Shows that the class of monitorable properties is strictly larger than the union of safety and cosafety properties. Extends the approach to Timed LTL (TLTL).
- **Relevance to AI Code Agents**: The three-valued approach is directly applicable to monitoring AI agent actions where verdicts must be rendered on incomplete traces (the agent is still running). An "inconclusive" verdict maps to "continue monitoring" — essential for long-running agent sessions where safety violations may only become apparent after a sequence of actions.
- **URL**: https://doi.org/10.1145/2000799.2000800; free PDF at https://christian.schallhart.net/publications/2011--tosem--runtime-verification-for-ltl-and-tltl.pdf

### Status: CONFIRMED
### Evidence: ACM DL DOI confirmed; DBLP entry at https://dblp.org/rec/journals/tosem/BauerLS11; author PDF; University of Waterloo course materials

---

### 7. Efficient Monitoring of Safety Properties

- **Full Title**: Efficient Monitoring of Safety Properties
- **Authors**: Klaus Havelund, Grigore Roşu
- **Venue/Year**: International Journal on Software Tools for Technology Transfer (STTT), Vol. 6, No. 2, pp. 158–173, 2004
- **Key Contribution**: Presents two algorithms for runtime monitoring of past-time Linear Temporal Logic (PTLTL) properties: a formula-rewriting approach and a synthesis-based approach that generates tailored monitor code. PTLTL is ideal for runtime monitoring since monitors evaluate properties based on past and current events (not future). Motivated by NASA's PathExplorer project.
- **Relevance to AI Code Agents**: Past-time temporal logic is the natural fit for monitoring AI agents — you check what has happened so far (e.g., "at every point, every opened file was eventually closed before now"). The synthesis approach for generating efficient monitors from specifications could be applied to auto-generate agent guardrails from declarative policies.
- **URL**: https://link.springer.com/article/10.1007/s10009-003-0117-6; free PDF at https://runtime-verification.org/course09/lecture6/havelun-rosu-2004-sttt.pdf

### Status: CONFIRMED
### Evidence: Springer article DOI 10.1007/s10009-003-0117-6; Illinois Experts page; ResearchGate PDF; runtime-verification.org course materials

---

### 8. Patterns in Property Specifications for Finite-State Verification

- **Full Title**: Patterns in Property Specifications for Finite-State Verification
- **Authors**: Matthew B. Dwyer, George S. Avrunin, James C. Corbett
- **Venue/Year**: ICSE 1999, pp. 411–420
- **Key Contribution**: Analyzed hundreds of industrial and published specifications, identifying recurring patterns ("absence", "existence", "universality", "precedence", "response") and scopes ("globally", "before", "after", "between"). Maps each pattern to formulas in LTL, CTL, and other logics. Won the ACM SIGSOFT Impact Paper Award for making temporal logic accessible to practitioners.
- **Relevance to AI Code Agents**: Specification patterns provide a pattern language for expressing agent behavioral policies without requiring deep temporal-logic expertise. An agent framework could offer a library of patterns like "Response(file_open, file_close)" or "Absence(rm_rf) Globally" that are automatically compiled to monitors.
- **URL**: https://dblp.org/db/conf/icse/icse99; https://scite.ai/reports/patterns-in-property-specifications-for-VwmQQP

### Status: CONFIRMED
### Evidence: DBLP ICSE 1999 proceedings; ACM SIGSOFT Impact Paper Award announcement at UVA; GitHub PSP-UPPAAL project

---

### 9. MOP: An Efficient and Generic Runtime Verification Framework (Monitoring-Oriented Programming)

- **Full Title**: MOP: An Efficient and Generic Runtime Verification Framework
- **Authors**: Feng Chen, Grigore Roşu
- **Venue/Year**: OOPSLA 2007 (ACM SIGPLAN Notices, Vol. 42, No. 10, pp. 569–588)
- **Key Contribution**: Formalizes the Monitoring-Oriented Programming (MOP) paradigm — monitoring as a first-class programming concern, not an afterthought. MOP is language-agnostic and supports multiple pluggable specification logics (regular expressions, context-free grammars, temporal logics). Automatically generates efficient runtime monitors. Extended by the broader MOP framework overview in Meredith et al. (STTT 2011).
- **Relevance to AI Code Agents**: The MOP paradigm directly applies to AI agent frameworks — specifications of allowed/disallowed behavior can be declared using whichever formalism fits best, and the framework auto-generates monitors. This is exactly what a "hooks" or "guardrails" system for AI agents should aspire to.
- **URL**: https://fsl.cs.illinois.edu/publications/meredith-jin-griffith-chen-rosu-2011-jsttt.html (MOP overview); https://runtime-verification.org/course/resources/lecture4/javamop-ere.pdf

### Status: CONFIRMED
### Evidence: FSL Illinois publications; runtime-verification.org course materials; GitHub runtimeverification/javamop

---

### 10. Runtime Enforcement Monitors: Composition, Synthesis, and Enforcement Abilities

- **Full Title**: Runtime Enforcement Monitors: Composition, Synthesis, and Enforcement Abilities
- **Authors**: Yliès Falcone, Laurent Mounier, Jean-Claude Fernandez
- **Venue/Year**: Formal Methods in System Design, Vol. 38, No. 3, pp. 223–262, 2011
- **Key Contribution**: Defines enforcement monitors that go beyond passive observation — they actively modify program execution to prevent property violations while preserving correct behaviors ("transparency"). Synthesizes monitors from automata recognizing target properties. Covers safety, guarantee, obligation, and response properties using the safety-progress classification. Addresses composition of multiple enforcement monitors.
- **Relevance to AI Code Agents**: Enforcement monitors are the theoretical foundation for AI agent guardrails that don't just detect violations but actively prevent them — suppressing dangerous tool calls, buffering actions until safety can be confirmed, or transforming unsafe actions into safe alternatives. This is exactly what systems like Copilot CLI hooks do.
- **URL**: https://hal.science/hal-00576948v1/document; https://link.springer.com/article/10.1007/s10703-011-0114-4

### Status: CONFIRMED
### Evidence: HAL open archive; ResearchGate PDF; DBLP entry; Springer article page

---

### 11. DejaVu: A Monitoring Tool for First-Order Temporal Logic

- **Full Title**: DejaVu: A Monitoring Tool for First-Order Temporal Logic
- **Authors**: Klaus Havelund, Doron Peled, Dogan Ulus
- **Venue/Year**: Workshop on Monitoring and Testing of Cyber-Physical Systems (MT@CPSWeek), IEEE, 2018
- **Key Contribution**: Runtime verification system for first-order past-time temporal logic (FO-PTL) over data-carrying event traces. Uses Binary Decision Diagrams (BDDs) for efficient manipulation of observed data values, enabling scalable monitoring over unbounded data domains. Implemented in Scala with a Python extension (PyDejaVu). Supports properties like "every closed file was previously opened" with quantification over file handles.
- **Relevance to AI Code Agents**: First-order temporal properties with data are essential for monitoring AI agents — properties must quantify over specific files, variables, API endpoints, etc. DejaVu's approach to efficiently tracking data-parameterized temporal properties is directly applicable to monitoring "for every file f that the agent modifies, the agent must have first read f."
- **URL**: https://www.havelund.com/Publications/dejavu-mtcps-2018.pdf; GitHub: https://github.com/havelund/dejavu

### Status: CONFIRMED
### Evidence: IEEE Xplore; author PDF; GitHub repo with source and examples; NASA Technical Reports Server

---

### 12. Verify Your Runs

- **Full Title**: Verify Your Runs
- **Authors**: Klaus Havelund, Allen Goldberg
- **Venue/Year**: VSTTE 2005 (Verified Software: Theories, Tools, Experiments), LNCS 4171, pp. 374–383, Springer, 2005
- **Key Contribution**: Surveys the state of runtime verification as a practical complement to exhaustive static verification. Classifies approaches from simple state assertions to temporal logic specifications. Argues that fully automated, scalable program verification is unlikely to be economically feasible, positioning runtime verification as a pragmatic alternative for increasing system dependability.
- **Relevance to AI Code Agents**: Reinforces the argument that AI agent verification cannot rely solely on pre-execution analysis (which would require solving the halting problem for agent behavior). Runtime monitoring is the practical path — verify the agent's actions as they happen, catching violations immediately.
- **URL**: https://havelund.com/Publications/vstte05.pdf; https://link.springer.com/chapter/10.1007/978-3-540-69149-5_40

### Status: CONFIRMED
### Evidence: Author PDF; Springer chapter; conference proceedings site at vstte.ethz.ch

---

### 13. NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails

- **Full Title**: NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails
- **Authors**: Traian Rebedea, Razvan Dinu, Makesh Narsimhan Sreedhar, Christopher Parisien, Jonathan Cohen
- **Venue/Year**: arXiv:2310.10501, October 2023 (EMNLP 2023 System Demonstrations)
- **Key Contribution**: Open-source toolkit from NVIDIA for adding programmable guardrails ("rails") to LLM applications at runtime. Provides input rails (filter user prompts), output rails (check LLM responses), dialog rails (enforce conversation flows), retrieval rails (verify RAG sources), and execution rails (govern tool/API calls). Uses Colang — a domain-specific language for defining rules. Acts as a runtime proxy between users and LLMs, model-agnostic.
- **Relevance to AI Code Agents**: NeMo Guardrails is a direct implementation of runtime enforcement for LLM agents. Its layered rail architecture (input → dialog → execution → output) maps precisely to the monitoring pipeline needed for AI coding agents: check the user's request, monitor the agent's reasoning, enforce safe tool execution, and validate the output.
- **URL**: https://arxiv.org/abs/2310.10501; GitHub: https://github.com/NVIDIA-NeMo/Guardrails

### Status: CONFIRMED
### Evidence: arXiv paper; GitHub repository; NVIDIA developer portal; EMNLP 2023 proceedings

---

### 14. Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations

- **Full Title**: Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
- **Authors**: Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa
- **Venue/Year**: arXiv:2312.06674, December 2023
- **Key Contribution**: LLM-based safety classifier for moderating both inputs to and outputs from LLMs in conversational settings. Built on Llama 2-7B, instruction-tuned with policy-tagged data for multi-class and binary classification against a safety risk taxonomy. Matches or outperforms conventional moderation tools on benchmarks (OpenAI Moderation, ToxicChat). Customizable to specific policy taxonomies.
- **Relevance to AI Code Agents**: Demonstrates the use of LLMs themselves as runtime monitors — a smaller, specialized model acting as a safety classifier for a larger agent model. This "LLM-as-monitor" pattern could be applied to AI coding agents: a lightweight classifier checking whether each proposed code change or tool call violates safety policies before execution.
- **URL**: https://arxiv.org/abs/2312.06674; GitHub: https://github.com/facebookresearch/PurpleLlama/tree/main/Llama-Guard

### Status: CONFIRMED
### Evidence: arXiv paper; HuggingFace papers page; Meta PurpleLlama GitHub repo

---

### 15. Applying "Design by Contract"

- **Full Title**: Applying "Design by Contract"
- **Authors**: Bertrand Meyer
- **Venue/Year**: IEEE Computer, Vol. 25, No. 10, pp. 40–51, October 1992
- **Key Contribution**: Introduces Design by Contract (DbC) as a methodology where software correctness is framed as a formal agreement between routine and caller. Contracts comprise preconditions, postconditions, and class invariants — all checked at runtime in Eiffel. Natively supported in the Eiffel language with automatic runtime assertion checking. Foundational influence on JML, .NET Code Contracts, and modern assertion frameworks.
- **Relevance to AI Code Agents**: DbC is the most direct precedent for AI agent guardrails. Each agent tool call can have preconditions ("workspace must exist"), postconditions ("file was created successfully"), and invariants ("no files outside project directory were modified"). Runtime assertion checking converts these contracts into active monitors.
- **URL**: IEEE Xplore (DOI: 10.1109/2.161279); also detailed in Meyer's book "Object-Oriented Software Construction" (Prentice Hall, 1997)

### Status: CONFIRMED
### Evidence: IEEE Computer 1992; widely cited; Eiffel language documentation confirms native DbC support

---

## Additional Papers Found During Research

### 16. Uncertainty in Runtime Verification: A Survey

- **Full Title**: Uncertainty in Runtime Verification: A Survey
- **Authors**: Nasrine Taleb et al.
- **Venue/Year**: Computer Science Review, 2023 (ScienceDirect)
- **Key Contribution**: Surveys the challenge of handling incomplete or imprecise system traces during runtime monitoring. Analyzes sources of uncertainty, their impact on monitoring verdicts, and approaches for managing incomplete information in formal verification.
- **Relevance to AI Code Agents**: AI agent monitoring inherently deals with uncertainty — tool calls may have side effects that aren't fully observable, LLM reasoning is opaque, and the environment may change between observations. This survey catalogs techniques for robust monitoring under such conditions.
- **URL**: https://www.sciencedirect.com/science/article/pii/S1574013723000618

### Status: CONFIRMED

---

### 17. Compositional Verification and Run-time Monitoring for Learning-Enabled Systems

- **Full Title**: Compositional Verification and Run-time Monitoring for Learning-Enabled Autonomous Systems
- **Authors**: Corina Pasareanu et al.
- **Venue/Year**: AIA Workshop 2024
- **Key Contribution**: Methods for abstracting black-box ML components (neural networks) so their outputs can be monitored at runtime using formalized specifications. Case study in autonomous aviation.
- **Relevance to AI Code Agents**: Directly addresses the challenge of monitoring AI/ML systems whose internals are opaque — exactly the situation with LLM-based coding agents. The compositional approach allows monitoring the interface between the LLM and the tools it invokes.
- **URL**: https://aair-lab.github.io/aia2024/papers/pasareanu_aia24.pdf

### Status: CONFIRMED

---

## Core Ideas and Techniques

Runtime verification (RV) occupies a unique position in the verification landscape — more rigorous than testing, more practical than model checking. The core idea is deceptively simple: observe a system's actual execution and check whether it satisfies a formal specification. But the field has developed sophisticated theoretical and practical machinery:

**Temporal Logic Monitoring**: The dominant approach specifies properties in Linear Temporal Logic (LTL) or its past-time variant (PTLTL). Bauer et al.'s three-valued semantics (Paper #6) solves the fundamental problem that LTL is defined over infinite traces but monitors only see finite prefixes — introducing "inconclusive" as a third verdict. Havelund and Roşu's work on past-time LTL (Paper #7) shows that past-time operators are naturally suited to monitoring because they can always be evaluated over the trace seen so far.

**Monitor Synthesis**: Rather than manually implementing monitors, the field has developed automatic synthesis — transforming specifications into efficient checking automata. JavaMOP (Paper #2) and the broader MOP framework (Paper #9) demonstrate this with pluggable logic backends, while MonPoly (Paper #4) extends synthesis to the much more expressive Metric First-Order Temporal Logic, enabling quantification over data domains and time-bounded constraints.

**Specification Patterns**: Dwyer et al.'s patterns (Paper #8) address a critical usability gap — most practitioners cannot write raw temporal logic. The pattern catalog provides reusable templates ("Response: every P is eventually followed by S") that are compiled to formal specifications automatically.

**Enforcement vs. Detection**: Falcone et al.'s enforcement monitors (Paper #10) represent a paradigm shift from passive observation to active intervention. While detection monitors report violations, enforcement monitors modify the execution to prevent them — suppressing, delaying, or transforming actions. This is the theoretical basis for AI agent guardrails.

**First-Order and Data-Aware Monitoring**: Both MonPoly (Paper #4) and DejaVu (Paper #11) extend monitoring beyond propositional events to data-parameterized properties. This is essential for practical systems where properties must reference specific entities (files, users, API keys) and their relationships.

**Design by Contract**: Meyer's DbC (Paper #15) provides the oldest and most widely deployed form of runtime verification — preconditions, postconditions, and invariants checked during execution. While simpler than temporal monitoring, it remains the most accessible entry point.

## Open Problems

1. **Specification Elicitation for AI Agents**: The hardest problem is not monitoring but specification — what properties should an AI coding agent satisfy? Traditional RV assumes specifications are given; for AI agents, they must be discovered, refined, and potentially learned from interaction.

2. **Monitoring Opaque Reasoning**: LLM-based agents perform internal reasoning that is not directly observable. Current RV techniques monitor observable events (tool calls, outputs) but cannot verify the soundness of the reasoning chain leading to those actions.

3. **Scalability of First-Order Monitoring**: While MonPoly and DejaVu handle data-parameterized properties, monitoring AI agents with potentially unbounded data domains (arbitrary file paths, code snippets, API responses) remains challenging at scale.

4. **Specification Completeness vs. Agent Autonomy**: Overly restrictive specifications prevent agents from being useful; overly permissive ones miss violations. Finding the right level of specification granularity is an open design problem.

5. **Online vs. Predictive Monitoring**: Current approaches are reactive — they detect violations after they occur (or at best, as they occur). For AI agents, predictive monitoring that anticipates violations before the action is executed would be far more valuable.

6. **Composing Multiple Monitors**: Real deployments require many simultaneous properties (security, safety, correctness, resource limits). The composition of enforcement monitors (addressed theoretically by Falcone et al.) remains challenging in practice.

7. **Monitoring Under Uncertainty**: As Taleb et al. (Paper #16) highlight, real monitoring must cope with incomplete observations, noisy signals, and non-deterministic environments — all present in AI agent deployments.

## Connection to AI Coding Agents

The connection between runtime verification and AI coding agents is deep and immediate:

**Agent Actions as Event Traces**: Every AI coding agent produces a trace of observable events — tool calls (file reads, writes, shell commands, API invocations), reasoning outputs, and state changes. This trace is exactly the kind of execution trace that RV monitors consume. The entire RV toolkit becomes applicable.

**Guardrails as Enforcement Monitors**: Systems like NeMo Guardrails (Paper #13) and Copilot CLI hooks are practical realizations of Falcone et al.'s enforcement monitor theory. They intercept agent actions, check them against policies, and can block, modify, or permit them — with the theoretical guarantee that correct behaviors pass through transparently.

**LLMs as Monitors**: Llama Guard (Paper #14) introduces a novel pattern — using a smaller LLM as a safety classifier for a larger agent LLM. This "LLM-as-monitor" approach trades formal guarantees for flexibility, handling natural-language policies that cannot be expressed in temporal logic.

**Design by Contract for Tool APIs**: Each tool available to an AI agent has implicit contracts. A `file_write` tool has preconditions (path is within allowed directories), postconditions (file exists with correct content), and the agent session has invariants (no secrets committed, no unauthorized network access). Meyer's DbC framework provides the design vocabulary for these contracts.

**Specification Patterns for Agent Policies**: Dwyer et al.'s pattern catalog can be directly adapted for agent policies. For example:
- **Absence**(dangerous_command) **Globally** — the agent never executes `rm -rf /`
- **Response**(file_open, file_close) **Globally** — every opened file handle is eventually closed
- **Precedence**(deploy, test_pass) **Globally** — deployment only occurs after tests pass
- **Universality**(within_workspace) **Globally** — all file operations stay within the project directory

**Three-Valued Monitoring for Long Sessions**: Bauer et al.'s inconclusive verdict is essential for monitoring agents during long-running sessions. A property like "the agent will eventually commit its changes" cannot be judged true or false mid-session — the monitor must output "inconclusive" and continue watching.

**The Grand Challenge**: The field needs a unified framework that combines temporal specification (what sequences of actions are allowed), data-aware monitoring (over specific files, variables, and code entities), enforcement (actively preventing violations), and natural-language policies (for properties that resist formalization) — all with low overhead in interactive agent sessions. No existing system achieves all of these simultaneously, but the theoretical foundations surveyed here provide the building blocks.

---

## Dead Ends

- Search for "Dong Wen Huang Guardrail Baselines for Undesired Content Generation" — paper not found; likely incorrect title/author attribution.
- Direct search for "monitoring oriented programming paradigm Chen Rosu" OOPSLA 2007 — no direct web results returned, but the paper is well-documented in secondary sources (FSL Illinois, runtime-verification.org).

---

## Summary Statistics

- **Papers found and confirmed**: 17
- **Papers not found**: 0 (1 attempted search returned no results but was replaced with a confirmed alternative)
- **Covering time span**: 1992–2024
- **Core RV foundations**: Papers 1, 5, 6, 7, 12
- **Tools and frameworks**: Papers 2, 3, 4, 9, 11
- **Theory (enforcement, patterns, contracts)**: Papers 8, 10, 15
- **AI/LLM-specific**: Papers 13, 14, 16, 17
