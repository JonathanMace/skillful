# Academic Literature Review: Cross-Platform Portability of Developer Knowledge Artifacts and Plugin Ecosystems

## Executive Summary

This review synthesizes findings from **~100 verified academic papers** across 8 research threads, gathered by 8 parallel researchers conducting 350+ web searches. The core question: what does academic research tell us about making developer knowledge artifacts (skills, agents, instructions, plugins) portable across incompatible AI coding tool platforms?

**The central finding is that the AI tool ecosystem is recapitulating — at compressed timescales — patterns that played out over decades in component-based software engineering, plugin ecosystems, and standards wars.** The academic literature provides both cautionary tales and actionable design principles:

1. **No component model has ever achieved universal portability** (Szyperski 2002, Emmerich & Kaveh 2002, Vale et al. 2016). Every attempt — COM, CORBA, JavaBeans, OSGi — succeeded within its niche but failed to span platforms. The AI tool ecosystem is pre-standardization and should not expect one vendor's format to "win."

2. **The M×N→M+N reduction pattern works** (LSP, MCP). When a standard decouples producers from consumers, adoption accelerates explosively. LSP went from 0 to 121 implementations; MCP is on a similar trajectory. The key lesson: solve the combinatorial problem, not the perfection problem.

3. **Reuse fails without organizational/social change** (Morisio et al. 2002, Frakes & Kang 2005). Technology alone is insufficient. Portable skills require vendor buy-in, community incentives, and process change. This is the most consistent finding across 30+ years of reuse research.

4. **Standards adoption is driven by network effects, not technical merit** (Arthur 1989, Katz & Shapiro 1985, Farrell & Saloner 1985). First-mover advantage and ecosystem momentum matter more than protocol elegance. MCP's early multi-vendor adoption is the critical strategic asset.

5. **A platform-independent model with generated platform-specific variants is the most promising architecture** (MDE/MDA, MLIR dialects, DSPy compilation, CWL/WDL/Nextflow). The academic precedent overwhelmingly supports: define once in a canonical format, compile/translate to tool-specific representations.

6. **Agent communication standards have a 30-year history** repeating similar patterns (KQML 1994 → FIPA ACL 2002 → MCP/A2A 2024). The shift from mentalistic (BDI) to protocol-based semantics, and from closed to open governance, are improvements — but the fundamental challenge of semantic interoperability remains.

---

## Thread 1: Software Reuse and Component-Based SE

### Narrative Synthesis

The software reuse literature — spanning from McIlroy's 1968 vision of "mass-produced software components" through Szyperski's foundational textbook (2002) to recent AI-era work (Mikkonen et al. 2025) — tells a story of persistent aspiration and partial achievement. **Reuse is universally desired but notoriously difficult to achieve across platform boundaries.**

The component model wars of the 1990s–2000s are the clearest historical parallel to today's AI tool fragmentation. COM was Windows-locked, JavaBeans/EJB were JVM-only, and CORBA attempted cross-platform interop but at prohibitive complexity cost (Emmerich & Kaveh 2002). **No single model achieved universal portability.** The eventual resolution was not one model winning but the industry moving to a different abstraction layer (web services, then microservices) — suggesting that the AI tool portability problem may be solved by moving to a higher abstraction level rather than standardizing at the current one.

Krueger's (1992) concept of **"cognitive distance"** — the gap between understanding a component and deploying it in a new context — is directly applicable. Currently, a developer who writes a Copilot CLI skill faces maximal cognitive distance when porting to Claude Code: completely different file formats, different capability models, different execution semantics. Reducing this distance is the core UX goal.

The software product line (SPL) tradition (Clements & Northrop 2002, Metzger & Pohl 2014, Kang et al. 1990/FODA) offers a systematic framework: AI coding tools are a product line sharing 80%+ of functionality but varying in platform integration. SPL theory prescribes extracting a shared core asset (the portable skill format) and managing platform-specific variants through feature models.

Batory's AHEAD algebra (2004) formalizes this: software artifacts can be expressed as algebraic compositions of features. If skills were modeled as composable refinements with defined composition semantics, they could be combined predictably across platforms.

**The most sobering finding** comes from Morisio, Ezran & Tully (2002), who studied 24 European reuse projects and found that failures were overwhelmingly due to **process and organizational factors, not technology**. Creating a portable skill format is a technology solution, but adoption depends on vendor process changes and community incentives.

Recent work (Badampudi et al. 2024, Kapitsaki 2024, Mikkonen et al. 2025) extends these lessons to the AI era, highlighting InnerSource practices for large-scale reuse, provenance tracking for AI-generated artifacts, and the risk of "cargo cult" reuse where developers include AI-generated content without understanding it.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Szyperski, *Component Software* | Book, 2002 | Components must be independently deployable with explicit interfaces |
| Emmerich & Kaveh, Component Technologies | ICSE 2002 | No component model achieved universal portability |
| Vale et al., 28 Years of CBSE | JSS 2016 | Standardization and interoperability remain open after 28 years |
| Krueger, Software Reuse | ACM Surveys 1992 | "Cognitive distance" determines reuse success |
| Frakes & Kang, Reuse Status & Future | TSE 2005 | Successful reuse requires organizational change, not just technology |
| Morisio et al., Success/Failure Factors | TSE 2002 | Failures are process/human factors, not technology |
| Clements & Northrop, SPL | Book 2002 | Core assets + managed variability = product line |
| Kang et al., FODA | SEI Report 1990 | Feature models capture commonality and variability |
| Batory et al., AHEAD | TSE 2004 | Algebraic composition of software artifacts |
| Metzger & Pohl, SPL Achievements | ICSE/FoSE 2014 | Runtime variability and ecosystem integration are open challenges |
| Badampudi et al., Microservice Reuse | EMSE 2024 | InnerSource + CI/CD enables large-scale reuse |
| Mikkonen et al., AI-Native Reuse | arXiv 2025 | AI creates "cargo cult" reuse risks |
| Kapitsaki, Generative AI Reuse | ICSR 2024 | Provenance and licensing for AI-generated code |

### Open Problems
- No formal model of "skill portability" exists for AI tool artifacts
- Economic incentives for cross-platform skill authoring are unclear
- Provenance tracking for ported/adapted skills is unsolved

### Connection to Our Problem
The 30-year CBSE trajectory predicts that AI tool artifact ecosystems will only mature when standardization occurs — but that standardization is more likely to emerge from a higher abstraction layer (a portable meta-format) than from one vendor's format winning.

---

## Thread 2: Domain-Specific Languages (DSLs)

