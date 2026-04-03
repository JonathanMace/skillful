# Supply Chain Security for AI Agent Plugin Ecosystems: A Literature Review

> **Compiled:** July 2025
> **Scope:** Academic literature (2018–2025) across software supply chain security, plugin/extension security, prompt injection, sandboxing, trust models, LLM agent safety, and emerging AI-specific threats.

---

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Thread 1: Software Supply Chain Security](#2-thread-1-software-supply-chain-security)
3. [Thread 2: Plugin and Extension Security](#3-thread-2-plugin-and-extension-security)
4. [Thread 3: Prompt Injection and Indirect Prompt Injection](#4-thread-3-prompt-injection-and-indirect-prompt-injection)
5. [Thread 4: Sandboxing and Isolation](#5-thread-4-sandboxing-and-isolation)
6. [Thread 5: Trust and Reputation in Open Source](#6-thread-5-trust-and-reputation-in-open-source)
7. [Thread 6: LLM Agent Safety and Alignment](#7-thread-6-llm-agent-safety-and-alignment)
8. [Thread 7: Recent Work (2024–2025) on Emerging AI-Specific Threats](#8-thread-7-recent-work-20242025-on-emerging-ai-specific-threats)
9. [Synthesis: The Converging Threat Landscape](#9-synthesis-the-converging-threat-landscape)
10. [Critical Research Gaps](#10-critical-research-gaps)
11. [References](#11-references)

---

## 1. Introduction and Motivation

AI coding tools — GitHub Copilot CLI, Claude Code, Cursor, Windsurf, and others — now support plugin and extension ecosystems. These plugins execute code with broad filesystem and network access, receive developer context via protocols like MCP (Model Context Protocol), and can influence AI-generated code through configuration files (`.copilot-instructions.md`, `.agent.md`, `.cursorrules`). As of mid-2025:

- **No sandboxing** isolates plugin code from the host environment.
- **No code signing** guarantees plugin provenance.
- **No formal security audit** gates plugin installation.
- **Rules-file injection** allows malicious actors to embed adversarial instructions in configuration files via contributed pull requests.
- **Remote MCP servers** receive developer context and can return tool-poisoned responses.

This document surveys the academic literature bearing on these threats, organized into seven research threads that collectively frame the security challenges of AI agent plugin ecosystems.

---

## 2. Thread 1: Software Supply Chain Security

### Overview

Software supply chain attacks exploit trust relationships in package ecosystems (npm, PyPI, RubyGems, crates.io) where developers routinely install third-party code with minimal scrutiny. The academic literature has matured from incident case studies to comprehensive taxonomies and automated detection systems. The core insight: modern software is assembled, not written, and each dependency is an attack surface.

The relevance to AI plugin ecosystems is direct — plugins are packages with fewer safeguards than npm or PyPI provide. They execute in privileged contexts (developer machines with source code, credentials, and network access), making them higher-value targets than typical library dependencies.

### Key Papers

**Zimmermann, M., Staicu, C.-A., Tenny, C., and Pradel, M.** "Small World with High Risks: A Study of Security Threats in the npm Ecosystem." *28th USENIX Security Symposium*, 2019.
- First large-scale empirical study of npm's dependency graph as an attack surface. Showed that a handful of maintainer accounts could inject malicious code into the majority of all npm packages. Demonstrated that the ecosystem operates as a "small world" network where compromise propagates rapidly through dense dependency chains. The left-pad and eslint-scope incidents validated these systemic risks. ([PDF](https://www.usenix.org/system/files/sec19-zimmermann.pdf))

**Ohm, M., Plate, H., Sykosch, A., and Meier, M.** "Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks." *DIMVA*, 2020.
- Manually collected and analyzed 174 real-world malicious packages from npm, PyPI, and RubyGems (2015–2019). Developed a detailed taxonomy using two attack trees: injection points (how malicious code enters packages) and execution vectors (when payloads trigger). Case studies include event-stream and NotPetya. The accompanying dataset remains a community resource. ([arXiv](https://arxiv.org/abs/2005.09535))

**Ladisa, P., Plate, H., Martinez, M., and Barais, O.** "SoK: Taxonomy of Attacks on Open-Source Software Supply Chains." *IEEE S&P*, 2023.
- The most comprehensive taxonomy to date: technology-agnostic attack tree covering the full OSS development lifecycle. Identifies attack vectors from source commit through build, packaging, and distribution. Accompanied by the open-source "Risk Explorer for Software Supply Chains" visualization tool. The taxonomy has become a standard reference. ([IEEE](https://ieeexplore.ieee.org/document/10179304), [Risk Explorer](https://sap.github.io/risk-explorer-for-software-supply-chains/))

**Birsan, A.** "Dependency Confusion: How I Hacked Into Apple, Microsoft and Dozens of Other Companies." 2021.
- Demonstrated that package managers' default resolution logic (preferring higher-version public packages over private ones) allows attackers to hijack internal dependencies. Successfully executed code inside Apple, Microsoft, PayPal, Tesla, and Uber by publishing same-named packages to public registries. Earned >$130K in bug bounties. While a practitioner disclosure rather than a peer-reviewed paper, it catalyzed extensive academic follow-up. ([Blog](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610))

**Neupane, S., et al.** "Beyond Typosquatting: An In-depth Look at Package Confusion." *USENIX Security*, 2023.
- Identified 13 distinct confusion mechanisms beyond simple typosquatting. Validated detection techniques against all npm packages, showing that prior work missed most confusion vectors. Rigorous definition of "package confusion" as a category. ([PDF](https://www.usenix.org/system/files/usenixsecurity23-neupane.pdf))

**Torres-Arias, S., Afzali, H., Kuppusamy, T.K., Curtmola, R., and Cappos, J.** "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security*, 2019.
- Cryptographic framework that captures and links metadata about each step of the software supply chain. Demonstrated it could have prevented the majority of 30 high-profile supply chain attacks. Now used in production (CNCF graduated project). ([PDF](https://www.usenix.org/system/files/sec19-torres-arias.pdf))

**Google / OpenSSF.** "SLSA: Supply-chain Levels for Software Artifacts." 2021–present.
- Four-level framework defining increasingly strict controls over source, build, and distribution. Level 4 requires hermetic builds and two-person review. SLSA's "provenance" concept (authenticated metadata documenting artifact origins) is foundational. Academic evaluation (arXiv 2409.05014, 2024) found adoption challenges at higher levels. ([slsa.dev](https://slsa.dev/), [arXiv](https://arxiv.org/abs/2409.05014))

### Open Problems
- Detection of zero-day malicious packages before any download occurs
- Scaling provenance verification to developer workflows without friction
- Dependency confusion in non-registry contexts (e.g., plugin discovery by name)

### Connection to AI Plugin Security
Plugin ecosystems replicate the npm/PyPI attack surface with fewer defenses. Typosquatting, dependency confusion, and maintainer compromise all apply. The absence of provenance (SLSA) or integrity frameworks (in-toto) for plugins means there is no way to verify that a plugin was built from its claimed source code.

---

## 3. Thread 2: Plugin and Extension Security

### Overview

Browser extensions and IDE extensions provide the closest analogy to AI agent plugins: user-installed code that runs with elevated privileges inside a trusted application. Two decades of browser extension security research have revealed persistent problems with over-permissioning, insufficient vetting, and malicious updates — problems now repeating in AI tool ecosystems.

### Key Papers

**Xie, Q., et al.** "Arcanum: Detecting and Evaluating the Privacy Risks of Browser Extensions on Web Pages and Web Content." *USENIX Security*, 2024.
- Dynamic taint tracking analysis of every functional Chrome extension in the Web Store. Found thousands of extensions (some with tens of millions of users) automatically extracting and exfiltrating user content from sensitive websites (Gmail, PayPal, Facebook). Demonstrates that static review is insufficient for privacy protection. ([PDF](https://www.usenix.org/system/files/usenixsecurity24-xie-qinge.pdf))

**Pantelaios, S., Nikiforakis, N., and Kapravelos, A.** "You've Changed: Detecting Malicious Browser Extensions through their Update Deltas." *ACM CCS*, 2020.
- Analyzed 922,000+ extension versions to detect malicious behavior introduced through updates. Two-stage system identifies "update deltas" that flip benign extensions malicious. Found clusters of extensions performing ad injection, history stealing, and user action hijacking that evaded Chrome's automated checks. ([PDF](https://kapravelos.com/publications/extensiondeltas-CCS20.pdf))

**ElBadawi, Y., et al.** "UntrustIDE: Exploiting Weaknesses in VS Code Extensions." *NDSS*, 2024.
- Comprehensive security assessment of 25,402 VS Code extensions. Found 21 extensions with proof-of-concept exploits enabling code injection, affecting >6 million installations. Key finding: VS Code extensions have no sandboxing — they run with full file and network access in the host process. Unsanitized inputs lead to arbitrary code execution. ([PDF](https://www.ndss-symposium.org/wp-content/uploads/2024-73-paper.pdf))

**Li, W., et al.** "Protect Your Secrets: Understanding and Measuring Data Exposure in VSCode Extensions." *arXiv*, 2024.
- Automated analysis of 27,261 VS Code extensions found ~8.5% could expose credentials (passwords, API keys, tokens) through extension commands, user input, or configuration vectors. ([arXiv](https://arxiv.org/abs/2412.00707))

**Luo, M., et al.** "A Study on Malicious Browser Extensions in 2025." *arXiv*, 2025.
- Demonstrated that researchers could bypass security mechanisms of both Chrome Web Store and Mozilla Add-ons Store to publish malicious extensions. Highlights persistent shortcomings in vetting processes despite years of investment. ([arXiv](https://arxiv.org/html/2503.04292v2))

### Open Problems
- Static analysis cannot catch all malicious behavior; dynamic analysis at scale is expensive
- Permission models are too coarse-grained (all-or-nothing filesystem/network access)
- Post-installation behavioral drift (benign extension becomes malicious through updates)

### Connection to AI Plugin Security
AI agent plugins face the same problems as VS Code extensions — no sandboxing, full host access, and an open publication model — but with the additional risk that plugins can manipulate AI behavior, not just the host application. The UntrustIDE findings directly preview the attack surface of AI tool plugins.

---

## 4. Thread 3: Prompt Injection and Indirect Prompt Injection

### Overview

Prompt injection is the defining security vulnerability of LLM-integrated applications. Unlike SQL injection, where parameterized queries provide a clean defense, prompt injection exploits the fundamental inability of LLMs to reliably distinguish instructions from data. Indirect prompt injection — where adversarial instructions are embedded in content the LLM processes (emails, web pages, configuration files) — is particularly relevant to plugin ecosystems, where plugins provide untrusted content to the agent.

### Key Papers

**Perez, F. and Ribeiro, I.** "Ignore Previous Prompt: Attack Techniques For Language Models." *NeurIPS ML Safety Workshop*, 2022.
- First formal study of direct prompt injection attacks. Introduced the PromptInject framework demonstrating that simple hand-crafted prompts ("Ignore previous instructions and…") can reliably hijack LLM outputs. Formalized "goal hijacking" and "prompt leaking" as attack categories. ([arXiv](https://arxiv.org/abs/2211.09527))

**Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., and Fritz, M.** "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." *AISec (ACM CCS Workshop)*, 2023.
- Foundational paper on indirect prompt injection. Demonstrated practical attacks against Bing Chat (GPT-4) and code completion tools. Key insight: LLM applications that consume external data (emails, web pages, documents, tool outputs) are inherently vulnerable because the model cannot reliably distinguish system instructions from injected content. Showed attacks including data exfiltration, API misuse, and arbitrary behavior modification. ([arXiv](https://arxiv.org/abs/2302.12173))

**Chen, S., Piet, J., Sitawarin, C., and Wagner, D.** "StruQ: Defending Against Prompt Injection with Structured Queries." *USENIX Security*, 2025.
- State-of-the-art defense: splits LLM input into separate prompt (trusted) and data (untrusted) channels using special delimiter tokens. A fine-tuned LLM is trained to follow instructions only from the prompt channel. Reduces attack success rates to near 0% with minimal utility loss. Addresses the root cause: lack of input/data separation. ([arXiv](https://arxiv.org/abs/2402.06363), [PDF](https://www.usenix.org/system/files/usenixsecurity25-chen-sizhe.pdf))

**Zhan, Q., Liang, Z., Ying, Z., and Kang, D.** "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents." *ACL Findings*, 2024.
- Benchmark of 1,054 test cases across 17 user tools and 62 attacker tools. Even GPT-4 with ReAct prompting was compromised in 24% of cases (48% with aggressive attack prompts). Tests both data exfiltration and direct harm scenarios. Critical finding: tool-using agents are significantly more vulnerable than simple chat LLMs. ([arXiv](https://arxiv.org/abs/2403.02691))

**Chen, Y., et al.** "Can Indirect Prompt Injection Attacks Be Detected and Removed?" *ACL*, 2025.
- Explores detection and removal approaches for indirect prompt injection using segmentation and extraction methods. Found that indirect injections are significantly harder to detect than direct injections, particularly when embedded in natural-looking content. ([PDF](https://aclanthology.org/2025.acl-long.890.pdf))

### Open Problems
- No complete defense exists; StruQ requires model fine-tuning, limiting applicability to closed-source models
- Multi-turn attacks where injected instructions accumulate across conversation turns
- "Sleeper" injections that activate only under specific conditions
- Rules-file injection as a specific indirect prompt injection vector (see Thread 7)

### Connection to AI Plugin Security
Prompt injection is the primary mechanism by which malicious plugins can subvert AI agents. A plugin can embed adversarial instructions in its responses, tool descriptions, or configuration files. Indirect prompt injection through `.copilot-instructions.md` or `.agent.md` is a live, demonstrated attack vector.

---

## 5. Thread 4: Sandboxing and Isolation

### Overview

Sandboxing techniques restrict untrusted code's access to system resources. The academic literature on OS-level sandboxing, container isolation, and WebAssembly-based sandboxing provides the technical foundation for isolating AI agent plugins. WebAssembly (WASM) is particularly promising because it provides lightweight, language-agnostic sandboxing with fine-grained capability control.

### Key Papers

**Bosamiya, J., Lim, W.S., and Parno, B.** "Provably-Safe Multilingual Software Sandboxing using WebAssembly." *USENIX Security*, 2022.
- Formal mathematical proof of WASM sandbox safety. Demonstrates safe Rust embeddings of WASM semantics that provide provable isolation. Performance is competitive with unsafe alternatives. Key insight: WASM guarantees are only as strong as the runtime and compiler implementation. ([USENIX](https://www.usenix.org/conference/usenixsecurity22/presentation/bosamiya))

**Johnson, E., et al.** "WaVe: A Verifiably Secure WebAssembly Sandboxing Runtime." *IEEE S&P*, 2023.
- Formally verified WASM runtime ensuring both memory safety and host resource isolation. Proves that sandboxed code cannot break out, even to OS-level resources like file systems and networks. Removes the runtime from the trusted computing base. Performance-competitive with production runtimes. ([IEEE](https://ieeexplore.ieee.org/document/10179357))

**Abbadini, M., et al.** "Leveraging eBPF to Enhance Sandboxing of WebAssembly Runtimes." *ACM AsiaCCS*, 2023.
- Uses eBPF to enforce per-module filesystem access control for WASM plugins interacting with the host via WASI. Addresses WASI's default access controls being too coarse, proposing fine-grained capability enforcement per module. ([ACM DL](https://dl.acm.org/doi/fullHtml/10.1145/3579856.3592831))

**Perrone, G. and Romano, S.P.** "WebAssembly and Security: A Review." *arXiv*, 2024.
- Comprehensive survey of 121 papers on WASM security. Discusses strengths and weaknesses of WASM sandboxing, noting that memory-unsafe languages compiled to WASM may still harbor vulnerabilities despite sandbox isolation. Classifies threats and identifies areas needing improvement. ([arXiv](https://arxiv.org/abs/2407.12297))

### Open Problems
- WASM sandboxing doesn't cover all plugin needs (e.g., network access policies, credential scoping)
- Performance overhead for IO-heavy plugins that need frequent host interactions
- Capability-based security models need standardization for plugin contexts
- No existing WASM runtime designed specifically for AI agent plugin isolation

### Connection to AI Plugin Security
WASM sandboxing is the most viable path to plugin isolation for AI tools. A plugin could run in a WASM sandbox with WASI capabilities restricted to only the files, network endpoints, and system calls it needs. The verified runtimes (WaVe) provide the security guarantees needed. Current AI tools (Copilot CLI, Claude Code) run plugins as unsandboxed native processes — the gap between the state of the art and the state of practice is vast.

---

## 6. Thread 5: Trust and Reputation in Open Source

### Overview

When plugins can't be fully sandboxed, trust becomes the gating mechanism. The academic literature on open-source trust and reputation provides models for assessing whether a package (or plugin) should be trusted based on its maintainers, development practices, and community signals. The event-stream incident (2018) remains the canonical case study of trust exploitation.

### Key Papers

**Zahan, N., Zimmermann, T., Khatchadourian, R., and Nadi, S.** "OpenSSF Scorecard: On the Path Toward Ecosystem-wide Automated Security Metrics." *arXiv*, 2022.
- Empirical evaluation of OpenSSF Scorecard across npm and PyPI. Found that scorecard metrics (18+ security heuristics including code review practices, maintainer activity, branch protection) correlate with security outcomes. Identified gaps: automated tools cannot reliably measure maintainer trustworthiness or capture nuanced dimensions of project health beyond technical metrics. ([arXiv](https://arxiv.org/pdf/2208.03412))

**Garrett, K., et al.** "A Systematic Analysis of the Event-Stream Incident." *EuroSec*, 2022.
- Deep analysis of the 2018 event-stream compromise where a social engineering attack led to maintainer takeover. The new maintainer introduced a targeted payload (via flatmap-stream) that only activated in the Copay Bitcoin wallet's build environment. The package was downloaded ~8 million times before discovery. Key lessons: volunteer maintainer fatigue creates takeover opportunities; ecosystem design lacks multi-party review for publishing rights transfer. ([Paper](https://es-incident.github.io/paper.html))

**OpenSSF / Google.** "Scorecards: Automated Security Metrics for Open Source." 2020–present.
- Automated tool scoring projects on 18+ heuristics (code review, branch protection, dependency updates, fuzzing, SAST, etc.). Aggregate scores from 0–10. Adopted by CISA. Ongoing research integrates additional signals: contributor churn, response time to vulnerabilities, governance clarity. ([scorecard.dev](https://www.scorecard.dev/))

### Open Problems
- Social trust and maintainer intent remain fundamentally unmeasurable by automated tools
- Single-maintainer concentration risk has no technical solution
- Trust transitivity through dependency graphs is poorly understood
- No reputation system exists for AI plugin authors

### Connection to AI Plugin Security
AI plugin ecosystems need trust infrastructure that doesn't yet exist. OpenSSF Scorecard provides a template but must be adapted for plugin-specific signals: Does the plugin request only necessary capabilities? Is the plugin author verified? Has the plugin been audited? The event-stream pattern (trusted maintainer hands off to attacker) is directly applicable to plugin ecosystems.

---

## 7. Thread 6: LLM Agent Safety and Alignment

### Overview

When an LLM agent has tool access (filesystem, network, code execution), the safety problem expands beyond prompt injection to encompass authorization, access control, and behavioral monitoring. The emerging literature on agent safety addresses how to prevent tool-using agents from being subverted through their inputs, tools, or memory.

### Key Papers

**Ruan, Y., Dong, H., Wang, A., Pitis, S., and Zhou, Y.** "Identifying the Risks of LM Agents with an LM-Emulated Sandbox (ToolEmu)." *ICLR*, 2024.
- LM-powered framework emulating tool execution to evaluate agent safety at scale. Tested 36 toolkits (311 tools, 144 test cases). Found even the safest LLM agents failed 23.9% of the time, with 68.8% of identified failures being valid real-world risks. Enables scalable red-teaming without requiring actual tool implementations. ([OpenReview](https://openreview.net/forum?id=GEcwtMk1uA))

**Xi, Z., et al.** "AGENTPOISON: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases." *NeurIPS*, 2024.
- Backdoor attack targeting agent memory/RAG knowledge bases. Inserts malicious instances that trigger on specific instructions. Achieves >80% attack success rate on agents in autonomous driving, healthcare, and QA settings with minimal impact on normal performance. Demonstrates that agent memory is a critical and under-protected attack surface. ([NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/file/eb113910e9c3f6242541c1652e30dfd6-Paper-Conference.pdf))

**Gu, X., et al.** "Red-Teaming LLM Multi-Agent Systems via Communication Attacks." *ACL Findings*, 2025.
- Introduces the "Agent-in-the-Middle" (AiTM) attack manipulating messages between LLM agents. Shows that inter-agent communication is a new vulnerability class distinct from single-agent prompt injection. Multi-agent systems (like plugin-using AI tools) face compounding risks when any agent/plugin can send messages to others. ([ACL](https://aclanthology.org/2025.findings-acl.349/))

**SIRAJ.** "Diverse and Efficient Red-Teaming for LLM Agents via Distilled Structured Reasoning." *arXiv*, 2025.
- Generic red-teaming framework for arbitrary black-box LLM agents. Achieves 2–2.5× improvement in risk coverage over prior approaches. Produces efficient, smaller red-teaming models. Emphasizes that tool-use capabilities fundamentally expand the agent attack surface. ([arXiv](https://arxiv.org/abs/2510.26037))

**Deng, G., et al.** "AutoRedTeamer: An Autonomous Red Teaming Agent Against Language Models." *OpenReview*, 2025.
- Fully automated LLM-based red-teaming agent achieving 20% higher attack success rate than manual approaches on HarmBench. Demonstrates that agent red-teaming can be automated and scaled. ([OpenReview](https://openreview.net/forum?id=DVmn8GyjeD))

### Open Problems
- No formal model of "agent authorization" analogous to OS-level access control
- Agent tool-use policies are defined informally in natural language, not enforced programmatically
- Multi-agent communication security is nascent
- Memory/knowledge-base poisoning has no robust defense

### Connection to AI Plugin Security
Plugins are tools that agents invoke. Every finding about tool-use agent safety applies: plugins can return poisoned outputs, manipulate agent memory, inject instructions into agent context, and exploit the gap between natural-language tool descriptions and actual tool behavior. The ToolEmu and InjecAgent benchmarks should be adapted specifically for plugin evaluation.

---

## 8. Thread 7: Recent Work (2024–2025) on Emerging AI-Specific Threats

### Overview

The most directly relevant literature has emerged in 2024–2025, addressing the specific security challenges of AI agent platforms, MCP, rules-file injection, and AI supply chain risks. This work is rapid, often appearing first on arXiv, and represents the frontier of the field.

### Key Papers

**Hou, X., et al.** "Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions." *arXiv*, 2025.
- Systematic threat taxonomy for MCP covering 16 distinct attack scenarios across creation, deployment, operation, and maintenance lifecycle phases. Catalogs threats from malicious developers, external attackers, and misconfigurations. First comprehensive academic treatment of MCP security. ([arXiv](https://arxiv.org/abs/2503.23278))

**Bao, G., et al.** "MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits." *arXiv*, 2025.
- Demonstrates concrete attack scenarios against MCP-integrated LLMs: credential theft, arbitrary code execution, context exfiltration. Introduces MCPSafetyScanner for automated security auditing of MCP servers. Found that leading LLMs could be manipulated through MCP tool interactions. ([arXiv](https://arxiv.org/abs/2504.03767))

**Chen, Z., et al.** "Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers." *arXiv*, 2025.
- Large-scale empirical assessment of public MCP servers. Identified 7–8 unique MCP-specific vulnerabilities, some entirely new (agentic tool orchestration flaws, context leakage). Shows the real-world attack surface of deployed MCP infrastructure. ([arXiv](https://arxiv.org/abs/2506.13538))

**Liang, Y., et al.** "Enterprise-Grade Security for the Model Context Protocol (MCP): Frameworks and Mitigation Strategies." *arXiv*, 2025.
- Enterprise-focused framework emphasizing threat modeling, defense-in-depth controls, zero-trust architectures, explicit resource permissions, and continuous monitoring. Actionable technical controls for production MCP deployments. ([arXiv](https://arxiv.org/abs/2504.08623))

**Wang, Z., et al.** "MindGuard: Tracking, Detecting, and Attributing MCP Tool Poisoning Attack via Decision Dependence Graph." *arXiv*, 2025.
- Focuses on Tool Poisoning Attacks (TPA) within MCP, where attackers manipulate tool metadata to induce malicious tool use. Proposes Decision Dependence Graphs for high-precision detection and attribution of such attacks, demonstrating that behavioral defenses alone are insufficient. ([arXiv](https://papers.cool/arxiv/2508.20412))

**Karliner, Z. (Pillar Security).** "Rules File Backdoor: AI Code Editors Exploited for Silent Supply Chain Attacks." *Pillar Security Technical Report*, March 2025.
- Discovers that hidden Unicode characters (zero-width joiners, bidirectional text markers) in `.cursorrules`, `CLAUDE.md`, and `.copilot-instructions.md` configuration files can inject invisible prompt instructions. AI coding agents treat these as trusted context, silently generating backdoored code. Virtually invisible in code review; propagates through repository forks — a pure supply chain attack vector. ([Pillar Security](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents))

**Maloyan, N. and Namiot, D.** "Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis." *arXiv*, January 2026.
- Comprehensive systematization of knowledge on prompt injection targeting AI coding assistants (Claude Code, Copilot, Cursor, MCP). Proposes a 3D taxonomy covering delivery vectors, attack modalities, and propagation behaviors. Catalogs 42 attack techniques and 18 defense mechanisms; finds defenses mitigate less than 50% of sophisticated attacks. ([arXiv](https://arxiv.org/abs/2601.17548))

**Marzouk, A.** "IDEsaster: A Novel Vulnerability Class in AI IDEs." *Security Research Disclosure*, December 2025 (24+ CVEs assigned).
- Discovers 30+ vulnerabilities across every tested AI-enhanced IDE (Copilot, Cursor, JetBrains, Claude Code, Gemini CLI, Zed, Roo Code). Universal attack chain: prompt injection → AI agent action → IDE feature abuse (JSON schema fetching, config overwrite) → data exfiltration or RCE. Demonstrates that IDEs were never architecturally designed for autonomous AI agents operating within them. ([MaccariTA](https://maccarita.com/posts/idesaster/))

**Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., et al.** "Defeating Prompt Injections by Design (CaMeL)." *arXiv*, 2025 (Google / Google DeepMind / ETH Zurich).
- Introduces CaMeL, a system-layer defense that separates trusted instructions from untrusted data using explicit control/data flow extraction and capability-based enforcement. Even if the underlying LLM is susceptible to prompt injection, untrusted data cannot impact control flow. Represents the most architecturally principled defense to date. ([arXiv](https://arxiv.org/abs/2503.18813))

**Zhu, K., Yang, X., Wang, J., Guo, W., and Wang, W.Y.** "MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents." *ICML*, 2025.
- Training-free defense that executes agent tasks twice (normal + masked user prompt) and compares tool calls to detect indirect prompt injection. Attack success rates drop below 1% when combined with prompt augmentation. Evaluated on AgentDojo with GPT-4o, o3-mini, and Llama-3.3-70B. ([arXiv](https://arxiv.org/abs/2502.05174))

**Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., and Xiang, Y.** "AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways." *ACM Computing Surveys*, 2025.
- Comprehensive survey categorizing AI agent threats across four knowledge gaps: unpredictable user inputs, complex agent execution, variable operational environments, and untrusted entity interactions. Highlights gaps in explainability, operational control, and resilience for deployed agent systems. ([arXiv](https://arxiv.org/abs/2406.02630))

**OWASP GenAI Security Project.** "OWASP Top 10 Risks and Mitigations for Agentic AI Security." December 2025.
- Industry-standard risk taxonomy defining 10 critical categories for agentic AI: Agent Behavior Hijacking, Identity/Privilege Abuse, Tool Misuse, Unexpected Code Execution, Insecure Inter-Agent Communication, Human-Agent Trust Exploitation, Memory/Context Poisoning, Supply Chain/Plugin Attacks, Cascading Failures, and Rogue Agents/Shadow AI. Companion to the LLM Top 10 2025. ([OWASP](https://genai.owasp.org/))

**NIST.** "AI-600-1: AI Risk Management Framework — Generative AI Profile." *NIST Special Publication*, July 2024.
- Extends the AI RMF specifically for generative AI risks. Provides a risk taxonomy for model manipulation, content misuse, and bias amplification. Establishes a governance framework (Govern/Map/Measure/Manage) aligned with Executive Order 14110 on Safe, Secure, and Trustworthy AI. ([NIST](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf))

### Open Problems
- MCP security is in its infancy — the first academic papers appeared in early 2025
- No code signing infrastructure exists for MCP servers or AI plugins
- No sandboxing standard has been proposed for AI agent tool execution
- Cross-agent communication security (multi-agent AI systems sharing tools) is unexplored
- Rules-file injection defenses are non-existent in deployed tools
- The IDEsaster findings suggest the entire IDE architecture needs rethinking for AI agents

### Connection to AI Plugin Security
MCP *is* the plugin protocol for AI coding tools — its security *is* plugin security. The papers in this section demonstrate that every layer is vulnerable: MCP servers can be poisoned (MindGuard), configuration files can carry invisible backdoors (Rules File Backdoor), IDE features can be weaponized through AI agents (IDEsaster), and comprehensive attack taxonomies now document dozens of distinct attack vectors (Maloyan & Namiot). The most promising defense approaches — CaMeL's capability-based control/data separation and MELON's dual-execution detection — offer architectural rather than patch-level solutions.

---

## 9. Synthesis: The Converging Threat Landscape

### The Recurring Pattern: Convenience Before Security

The history of software ecosystems reveals a recurring pattern: platforms prioritize developer convenience and rapid adoption, discover critical security gaps only after widespread deployment, then retrofit security mechanisms at enormous cost. Browser extensions launched with unconstrained DOM access before Chrome introduced permission isolation in 2010 (Barth et al.). npm grew to millions of packages before anyone studied the systemic risk of maintainer account compromise (Zimmermann et al., 2019). Docker containers were widely deployed before systematic studies of their escape vulnerabilities appeared (Haq et al., 2024). Deno explicitly promised "secure by default" but still has exploitable permission model weaknesses (AlHamdan & Staicu, NDSS 2025).

AI agent plugin ecosystems are repeating this pattern at an accelerated pace. Copilot CLI, Claude Code, and Cursor have launched plugin systems with no sandboxing, no code signing, no formal permission model, and no security audit process. The academic literature reviewed here demonstrates that *every* prior platform that followed this path eventually experienced serious security incidents — and the AI agent context introduces new attack dimensions that make the problem strictly harder.

### The Compound Threat Model

What makes AI agent plugin security uniquely challenging is that it combines attack surfaces from *every* prior domain:

**Supply chain attacks** (Thread 1) apply directly. Plugin ecosystems are package managers; malicious plugins can be injected through typosquatting, dependency confusion, maintainer compromise, or social engineering — exactly as documented by Ohm et al. (2020), Zimmermann et al. (2019), and Ladisa et al. (2023). The XZ Utils backdoor (Lins et al., 2024) demonstrates that even years-long social engineering campaigns are viable.

**Extension security failures** (Thread 2) are amplified. UntrustIDE (Lin et al., NDSS 2024) showed that VS Code extensions — running in the *same* IDE environment as AI coding agents — have exploitable vulnerabilities in 21 extensions with 6M+ installs. These extensions run unsandboxed with the same privileges as the IDE. AI agent plugins inherit this entire attack surface and add the ability to manipulate generated code.

**Prompt injection** (Thread 3) is the novel attack class. Unlike traditional plugins that execute code directly, AI agent plugins operate through an intermediary — the LLM. This means plugins can attack through content as well as code. A malicious plugin can embed adversarial instructions in its tool descriptions, response data, or configuration files. The Rules File Backdoor (Karliner, 2025) demonstrates this is not theoretical: hidden Unicode characters in `.copilot-instructions.md` files can inject invisible instructions that cause the AI to generate backdoored code.

**Sandbox absence** (Thread 4) means there is no containment. The academic literature shows that effective sandboxing mechanisms exist — WASM sandboxing (Bosamiya et al., 2022; Johnson et al., 2023), capability-based security (Watson et al., 2010; Miller, 2006), language-level permission models (AlHamdan & Staicu, 2025) — but *none* are deployed in any production AI agent plugin system. This is the largest gap between research capability and practice.

**Trust infrastructure absence** (Thread 5) means there is no prevention. OpenSSF Scorecard (Zahan et al., 2023) demonstrates that automated security metrics can correlate with vulnerability outcomes, but no equivalent system exists for AI plugins. The Census studies (Nagle et al., 2022, 2024) show that critical infrastructure often depends on single-maintainer packages — plugin ecosystems will inevitably reproduce this pattern.

**Agent safety failures** (Thread 6) compound everything. Even the safest LLM agents fail 23.9% of the time on high-risk tool-use scenarios (Ruan et al., 2024). Agent security benchmarks (Zhang et al., ICLR 2025) show attack success rates reaching 84.3%. Memory poisoning (Chen et al., NeurIPS 2024) achieves 80%+ success rates. The agent itself is a weak link in the chain.

### The Unique Danger: Instruction-Level Attacks

The most alarming finding from this review is that AI agent plugins face an attack class with no parallel in prior systems: **instruction-level manipulation**. Traditional software supply chain attacks compromise *code* — they inject malware, backdoors, or exploit kits that execute deterministically. AI agent plugin attacks can compromise *instructions* — they inject prompts, tool descriptions, or configuration content that manipulates the AI's *reasoning*.

This distinction matters because instruction-level attacks:
1. **Leave no executable trace.** A malicious `.copilot-instructions.md` file contains only text — no malware scanner can detect it.
2. **Are context-dependent.** The same instruction may produce different malicious outputs depending on what code the developer is working on.
3. **Exploit human trust in AI.** Developers accept AI-generated code more readily than manually written code from untrusted sources.
4. **Propagate through development workflows.** A poisoned instruction file in a repository affects every developer who clones it.

CaMeL (Debenedetti et al., 2025) represents the most principled approach to this problem — capability-based separation of control flow (trusted instructions) from data flow (untrusted content). But CaMeL is a research prototype, not a deployed system.

---

## 10. Critical Research Gaps

Based on this review, six critical gaps require urgent attention:

### Gap 1: No Sandboxing for Plugin Execution
**What exists:** WASM sandboxing (Bosamiya et al., 2022), capability models (Watson et al., 2010; Miller, 2006), Deno-style permissions (AlHamdan & Staicu, 2025). **What's missing:** Any application of these techniques to AI agent plugins. No paper proposes or evaluates a sandbox architecture for AI tool plugins.

### Gap 2: No Code Signing or Provenance for Plugins
**What exists:** Sigstore (Newman et al., 2022), in-toto (Torres-Arias et al., 2019), SLSA framework. **What's missing:** Code signing infrastructure for AI plugins. No paper addresses plugin provenance verification, cryptographic attestation of plugin integrity, or transparency logs for plugin distribution.

### Gap 3: No Permission Model for Tool Access
**What exists:** Chrome extension permissions (Barth et al., 2010), Deno permission flags, WASI capabilities. **What's missing:** A permission model for AI agent tool access. Current agents grant tools all-or-nothing filesystem and network access. No paper proposes fine-grained, user-reviewable capability grants for AI plugins.

### Gap 4: Prompt Injection Through Plugin Content Is Unsolved
**What exists:** StruQ (Chen et al., 2025), CaMeL (Debenedetti et al., 2025), MELON (Zhu et al., 2025), instruction hierarchy (Wallace et al., 2024). **What's missing:** Defenses validated against plugin-specific injection vectors. Rules-file injection, MCP tool description poisoning, and multi-plugin collusion attacks have no tested defenses. Current defenses mitigate <50% of sophisticated attacks (Maloyan & Namiot, 2026).

### Gap 5: No Trust/Reputation Framework for Plugin Authors
**What exists:** OpenSSF Scorecard (Zahan et al., 2023), Census studies (Nagle et al., 2022, 2024), developer trust models (Sapkota et al., 2019; Wermke et al., 2022). **What's missing:** Trust scoring for AI plugin authors. No paper proposes reputation metrics for plugin developers, automated vetting for plugin submissions, or trust propagation models for plugin dependency graphs.

### Gap 6: MCP Server Security Is Nascent
**What exists:** First threat taxonomies (Hou et al., 2025), safety audits (Radosevich & Halloran, 2025), empirical studies (Hasan et al., 2025). **What's missing:** Mature security frameworks. MCP authentication, authorization, rate limiting, and audit logging are underdeveloped. Tool poisoning defenses are at the proof-of-concept stage (MindGuard). No standard for MCP server security certification exists.

### A Research Agenda

The papers that *should* be written for this space include:

1. **A WASM sandbox for AI agent plugins** — adapting verified WASM runtimes (WaVe) for AI tool isolation with WASI capability restriction.
2. **An OpenSSF Scorecard for AI plugins** — defining security metrics specific to AI plugin ecosystems (capability requests, instruction content analysis, author reputation).
3. **A capability-based permission model for AI tools** — formalizing agent tool permissions using object-capability principles (Miller, 2006) with user-reviewable grants.
4. **Rules-file injection detection** — developing static analysis tools to detect hidden instructions in `.copilot-instructions.md`, `.agent.md`, and `.cursorrules` files.
5. **Plugin-specific prompt injection benchmarks** — extending AgentDojo and InjecAgent with plugin-specific attack scenarios.
6. **Empirical security analysis of AI plugin marketplaces** — a large-scale study (in the spirit of Zimmermann et al., 2019 or Kasturi et al., 2022) of deployed AI plugin ecosystems.
7. **MCP server authentication and authorization** — adapting supply chain integrity frameworks (in-toto, Sigstore) for MCP server provenance and tool attestation.

---

## 11. References

1. Abbadini, M., Facchinetti, D., Oldani, G., Rossi, M., and Paraboschi, S. "Cage4Deno: A Fine-Grained Sandbox for Deno Subprocesses." ACM ASIA CCS, 2023.
2. AlHamdan, A. and Staicu, C.-A. "Welcome to Jurassic Park: A Comprehensive Study of Security Risks in Deno and its Ecosystem." NDSS, 2025.
3. Alhindi, M. and Hallett, J. "Sandboxing Adoption in Open Source Ecosystems." SESoS/ICSE, 2024.
4. Arvanitis, I., Ntousakis, G., Ioannidis, S., and Vasilakis, N. "A Systematic Analysis of the Event-Stream Incident." EUROSEC, 2022.
5. Ayala, J., Tung, S., and Garcia, J. "A Mixed-Methods Study of Open-Source Software Maintainers on Vulnerability Management and Platform Security Features." USENIX Security, 2025.
6. Barth, A., Felt, A.P., Saxena, P., and Boodman, A. "Protecting Browsers from Extension Vulnerabilities." NDSS, 2010.
7. Bosamiya, J., Lim, W.S., and Parno, B. "Provably-Safe Multilingual Software Sandboxing using WebAssembly." USENIX Security, 2022.
8. Boughton, L., Miller, C., Acar, Y., Wermke, D., and Kästner, C. "Decomposing and Measuring Trust in Open-Source Software Supply Chains." ICSE-NIER, 2024.
9. Carlini, N., Felt, A.P., and Wagner, D. "An Evaluation of the Google Chrome Extension Security Architecture." USENIX Security, 2012.
10. Chaudhari, H., Severi, G., Abascal, J., Suri, A., Jagielski, M., Choquette-Choo, C.A., Nasr, M., Nita-Rotaru, C., and Oprea, A. "Phantom: General Trigger Attacks on Retrieval Augmented Language Generation." ICLR, 2025.
11. Chen, S., Piet, J., Sitawarin, C., and Wagner, D. "StruQ: Defending Against Prompt Injection with Structured Queries." USENIX Security, 2025.
12. Chen, Z., Xiang, Z., Xiao, C., Song, D., and Li, B. "AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases." NeurIPS, 2024.
13. Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., and Tramèr, F. "Defeating Prompt Injections by Design (CaMeL)." arXiv, 2025.
14. Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., and Tramèr, F. "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents." NeurIPS, 2024.
15. Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., and Xiang, Y. "AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways." ACM Computing Surveys, 2025.
16. Duan, R., Alrawi, O., Kasturi, R.P., Elder, R., Saltaformaggio, B., and Lee, W. "Towards Measuring Supply Chain Attacks on Package Managers for Interpreted Languages." NDSS, 2021.
17. Edirimannage, S., et al. "Developers Are Victims Too: A Comprehensive Analysis of The VS Code Extension Ecosystem." arXiv, 2024.
18. Enck, W. and Williams, L. "Top Five Challenges in Software Supply Chain Security." IEEE Security & Privacy, 2022.
19. Fourné, M., Wermke, D., Enck, W., Fahl, S., and Acar, Y. "It's like flossing your teeth: On the Importance and Challenges of Reproducible Builds for Software Supply Chain Security." IEEE S&P, 2023.
20. Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., and Fritz, M. "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." AISec (ACM CCS Workshop), 2023.
21. Haq, M.S., Nguyen, T.D., Tosun, A.S., Vollmer, F., Korkmaz, T., and Sadeghi, A.-R. "SoK: A Comprehensive Analysis and Evaluation of Docker Container Attack and Defense Mechanisms." IEEE S&P, 2024.
22. Hasan, M.M., Li, H., Fallahzadeh, E., Rajbahadur, G.K., Adams, B., and Hassan, A.E. "Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers." arXiv, 2025.
23. Hou, X., Zhao, Y., Wang, S., and Wang, H. "Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions." arXiv, 2025.
24. Johnson, E., et al. "WaVe: A Verifiably Secure WebAssembly Sandboxing Runtime." IEEE S&P, 2023.
25. Kapravelos, A., Grier, C., Chachra, N., Kruegel, C., Vigna, G., and Paxson, V. "Hulk: Eliciting Malicious Behavior in Browser Extensions." USENIX Security, 2014.
26. Karliner, Z. "Rules File Backdoor: AI Code Editors Exploited for Silent Supply Chain Attacks." Pillar Security, 2025.
27. Kasturi, R.P., Fuller, J., Sun, Y., Chabklo, O., Rodriguez, A., Park, J., and Saltaformaggio, B. "Mistrust Plugins You Must: A Large-Scale Study Of Malicious Plugins In WordPress Marketplaces." USENIX Security, 2022.
28. Kim, Y.M. and Lee, B. "Extending a Hand to Attackers: Browser Privilege Escalation Attacks via Extensions." USENIX Security, 2023.
29. Ladisa, P., Plate, H., Martinez, M., and Barais, O. "SoK: Taxonomy of Attacks on Open-Source Software Supply Chains." IEEE S&P, 2023.
30. Lin, E., Koishybayev, I., Dunlap, T., Enck, W., and Kapravelos, A. "UntrustIDE: Exploiting Weaknesses in VS Code Extensions." NDSS, 2024.
31. Lins, M., Mayrhofer, R., Roland, M., Hofer, D., and Schwaighofer, M. "On the Critical Path to Implant Backdoors and the Effectiveness of Potential Mitigation Techniques: Early Learnings from XZ." arXiv, 2024 / CANS, 2025.
32. Liu, Y., et al. "Prompt Injection attack against LLM-integrated Applications (HouYi)." arXiv, 2023.
33. Liu, Y., et al. "Formalizing and Benchmarking Prompt Injection Attacks and Defenses." USENIX Security, 2024.
34. Maloyan, N. and Namiot, D. "Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis." arXiv, 2026.
35. Marzouk, A. "IDEsaster: A Novel Vulnerability Class in AI IDEs." Security Research Disclosure, 2025.
36. Miller, M.S. "Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control." PhD Thesis, Johns Hopkins University, 2006.
37. Nagle, F., Dana, J., Hoffman, J., Randazzo, S., and Zhou, Y. "Census II of Free and Open Source Software — Application Libraries." Linux Foundation / Harvard, 2022.
38. Nagle, F., Zitomer, R., Powell, K., and Wheeler, D.A. "Census III of Free and Open Source Software — Application Libraries." Linux Foundation / Harvard / OpenSSF, 2024.
39. Nayak, A., Khandelwal, R., Fernandes, E., and Fawaz, K. "Experimental Security Analysis of Sensitive Data Access by Browser Extensions." WWW, 2024.
40. Newman, Z., Meyers, J.S., and Torres-Arias, S. "Sigstore: Software Signing for Everybody." ACM CCS, 2022.
41. NIST. "AI-600-1: AI Risk Management Framework — Generative AI Profile." NIST Special Publication, 2024.
42. Ohm, M., Plate, H., Sykosch, A., and Meier, M. "Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks." DIMVA, 2020.
43. OWASP. "Top 10 Risks and Mitigations for Agentic AI Security." OWASP GenAI Security Project, 2025.
44. Pailoor, S., Wei, S., and Dillig, I. "Automated Policy Synthesis for System Call Sandboxing." OOPSLA, 2020.
45. Perez, F. and Ribeiro, I. "Ignore Previous Prompt: Attack Techniques For Language Models." NeurIPS ML Safety Workshop, 2022.
46. Perrone, G. and Romano, S.P. "WebAssembly and Security: A Review." arXiv, 2024.
47. Picazo-Sanchez, P., Ortiz-Martin, L., Schneider, G., and Sabelfeld, A. "Are Chrome Extensions Compliant with the Spirit of Least Privilege?" International Journal of Information Security, 2022.
48. Radosevich, B. and Halloran, J. "MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits." arXiv, 2025.
49. Ruan, Y., Dong, H., Wang, A., Pitis, S., Zhou, Y., Ba, J., Dubois, Y., Maddison, C.J., and Hashimoto, T. "Identifying the Risks of LM Agents with an LM-Emulated Sandbox (ToolEmu)." ICLR, 2024.
50. Sapkota, H., Murukannaiah, P.K., and Wang, Y. "A Network-Centric Approach for Estimating Trust Between Open Source Software Developers." PLOS ONE, 2019.
51. Schulhoff, S., et al. "Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities of LLMs through a Global Scale Prompt Hacking Competition." EMNLP, 2023.
52. Taylor, M.K., et al. "Defending Against Package Typosquatting (TypoGard)." NSS, 2020.
53. Torres-Arias, S., Afzali, H., Kuppusamy, T.K., Curtmola, R., and Cappos, J. "in-toto: Providing farm-to-table guarantees for bits and bytes." USENIX Security, 2019.
54. Toyer, S., et al. "Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game." NeurIPS Workshop, 2023.
55. Vu, D.-L., Pashchenko, I., Massacci, F., Plate, H., and Sabetta, A. "Typosquatting and Combosquatting Attacks on the Python Ecosystem." IEEE EuroS&PW, 2020.
56. Wahbe, R., Lucco, S., Anderson, T.E., and Graham, S.L. "Efficient Software-Based Fault Isolation." SOSP, 1993.
57. Wallace, E., Xiao, K., Leike, R., Weng, L., Heidecke, J., and Beutel, A. "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions." arXiv, 2024.
58. Wang, Z., et al. "MindGuard: Tracking, Detecting, and Attributing MCP Tool Poisoning Attack via Decision Dependence Graph." arXiv, 2025.
59. Watson, R.N.M., Anderson, J., Laurie, B., and Kennaway, K. "Capsicum: Practical Capabilities for UNIX." USENIX Security, 2010.
60. Wermke, D., Wöhler, N., Klemmer, J.H., Fourné, M., Acar, Y., and Fahl, S. "Committed to Trust: A Qualitative Study on Security & Trust in Open Source Software Projects." IEEE S&P, 2022.
61. Wermke, D., et al. ""Always Contribute Back": A Qualitative Study on Security Challenges of the Open Source Supply Chain." IEEE S&P, 2023.
62. Xie, Q., et al. "Arcanum: Detecting and Evaluating the Privacy Risks of Browser Extensions on Web Pages and Web Content." USENIX Security, 2024.
63. Yee, B., et al. "Native Client: A Sandbox for Portable, Untrusted x86 Native Code." IEEE S&P, 2009.
64. Young, E.G., Zhu, P., Caraza-Harter, T., Arpaci-Dusseau, A.C., and Arpaci-Dusseau, R.H. "The True Cost of Containing: A gVisor Case Study." USENIX HotCloud, 2019.
65. Zahan, N., Zimmermann, T., Godefroid, P., Murphy, B., Maddila, C., and Williams, L. "What are Weak Links in the npm Supply Chain?" ICSE SEIP, 2022.
66. Zahan, N., et al. "OpenSSF Scorecard: On the Path Toward Ecosystem-Wide Automated Security Metrics." IEEE Security & Privacy, 2023.
67. Zhang, H., et al. "Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents." ICLR, 2025.
68. Zhang, Z., et al. "Agent-SafetyBench: Evaluating the Safety of LLM Agents." arXiv, 2024.
69. Zhan, Q., Liang, Z., Ying, Z., and Kang, D. "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents." ACL Findings, 2024.
70. Zhu, K., Yang, X., Wang, J., Guo, W., and Wang, W.Y. "MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents." ICML, 2025.
71. Zimmermann, M., Staicu, C.-A., Tenny, C., and Pradel, M. "Small World with High Risks: A Study of Security Threats in the npm Ecosystem." USENIX Security, 2019.
72. Zou, A., Wang, Z., Carlini, N., Nasr, M., Kolter, J.Z., and Fredrikson, M. "Universal and Transferable Adversarial Attacks on Aligned Language Models." arXiv, 2023.