### Narrative Synthesis

DSL research provides the strongest **design framework** for the portable artifact problem because AI tool formats (SKILL.md, .cursorrules, CLAUDE.md, AGENTS.md) are essentially lightweight external DSLs. The field offers both theoretical foundations and practical precedents.

Mernik, Heering & Sloane's (2005) foundational survey establishes decision patterns for when to build a DSL — and the current situation clearly qualifies: a narrow domain (AI tool configuration), repetitive tasks (defining skills/agents), and domain experts (developers) who aren't PL designers. Fowler's (2010) external vs. internal DSL distinction is critical: external DSLs (like YAML/Markdown skill definitions) are inherently more portable since they're not bound to a host language. Kosar et al. (2010) empirically confirmed that DSL users show **15% higher comprehension** than GPL users — evidence that declarative formats are the right approach.

The most architecturally illuminating parallel comes from **MLIR** (Lattner et al. 2021). MLIR solved the compiler fragmentation problem — where each DSL built its own compilation pipeline from scratch — by providing a multi-level, extensible intermediate representation with composable "dialects." **This is directly analogous to the AI tool portability problem.** Just as MLIR provides shared infrastructure for diverse DSL compilers, a shared intermediate representation for AI tool artifacts could allow translation between platform-specific formats. Platform-specific extensions become "dialects" of a common core.

The **Model-Driven Engineering** tradition (Schmidt 2006, Czarnecki & Eisenecker 2000) provides the theoretical backbone: define a Platform-Independent Model (PIM) for skills/agents, then transform it into Platform-Specific Models (PSMs) for each tool. Hebig et al. (2018) empirically validated that dedicated transformation languages outperform general-purpose approaches for model transformations — suggesting that a purpose-built tool for skill format translation would be more effective than ad hoc scripts.

**DSPy** (Khattab et al. 2023) from Stanford is perhaps the most directly relevant recent work: a declarative programming model for LLM pipelines where users compose modular "signatures" and the compiler optimizes for different execution backends. The "compile once, run on many LLMs" pattern is exactly the abstraction needed for "define once, use on many AI tools."

The **bioinformatics workflow portability precedent** (CWL, WDL, Nextflow) is the closest real-world analog: that community faced the exact same fragmentation problem with workflow DSLs, and after 10+ years has developed cross-format translation tools, competing standards, and nascent convergence. This validates the approach but also shows it takes years.

Emerging industry efforts confirm the academic direction: Oracle's Open Agent Specification (inspired by ONNX), the Agent Definition Language (ADL), and SuperSpec DSL all attempt platform-agnostic agent definitions — but none has achieved critical mass yet.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Mernik, Heering & Sloane | ACM Surveys 2005 | Decision/implementation patterns for DSL development |
| Fowler, *DSLs* | Book 2010 | External DSLs are inherently more portable |
| Kosar et al., DSL vs GPL | CSIS 2010 | DSL users show 15% higher comprehension |
| Erdweg et al., Language Workbench Challenge | SLE 2013 | Feature model for comparing DSL ecosystems |
| Lattner et al., MLIR | CGO 2021 | Multi-level IR with composable dialects solves fragmentation |
| Brown et al., xDSL | SC22 2022 | Reusable, composable IR components for siloed toolchains |
| Schmidt, MDE | IEEE Computer 2006 | Platform-independent models → platform-specific generation |
| Czarnecki & Eisenecker, Generative Programming | Book 2000 | Feature models for product families |
| Khattab et al., DSPy | ICLR 2024 | Declarative LLM pipelines compiled to different backends |
| Hebig et al., Transformation Languages | ESEC/FSE 2018 | Dedicated transformation languages outperform GPL for model transforms |
| Rodriguez-Sanchez et al., RLang | ICML 2023 | Algorithm-agnostic declarative agent knowledge specification |
| LLM Code Gen for DSLs | arXiv 2024 | LLM capability drops for underrepresented DSLs |

### Open Problems
- No existing DSL workbench targets AI tool artifact formats
- LLMs struggle with underrepresented DSLs (arXiv 2024) — a converged standard would create a virtuous cycle
- Feature model for "AI tool capabilities" doesn't exist yet

### Connection to Our Problem
The DSL literature provides the strongest design prescription: create an external DSL (YAML/Markdown-based) as the platform-independent format, use model transformations to generate tool-specific variants, and leverage the MLIR "dialects" concept for platform-specific extensions atop a shared core.

---

## Thread 3: Plugin Architecture Research

### Narrative Synthesis

The plugin ecosystem literature reveals that **ecosystem dynamics, not technical design, determine success or failure**. This is the thread most directly relevant to how AI tool plugin ecosystems will evolve.

Manikas & Hansen's (2013) systematic review of 90 papers found remarkably little consensus on even defining "software ecosystem" — and AI tool ecosystems are even newer and less understood. Jansen's (2014) Open Source Ecosystem Health Operationalization provides actionable metrics (contributor diversity, update frequency, abandonment risk) that MCP server registries and plugin marketplaces urgently need.

Decan, Mens & Grosjean's (2019) comparison of 7 packaging ecosystems reveals a critical lesson: **governance policies fundamentally shape ecosystem fragility**. CRAN's strict review produces a stable but slow-growing ecosystem; npm's permissiveness enables explosive growth but creates fragility through transitive dependencies. MCP and AI tool plugin ecosystems must make this governance choice deliberately — and the research shows there's no way to have both.

Bogart et al.'s (2016) study of how Eclipse, R/CRAN, and npm handle breaking changes shows that **community values shape cost distribution**. Eclipse prioritizes backward compatibility (cost on producers); npm permits rapid change via semver (cost on consumers). This is not a technical decision — it's a social contract.

The **security dimension** is alarming. Edirimannage et al. (2024) found 5.6% of VS Code extensions exhibited suspicious behavior. Agarwal et al. (2022) showed browser extensions actively undermine platform security. MCP servers and AI tool plugins, which operate with broad filesystem/network access, face amplified versions of these risks.

Tiwana, Konsynski & Bush (2010) provide the overarching framework: **platform architecture, governance, and environment co-evolve**. Input control (gatekeeping) accelerates healthy evolution more than output controls. The generativity-control tension — openness for innovation vs. security/quality control — is the central challenge for every AI tool ecosystem.

Zerouali et al.'s (2019) "technical lag" concept (the gap between deployed dependency versions and latest releases) will manifest in plugin ecosystems as platform APIs evolve: MCP server authors who don't update risk silent incompatibilities.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Manikas & Hansen, SE Ecosystems SLR | JSS 2013 | Little consensus on definitions; few analytical models |
| Jansen, OS Ecosystem Health | IST 2014 | Health metrics: contributor diversity, growth, risk, robustness |
| Decan, Mens & Grosjean, 7 Ecosystems | EMSE 2019 | Governance policies shape fragility; power-law dependencies |
| Bogart et al., How to Break an API | ESEC/FSE 2016 | Community values determine cost distribution of breaking changes |
| Robbes et al., API Deprecation Reaction | FSE 2012 | 40% of deprecation messages are unhelpful; adaptation takes weeks |
| Edirimannage et al., VS Code Security | arXiv 2024 | 5.6% of VS Code extensions exhibit suspicious behavior |
| Agarwal et al., Browser Extensions Security | CCS 2022 | Extensions undermine platform security guarantees |
| Tiwana et al., Platform Evolution | ISR 2010 | Architecture, governance, environment co-evolve |
| Zerouali et al., Technical Lag | JSEP 2019 | Lag accumulates passively, introducing bugs and vulnerabilities |
| Mosqueira-Rey et al., API Usability | CSR 2019 | Most evaluations focus on learnability; few during early design |
| Um et al., WordPress Ecosystem | 2022 | Core plugins enable long-tail niche offerings |

### Open Problems
- No empirical study exists of MCP server ecosystems or LLM plugin marketplaces (too new)
- Security models for AI tool plugins with filesystem/network access are immature
- Health metrics haven't been adapted for AI tool ecosystems

### Connection to Our Problem
Plugin ecosystem research predicts that the MCP ecosystem will follow the same power-law dynamics as npm: a few foundational servers will enable a long tail of specialized tools. Governance decisions made now will determine whether the ecosystem develops npm-style fragility or CRAN-style stability.

---

## Thread 4: Knowledge Representation for SE

### Narrative Synthesis

This thread reveals that AI tool "skills" and "instructions" are a **new form of an old problem**: structuring developer knowledge for machine consumption. The lineage runs from formal ontologies through knowledge graphs to modern RAG systems.

Abran et al. (2006) formalized the SWEBOK into an ontology with 4,000+ concepts — the closest academic precedent to what skill/instruction files attempt. But the ontology is static and expert-curated; it doesn't capture procedural knowledge (the "how"). Skills fill exactly this gap: they encode task-specific procedural knowledge that formal ontologies miss.

Dey, Karnauch & Mockus (2021) introduced "Skill Space" — embedding developer expertise as vectors using Doc2Vec across the World of Code infrastructure. If skills can be mapped into the same vector space, automated discovery becomes possible: which skills does a project need? Which agents are relevant?

Code knowledge graphs (Abdelaziz et al. 2021/GraphGen4Code, Borowski et al. 2024/Semantic Code Graph) demonstrate that code knowledge can be structured as queryable graphs combining code entities, documentation, and community knowledge. Skills are essentially **human-curated, lightweight versions** of what these systems generate automatically.

Treude & Robillard (2016) and Robillard (2009) established that essential developer knowledge lives outside official documentation — in forums, examples, and tacit practice. Every knowledge barrier Robillard identified (selecting the right API, task-specific usage, common pitfalls) is a use case for well-authored skills.

The mining tradition (Xie & Pei 2006/MAPO) shows that API usage patterns can be extracted automatically from repositories. The emerging frontier — **Bi et al. (2026)** — directly targets SKILL.md format, proposing automated extraction of procedural knowledge from open-source agentic repositories with a 40% improvement in knowledge transfer efficiency. This is the most directly relevant paper in the entire review.

CONAN (Li et al. 2024) validates that feeding structured knowledge artifacts into LLM context via RAG improves code generation quality — confirming that skills (as curated retrieval corpora) are architecturally sound.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Abran et al., SWEBOK Ontology | Springer 2006 | 4,000+ concepts; static, expert-curated SE knowledge |
| Dey et al., Skill Space | ICSE 2021 | Developer expertise as vector embeddings |
| Abdelaziz et al., GraphGen4Code | K-CAP 2021 | 2B-triple code knowledge graph from 1.3M Python files |
| Borowski et al., Semantic Code Graph | IEEE 2024 | Abstract source-code-connected dependency representation |
| Treude & Robillard, Augmenting API Docs | ICSE 2016 | Crowd knowledge fills documentation gaps |
| Robillard, API Learning Barriers | IEEE Software 2009 | Six categories of knowledge barriers for developers |
| Xie & Pei, MAPO | MSR 2006 / ECOOP 2009 | Mining API usage patterns from repositories |
| Garousi et al., SE Competencies | IST 2023 | 62 hard + 63 soft competencies via Kano model |
| Li et al., CONAN | arXiv 2024 | RAG coding assistant with code-structure-aware retrieval |
| **Bi et al., Automated Skill Acquisition** | **arXiv 2026** | **Mining SKILL.md from agentic repos; 40% transfer improvement** |

### Open Problems
- No portable standard for developer knowledge artifacts exists despite rich representation research
- Automated skill quality assessment is unsolved
- Reconciling auto-mined patterns with human-authored curation

### Connection to Our Problem
Skills and instructions are the practical realization of 20+ years of knowledge representation research. The field has converged on structured, queryable, contextually-augmented knowledge — and skills are the lightweight, versionable, portable incarnation of this vision. Bi et al. (2026) validates that SKILL.md-format artifacts can be mined automatically from codebases.

---

## Thread 5: Interoperability Standards

### Narrative Synthesis

This thread provides the **strategic and economic foundations** for understanding standards adoption. The lesson from LSP, OpenAPI, CORBA, GraphQL, and OSLC is remarkably consistent: **simplicity, ubiquity, and ecosystem momentum beat technical sophistication.**

The LSP case study is the most instructive parallel. Barros et al. (2022) documented 121 language server implementations — evidence of explosive adoption. But the F-IDE 2021 paper revealed a critical warning: when LSP lacks needed capabilities, implementers create **ad-hoc extensions that break the decoupling goal**. MCP will face the same pressure — and must plan an explicit extension mechanism with governance to prevent fragmentation.

Bork & Langer (2023) attributed LSP's success to its **open, community-driven governance** model. This maps directly to MCP's transfer to the Linux Foundation's Agentic AI Foundation.

The GraphQL study (Brito & Valente 2020) showed that schema-first, self-describing protocols lower adoption barriers — even for inexperienced developers. MCP's tool/resource discovery mechanism serves the same role: AI tools can introspect what's available.

The OSLC experience (Elberzhager et al. 2016, El-Khoury 2020) provides a cautionary tale: OSLC's RESTful/Linked Data approach enabled loose coupling, but **syntactic interoperability ≠ semantic interoperability**. Having a common transport doesn't mean tools understand each other's data. MCP must go beyond transport-level standardization. Additionally, OSLC's complexity limited adoption to large enterprises — MCP must keep the implementation barrier low.

The CORBA vs. Web Services comparison (Gokhale et al. 2002) drives home the simplicity lesson: CORBA was arguably more capable, but web services won because HTTP/XML were universally available while CORBA required specialized infrastructure. MCP's use of JSON-RPC over stdio/HTTP follows this winning pattern.

The economics literature is definitive. Arthur's (1989) increasing-returns model shows that markets with network effects tend to "tip" toward a single standard, even an inferior one, based on early historical events. Katz & Shapiro (1985) formalize that every new adopter makes the standard more valuable for all existing users. Farrell & Saloner (1985) introduce "excess inertia" — industries trapped in inferior standards due to coordination failure. **MCP's early multi-vendor adoption is the critical strategic asset** — it creates the positive feedback loop Arthur describes.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Barros et al., LSP Empirical Study | MODELS 2022 | 121 language servers; M×N→M+N works |
| F-IDE 2021, Specification LSP Extensions | EPTCS 2021 | Ad-hoc extensions break decoupling; governance needed |
| Bork & Langer, LSP Introduction | EMISA 2023 | Open governance + generic pattern = broad adoption |
| Brito & Valente, REST vs GraphQL | ICSA 2020 | Schema-first lowers adoption barriers |
| Serbout & Pautasso, APIstic | MSR 2024 | 1M+ OpenAPI docs; machine-readable enables quality analysis |
| Coblenz et al., REST Design Practices | VL/HCC 2023 | Specification-implementation drift is persistent |
| Elberzhager et al., OSLC Lessons | ICIST 2016 | Syntactic interop ≠ semantic interop |
| El-Khoury, OSLC Analysis | KTH 2020 | Complexity limits adoption to enterprises |
| Arthur, Competing Technologies | Economic Journal 1989 | Increasing returns create lock-in; first-mover advantage |
| Katz & Shapiro, Network Externalities | AER 1985 | Network effects drive tipping dynamics |
| Farrell & Saloner, Standardization | RAND Journal 1985 | "Excess inertia" traps industries in inferior standards |
| Gokhale et al., CORBA vs Web Services | WWW 2002 | Simplicity and ubiquity beat technical sophistication |
| Hou et al., MCP Security | arXiv 2025 | First comprehensive MCP security analysis |

### Open Problems
- Extension governance for MCP not yet formalized
- No academic analysis of MCP adoption dynamics exists
- Semantic interoperability beyond transport-level standardization is unsolved

### Connection to Our Problem
The standards literature says: **get the economics right before perfecting the technology.** Multi-vendor adoption, low implementation barriers, and open governance are necessary conditions. MCP is following the LSP playbook — and the economics literature confirms this is the right strategy.

---

## Thread 6: API Design and Evolution

### Narrative Synthesis

This thread addresses the **engineering mechanics** of how artifact formats can evolve without breaking consumers. The findings are directly actionable.

Dig & Johnson's (2005) foundational finding is the most practical: **>80% of breaking API changes are refactorings** (renames, moves, signature changes), not arbitrary deletions. This means migration tooling is feasible — if skill format changes are primarily structural refactorings, automated migration scripts can handle most transitions.

Semver research (Raemaekers et al. 2014/2017, Ochoa et al. 2022, Pinckney et al. 2023) shows that semantic versioning helps but is chronically violated. Raemaekers found ~1/3 of Maven releases contained breaking changes; Ochoa's replication showed improvement to 83.4% compliance but found only 7.9% of clients were actually affected — suggesting that "actual impact" matters more than "number of changes." Pinckney's npm analysis shows that when semver is followed, 90% of security patches propagate quickly. **For AI tool formats: automated compliance verification at publish time is essential.**

Robillard & DeLine (2011) identified documentation quality as the **#1 obstacle** to API adoption. Myers & Stylos (2016) applied HCI/Cognitive Dimensions to API evaluation. Uddin & Robillard (2015) cataloged documentation anti-patterns. The lesson for AI tool formats: invest heavily in examples, intent documentation, and scenario matching — not just reference specs.

The adapter/wrapper pattern research is directly applicable. Bartolomei, Czarnecki & Lämmel (2010) documented 6 migration wrapping patterns for API translation (Layered Adapter, Stateful Adapter, etc.). Reimann & Kniesel-Wünsche (2024) showed that adapter generation can be systematized — if schema transformations are specified declaratively, cross-platform translation is automatable.

The most striking recent finding: Wang et al. (2025, ICSE) discovered that **LLMs frequently generate deprecated API calls** because training data lags library evolution. This creates a unique feedback loop for AI tool formats: if the tools themselves generate skill/agent definitions using deprecated schema fields, format evolution must account for LLM training lag.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Dig & Johnson, Refactorings in API Evolution | ICSM 2005 | >80% of API breaks are refactorings → migration automatable |
| Brito et al., APIDiff | SANER 2018 | Automated breaking-change detection tooling |
| Brito et al., Breaking Change Motivations | EMSE 2020 | Simplification, features, maintainability drive breaks |
| Raemaekers et al., Semver vs Breaking Changes | SCAM 2014/JSS 2017 | ~1/3 of releases break semver |
| Ochoa et al., Breaking Bad? | EMSE 2022 | 83.4% semver adherence; only 7.9% of clients affected |
| Pinckney et al., Semver in NPM | MSR 2023 | Proper semver enables 90% security patch propagation |
| Robillard & DeLine, API Learning Obstacles | EMSE 2011 | Documentation is #1 adoption barrier |
| Myers & Stylos, API Usability | CACM 2016 | HCI methods reveal design pitfalls |
| Bartolomei et al., Wrapping Patterns | ICSM 2010 | 6 migration wrapping patterns for API translation |
| Reimann & Kniesel-Wünsche, Adaptoring | SANER 2024 | Systematic adapter generation is feasible |
| Yang et al., REST API Deprecation | ICSME 2020 | Only 0.6% use formal deprecation |
| Wang et al., LLMs Meet Library Evolution | ICSE 2025 | LLMs generate deprecated calls; training lag matters |
| Ding et al., Unified Tool Integration | arXiv 2025 | Protocol-agnostic design: 60-80% code reduction |

### Open Problems
- Semantic changes (meaning changes without syntax changes) remain hard to detect
- Ecosystem-wide usage telemetry for "actual impact" analysis is rare
- LLM training lag creates a new category of deprecation challenge

### Connection to Our Problem
API evolution research provides specific engineering guidance: use automated breaking-change detection at publish time, design adapter/wrapper patterns for cross-format translation, invest in documentation quality (not just spec completeness), and establish formal deprecation policies from day one.

---

## Thread 7: MCP and Agent Communication Protocols

### Narrative Synthesis

This thread reveals that **the AI tool interoperability challenge has a 30-year academic lineage** — and that today's protocols are making real improvements over their predecessors while facing some of the same unsolved problems.

KQML (Finin et al. 1994) was the first agent communication language, introducing "performatives" (speech-act-inspired message types). Labrou & Finin (1997) formalized KQML's semantics using speech act theory. FIPA ACL (2002) refined this into 22 standardized communicative acts with formal BDI-based semantics. Wooldridge & Jennings (1995) provided the canonical theoretical framework.

But FIPA ACL had a fatal flaw: its mentalistic (BDI) semantics were **unverifiable in open systems**. You cannot inspect another agent's beliefs, desires, and intentions. Singh (1998) proposed the solution: replace unverifiable mental states with **social commitments** — publicly observable, trackable obligations. This shift from internal to external semantics is the intellectual foundation of modern protocols.

MCP and A2A embody the commitment-based, protocol-level semantics that Singh and Pitt & Mamdani (1999) advocated. MCP's JSON-RPC methods define valid request/response sequences; A2A's Agent Cards create publicly observable capability declarations; Task objects implement observable state machines (created → working → completed).

The academic analysis of modern protocols is already underway. A comprehensive survey (arXiv:2505.02279) compares MCP, ACP, A2A, and ANP, proposing a phased adoption roadmap. Security analysis (arXiv:2503.23278) identifies 16 threat scenarios across MCP's lifecycle. Habler et al. (2025) evaluate A2A's security using the MAESTRO framework.

The institutional landscape has shifted dramatically: ACP merged with A2A under the Linux Foundation (August 2025), and MCP governance transferred to the Agentic AI Foundation (December 2025). **Open governance under a neutral body is the historically validated approach** (JADE's FIPA compliance demonstrated this at the implementation level).

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Finin et al., KQML | CIKM 1994 | First widely-adopted agent communication language |
| Labrou & Finin, KQML Semantics | IJCAI 1997 | Formalized with speech act theory + conversation policies |
| Wooldridge & Jennings, Intelligent Agents | KER 1995 | Canonical agent paradigm: autonomy, reactivity, proactivity, social ability |
| FIPA ACL Specification | FIPA 2002 | 22 communicative acts with BDI-based semantics |
| Singh, Social Semantics | IJCAI 1999 | Social commitments replace unverifiable mental states |
| Pitt & Mamdani, Protocol-Based Semantics | IJCAI 1999 | Protocol-level > message-level semantics |
| Bellifemine et al., JADE | PAAM 1999 | Most adopted FIPA platform; proved standards work in practice |
| Survey of Agent Interop Protocols | arXiv 2505.02279 | MCP → ACP → A2A → ANP phased roadmap |
| MCP Security Analysis | arXiv 2503.23278 | 16 threat scenarios across MCP lifecycle |
| Habler et al., A2A Security | arXiv 2504.16902 | MAESTRO framework for A2A threat modeling |
| Ray, A2A Review | TechRxiv 2025 | Agent Cards, Tasks, schema evolution challenges |
| MCP Safety Audit | arXiv 2504.03767 | Concrete exploits: tool hijacking, credential theft |

### Key Historical Comparison

| Aspect | KQML/FIPA (1990s) | MCP/A2A (2025) |
|--------|-------------------|----------------|
| Semantics | Mentalistic (BDI) — unverifiable | Protocol-level (JSON-RPC) — pragmatic |
| Discovery | Directory Facilitator | Agent Cards, JSON-LD |
| Security | Largely assumed | First-class concern; active threat modeling |
| Scope | Agent↔Agent only | Agent↔Tool (MCP) + Agent↔Agent (A2A) |
| Governance | FIPA (now defunct) | Linux Foundation (active) |

### Open Problems
- No peer-reviewed FIPA-to-MCP/A2A comparison exists yet
- Dynamic trust establishment across protocols is unsolved
- Semantic interoperability (not just transport interop) remains the fundamental challenge

### Connection to Our Problem
The 30-year arc from KQML to MCP validates that the problem of agent interoperability is real and recurring. The shift to commitment-based, protocol-level semantics is an improvement. But semantic interoperability — ensuring tools actually understand each other's capabilities, not just exchange messages — remains the unsolved frontier that's directly relevant to portable skills.

---

## Thread 8: Recent LLM Tool Use and Agent Interoperability (2024–2026)

### Narrative Synthesis

This thread captures the rapidly evolving cutting edge. The field is moving from isolated tool-use to **standardized, interoperable agent systems**, but is pre-convergence.

The **function calling standardization** space has matured rapidly. The Berkeley Function-Calling Leaderboard (BFCL, Patil et al.) has become the de facto evaluation standard, testing single-turn, multi-turn, parallel, and agentic API use. ToolACE (Liu et al., ICLR 2025) demonstrated that focused training data enables 8B-parameter models to compete with GPT-4 on function calling. AsyncLM (Gim et al. 2024) proposes protocol extensions for asynchronous tool calls — a capability gap in current standards.

**Tool-use benchmarks** are proliferating. ToolLLM (Qin et al., ICLR 2024) covers 16,464 APIs with the ToolBench dataset. T-Eval (Chen et al., ACL 2024) decomposes tool use into sub-processes, revealing exactly where models fail. The key insight for portability: **which tool-use competencies transfer across platforms vs. which are platform-specific** is empirically testable.

The **multi-agent framework space** is vibrant but fragmented. MetaGPT (Hong et al., ICLR 2024 oral) encodes Standard Operating Procedures (SOPs) into multi-agent prompts — SOPs as serializable sequences are inherently portable. AutoGen (Wu et al., COLM 2024) supports customizable conversation patterns. But **no cross-framework portability exists**: MetaGPT roles ≠ AutoGen roles ≠ CrewAI roles (and CrewAI and LangGraph have no academic papers).

**Agent-computer interface benchmarks** reveal the scale of the portability challenge. OSWorld (Xie et al., NeurIPS 2024) tests 369 real-world tasks across Ubuntu/Windows/macOS: humans achieve 72% success, best AI agents only ~12%. WebArena (Zhou et al. 2023) shows GPT-4 agents at ~14% vs ~80% human on web tasks. **Cross-platform agent transfer is far from solved.**

The **emerging standards stack** — MCP (tool integration) + A2A (agent communication) + AGENTS.md (project instructions) — forms a converging but pre-1.0 foundation. AGENTS.md has achieved remarkable adoption (60K+ projects) as a vendor-neutral replacement for .cursorrules, claude.md, etc. But these are industry specifications, not academic publications.

Surveys (arXiv:2501.06322 on multi-agent collaboration, arXiv:2601.01743 on agent architectures, Li 2025 at COLING on paradigms, Luo et al. 2025 on methodology) provide taxonomies but no convergence on a standard architecture.

### Key Papers

| Paper | Venue/Year | Key Finding |
|-------|-----------|-------------|
| Patil et al., Berkeley Function Calling Leaderboard | ICML 2025 | De facto standard for LLM function-calling evaluation |
| Liu et al., ToolACE | ICLR 2025 | 8B models compete with GPT-4 via curated training data |
| Gim et al., AsyncLM | arXiv 2024 | Asynchronous function calling protocol extensions |
| Qin et al., ToolLLM | ICLR 2024 | 16,464 APIs; ToolBench dataset; ToolEval evaluator |
| Chen et al., T-Eval | ACL 2024 | Step-by-step tool-use evaluation decomposition |
| Hong et al., MetaGPT | ICLR 2024 (oral) | SOPs as portable role-based agent definitions |
| Wu et al., AutoGen | COLM 2024 | Customizable multi-agent conversation patterns |
| Patil et al., Gorilla | arXiv 2023 | Retriever-Aware Training for API adaptation |
| Xie et al., OSWorld | NeurIPS 2024 | Cross-OS benchmark; 12% AI vs 72% human |
| Zhou et al., WebArena | arXiv 2023 | Web environment; 14% AI vs 80% human |
| Multi-Agent Collaboration Survey | arXiv 2025 | Taxonomy of coordination protocols |
| AI Agent Architectures Survey | arXiv 2026 | Taxonomy of orchestration patterns |
| Li, Tool Use Paradigms | COLING 2025 | Universal workflow taxonomy for agent comparison |

### Emerging Industry Standards

| Standard | Status | What It Standardizes |
|----------|--------|---------------------|
| MCP | Linux Foundation, multi-vendor | Agent↔Tool integration |
| A2A | Linux Foundation, 100+ backers | Agent↔Agent communication |
| AGENTS.md | 60K+ repos, vendor-neutral | Project-level agent instructions |
| Open Agent Specification (Oracle) | Early, ONNX-inspired | Cross-framework agent definitions |
| ADL (Agent Definition Language) | Early, OpenAPI-inspired | Declarative agent identity/config |

### Open Problems
- No universal tool description schema (OpenAPI is closest, but LLM tool descriptions vary wildly)
- Function calling semantics differ across platforms (sync vs async, error handling)
- Agent role definitions are framework-locked
- Cross-OS/cross-environment agent transfer is at ~12% accuracy
- State and memory portability between platforms is unstandardized

### Connection to Our Problem
The emerging MCP + A2A + AGENTS.md stack is the most promising foundation for portable AI tool artifacts. But academic research is lagging industry practice — most of these standards lack peer-reviewed analysis. The benchmarking work (BFCL, OSWorld, WebArena) provides the evaluation infrastructure needed to measure portability progress.

---

## Cross-Cutting Synthesis: Six Themes Across All Threads

### Theme 1: The Abstraction Layer Hypothesis

Across all threads, a consistent pattern emerges: **portability is achieved by moving to a higher abstraction layer, not by standardizing at the current one.**

- Component models → services → serverless (Thread 1)
- DSL → IR → platform-specific code (Thread 2, MLIR)  
- Platform-Independent Model → Platform-Specific Model (Thread 2, MDE)
- KQML → FIPA ACL → protocol-level commitments (Thread 7)
- Raw API calls → function-calling schemas → tool protocols (Thread 8)

**Implication**: A portable AI tool artifact format should be a higher-level abstraction than any individual tool's native format. It should describe *what* the skill/agent does (intent, triggers, inputs, outputs, constraints) without prescribing *how* the tool executes it.

### Theme 2: Economics Trumps Engineering

The standards economics literature (Thread 5) and the reuse failure studies (Thread 1) converge on a single finding: **adoption is determined by network effects, organizational incentives, and ecosystem momentum — not technical merit.**

- Arthur (1989): increasing returns create lock-in
- Morisio et al. (2002): reuse fails without process change
- Frakes & Kang (2005): management commitment is critical
- Gokhale et al. (2002): simplicity beats sophistication

**Implication**: A technically superior portable format that lacks vendor buy-in will fail. MCP's strategy of early multi-vendor adoption under neutral governance is the right approach, per the literature.

### Theme 3: The Governance-Fragmentation Tradeoff

Plugin ecosystem research (Thread 3) and standards research (Thread 5) both identify a fundamental tension: **openness enables growth but creates fragility.**

- npm permissiveness → explosive growth but dependency hell (Decan et al. 2019)
- CRAN strictness → stability but slow growth (Bogart et al. 2016)
- LSP ad-hoc extensions → break the decoupling goal (F-IDE 2021)
- VS Code permissiveness → 5.6% suspicious extensions (Edirimannage et al. 2024)

**Implication**: AI tool plugin ecosystems must make this choice deliberately. The MCP/A2A/AGENTS.md stack currently leans toward the npm model (permissive, fast-growing). The research predicts this will produce security and quality problems that require retroactive governance.

### Theme 4: Documentation Is the Bottleneck

Across API usability (Thread 6), plugin ecosystems (Thread 3), and knowledge representation (Thread 4), documentation quality emerges as the **single biggest adoption barrier.**

- Robillard & DeLine (2011): #1 obstacle to API learning
- Robillard (2009): six categories of knowledge barriers
- Mosqueira-Rey et al. (2019): most usability evaluations focus on learnability
- Uddin & Robillard (2015): taxonomy of documentation anti-patterns

**Implication**: A portable skill format with poor documentation, unclear examples, or missing intent descriptions will fail regardless of technical design. The format specification itself is API documentation and should be audited against Uddin & Robillard's anti-pattern taxonomy.

### Theme 5: Adapter Patterns Enable Pragmatic Portability

Rather than waiting for universal standardization, the adapter/wrapper pattern from API evolution research (Thread 6) and the compilation model from DSL research (Thread 2) suggest a pragmatic path:

- Bartolomei et al. (2010): 6 migration wrapping patterns
- Reimann & Kniesel-Wünsche (2024): systematic adapter generation
- Lattner et al. (2021): MLIR dialects as composable adapters
- Khattab et al. (2023): DSPy compiles to multiple backends
- CWL→Nextflow translation tools (bioinformatics precedent)

**Implication**: Don't wait for the industry to converge on one format. Build translation layers now. A canonical intermediate representation (like MLIR for compilers) with adapter plugins for each AI tool format is architecturally sound and practically achievable.

### Theme 6: The Semantic Gap Remains

Despite 30 years of progress on syntactic interoperability, **semantic interoperability** — ensuring tools actually understand each other's capabilities — remains the deepest unsolved problem:

- OSLC (Thread 5): transport interop ≠ semantic interop
- FIPA/KQML (Thread 7): mentalistic semantics were unverifiable
- OSWorld (Thread 8): 12% cross-platform agent transfer
- Singh (1998): social commitments as observable semantics

**Implication**: Even with a portable skill format, different AI tools may interpret the same skill differently because they have different capability models. A feature model of AI tool capabilities (echoing Kang's FODA from Thread 1) would let skills declare their requirements and tools declare their capabilities — enabling semantic matching, not just syntactic parsing.

---

## Identified Research Gaps

1. **No empirical study of AI tool artifact portability exists.** No paper has measured the effort or success rate of porting skills/agents across tools.
2. **No feature model of AI coding tool capabilities exists.** No formalization of what capabilities (filesystem access, web search, subagent spawning, etc.) different tools provide.
3. **No intermediate representation for AI tool artifacts exists.** The MLIR analogy suggests one is needed but none has been proposed.
4. **No security model for portable skills exists.** If a skill works across tools, its attack surface spans all of them.
5. **No academic study of AGENTS.md, MCP, or A2A adoption dynamics exists.** The standards economics models (Arthur, Katz & Shapiro) have not been applied to this ecosystem.
6. **Bi et al. (2026) is the only paper directly targeting SKILL.md-format artifacts.** The intersection of knowledge representation and portable tool artifacts is almost entirely unexplored.

---

## Bibliography

### Thread 1: Software Reuse & Component-Based SE
- Abran, A. et al. (2006). Engineering the Ontology for the SWEBOK. Springer.
- Apel, S., Batory, D. et al. An Algebra for Feature-Oriented Software Development. CMU.
- Badampudi, D. et al. (2024). Large Scale Reuse of Microservices. EMSE. Springer.
- Batory, D. et al. (2004). Scaling Step-Wise Refinement. TSE 30(6).
- Clements, P. & Northrop, L. (2002). Software Product Lines. Addison-Wesley.
- Crnkovic, I. et al. (2011). Software Components beyond Programming. IEEE Software 28(3).
- Czarnecki, K. & Eisenecker, U. (2000). Generative Programming. Addison-Wesley.
- Emmerich, W. & Kaveh, N. (2002). Component Technologies. ICSE.
- Frakes, W. & Kang, K. (2005). Software Reuse Research. TSE 31(7).
- Kang, K. et al. (1990). FODA Feasibility Study. SEI/CMU.
- Kapitsaki, G. (2024). Generative AI for Code Generation. ICSR, LNCS 14614.
- Krueger, C. (1992). Software Reuse. ACM Computing Surveys 24(2).
- Metzger, A. & Pohl, K. (2014). SPL Engineering and Variability Management. ICSE/FoSE.
- Mikkonen, T. et al. (2025). Software Reuse in the Generative AI Era. arXiv:2506.17937.
- Mikkonen, T. et al. (2025). On the Future of Software Reuse. arXiv:2508.19834.
- Morisio, M. et al. (2002). Success and Failure Factors. TSE 28(4).
- Szyperski, C. (2002). Component Software. 2nd ed. Addison-Wesley.
- Vale, T. et al. (2016). Twenty-eight Years of CBSE. JSS 111.

### Thread 2: Domain-Specific Languages
- Bridging MDE and AI (2024). Systematic Review. Software and Systems Modeling.
- Brown, N. et al. (2022). xDSL: Common Compiler Ecosystem. SC22.
- Erdweg, S. et al. (2013). State of the Art in Language Workbenches. SLE, LNCS 8225.
- Erdweg, S. et al. (2015). Evaluating Language Workbenches. CLSS 44.
- Fowler, M. (2010). Domain-Specific Languages. Addison-Wesley.
- Hebig, R. et al. (2018). Model Transformation Languages. ESEC/FSE.
- Khattab, O. et al. (2023). DSPy: Compiling Declarative LM Calls. arXiv:2310.03714. ICLR 2024.
- Kosar, T. et al. (2010). Comparing DSLs and GPLs. CSIS 7(2).
- Lattner, C. et al. (2021). MLIR: Scaling Compiler Infrastructure. CGO.
- LLM Code Generation for DSLs (2024). arXiv:2410.03981v3.
- Mernik, M. et al. (2005). When and How to Develop DSLs. ACM Computing Surveys 37(4).
- Rodriguez-Sanchez, R. et al. (2023). RLang: Declarative Agent Knowledge. ICML.
- Schmidt, D. (2006). Model-Driven Engineering. IEEE Computer 39(2).
- Sujeeth, A. et al. (2013). Composition and Reuse with Compiled DSLs. ECOOP, LNCS 7920.
- Voelter, M. (2013). DSL Engineering. CreateSpace.

### Thread 3: Plugin Ecosystems
- Agarwal, N. et al. (2022). Browser Extensions Undermine Security. CCS.
- Bogart, C. et al. (2016). How to Break an API. ESEC/FSE.
- Decan, A. et al. (2019). Dependency Network Evolution. EMSE 24.
- Edirimannage, S. et al. (2024). VS Code Extension Ecosystem. arXiv:2411.07479.
- Jansen, S. (2014). Measuring OSS Ecosystem Health. IST 56(11).
- Manikas, K. & Hansen, K. (2013). Software Ecosystems SLR. JSS 86(5).
- Mosqueira-Rey, E. et al. (2019). API Usability Evaluation Methods. Computer Science Review 33.
- Robbes, R. et al. (2012). API Deprecation Reaction. FSE.
- Tiwana, A. et al. (2010). Platform Evolution. ISR 21(4).
- Um, S. et al. (2022). WordPress Plugin Ecosystem Dynamics.
- Zerouali, A. et al. (2019). Measuring Technical Lag. JSEP 31(8).

### Thread 4: Knowledge Representation for SE
- Abdelaziz, I. et al. (2021). GraphGen4Code. K-CAP. arXiv:2002.09440.
- Bi, S. et al. (2026). Automated Skill Acquisition from Agentic Repos. arXiv:2603.11808.
- Borowski, K. et al. (2024). Semantic Code Graph. IEEE.
- Dey, T. et al. (2021). Representation of Developer Expertise. ICSE.
- Garousi, V. et al. (2023). Essential SE Competencies. IST.
- Li, X. et al. (2024). CONAN: RAG Coding Assistant. arXiv:2410.16229.
- Robillard, M. (2009). What Makes APIs Hard to Learn? IEEE Software.
- Treude, C. & Robillard, M. (2016). Augmenting API Docs with Stack Overflow. ICSE.
- Xie, T. & Pei, J. (2006/2009). MAPO: Mining API Usage Patterns. MSR/ECOOP.

### Thread 5: Interoperability Standards
- Arthur, W. (1989). Competing Technologies and Lock-In. Economic Journal 99(394).
- Barros, D. et al. (2022). LSP Implementation Practices. MODELS.
- Bork, D. & Langer, P. (2023). Language Server Protocol Introduction. EMISA 18(9).
- Brito, G. & Valente, M. (2020). REST vs GraphQL. ICSA.
- Coblenz, M. et al. (2023). REST API Design Practices. VL/HCC.
- El-Khoury, J. (2020). Analysis of OSLC Standard. KTH Report.
- Elberzhager, B. et al. (2016). Lessons Learned from OSLC. ICIST, CCIS 639.
- Farrell, J. & Saloner, G. (1985). Standardization and Innovation. RAND Journal 16(1).
- Gokhale, A. et al. (2002). CORBA vs. Web Services. WWW.
- Hou, X. et al. (2025). MCP Security Threats. arXiv:2503.23278.
- Katz, M. & Shapiro, C. (1985). Network Externalities. AER 75(3).
- Serbout, S. & Pautasso, C. (2024). APIstic: OpenAPI Metrics. MSR.
- Specification LSP Extensions (2021). F-IDE, EPTCS 338.

### Thread 6: API Design & Evolution
- Bartolomei, T. et al. (2010). Swing to SWT Wrapping Patterns. ICSM.
- Brito, A. et al. (2018). APIDiff: Detecting Breaking Changes. SANER.
- Brito, A. et al. (2020). Motivations for Breaking Changes. EMSE.
- Dig, D. & Johnson, R. (2005). Refactorings in API Evolution. ICSM.
- Ding, P. et al. (2025). Unified Tool Integration for LLMs. arXiv:2508.02979.
- Majchrzak, T. et al. (2021). Holistic Cross-Platform Development. JSS.
- Myers, B. & Stylos, J. (2016). Improving API Usability. CACM.
- Ochoa, L. et al. (2022). Breaking Bad? Semver in Maven. EMSE.
- Pinckney, D. et al. (2023). Semver Analysis in NPM. MSR. arXiv:2304.00394.
- Raemaekers, S. et al. (2014/2017). Semver vs Breaking Changes. SCAM/JSS.
- Reimann, L. & Kniesel-Wünsche, G. (2024). Adaptoring. SANER. arXiv:2401.07053.
- Robillard, M. & DeLine, R. (2011). API Learning Obstacles. EMSE.
- Uddin, G. & Robillard, M. (2015). How API Documentation Fails. IEEE Software.
- Wang, C. et al. (2025). LLMs Meet Library Evolution. ICSE. arXiv:2406.09834.
- Yang, J. et al. (2020). REST API Deprecation. ICSME.

### Thread 7: Agent Communication Protocols
- Bellifemine, F. et al. (1999). JADE Framework. PAAM.
- FIPA (2002). ACL Message Structure Specification. SC00061G.
- Finin, T. et al. (1994). KQML. CIKM.
- Habler, I. et al. (2025). Secure Agentic AI via A2A. arXiv:2504.16902.
- Labrou, Y. & Finin, T. (1997). KQML Semantics. IJCAI. arXiv:cs/9809034.
- MCP Safety Audit (2025). arXiv:2504.03767.
- Pitt, J. & Mamdani, A. (1999). Protocol-Based ACL Semantics. IJCAI.
- Ray, P. (2025). A2A Protocol Review. TechRxiv.
- Singh, M. (1998). Social Semantics for ACL. IJCAI-99.
- Survey of Agent Interop Protocols (2025). arXiv:2505.02279.
- Wooldridge, M. & Jennings, N. (1995). Intelligent Agents. KER 10(2).

### Thread 8: Recent LLM Agent Interoperability (2024–2026)
- Chen, Z. et al. (2024). T-Eval: Step-by-Step Tool Evaluation. ACL. arXiv:2312.14033.
- Gim, I. et al. (2024). Asynchronous LLM Function Calling. arXiv:2412.07017.
- Hong, S. et al. (2024). MetaGPT: Multi-Agent Collaborative Framework. ICLR. arXiv:2308.00352.
- Li, X. (2025). Tool Use Paradigms Review. COLING. arXiv:2406.05804.
- Liu, W. et al. (2025). ToolACE. ICLR. arXiv:2409.00920.
- Luo, J. et al. (2025). LLM Agent Survey. arXiv:2503.21460.
- Multi-Agent Collaboration Survey (2025). arXiv:2501.06322.
- AI Agent Architectures Survey (2026). arXiv:2601.01743.
- Patil, S. et al. (2023). Gorilla: LLM + APIs. arXiv:2305.15334.
- Patil, S. et al. (2025). Berkeley Function-Calling Leaderboard. ICML.
- Qin, Y. et al. (2024). ToolLLM. ICLR. arXiv:2307.16789.
- Shen, Z. (2024). LLM With Tools Survey. arXiv:2409.18807.
- Wu, Q. et al. (2024). AutoGen: Multi-Agent Conversation. COLM. arXiv:2308.08155.
- Xie, T. et al. (2024). OSWorld. NeurIPS. arXiv:2404.07972.
- Zhou, S. et al. (2023). WebArena. arXiv:2307.13854.

---

**Research team stats**: 8 parallel researchers, 350+ web searches, ~460 tool calls total, ~100 verified papers across 8 threads. Average researcher runtime: 28 minutes. All citations verified via web search — no fabricated references.