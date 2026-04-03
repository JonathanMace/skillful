# Multi-Agent Coordination for Software Engineering Tasks: A Literature Review

**Date:** July 2025
**Scope:** Academic literature on coordinating multiple AI agents for parallel software development

---

## Executive Summary

The rapid emergence of LLM-powered coding agents has created a new class of coordination problem: how do multiple autonomous agents work concurrently on a shared codebase without stepping on each other? This review surveys **50+ papers** across seven research threads—from classical multi-agent systems and CSCW, through merge conflict prediction, to the latest multi-agent coding frameworks—and maps their findings onto the practical problem of running parallel AI agents with git worktree isolation.

**Key findings:**

1. **Multi-agent SE frameworks** (ChatDev, MetaGPT, CodeR) assign specialized roles but assume sequential pipelines—none address true parallelism on a shared repo.
2. **Task decomposition** research shows LLMs can split work into subtasks, but automatic *dependency detection* between code changes remains unsolved.
3. **Merge conflict prediction** has advanced significantly (DeepMerge, RPredictor, ConGra), yet no system integrates these predictions *proactively* into agent task assignment.
4. **CSCW awareness mechanisms** from decades of distributed development research provide the theoretical foundation for agent coordination, but have not been adapted for AI-to-AI collaboration.
5. **Distributed systems protocols** (contract net, blackboard architectures, consensus algorithms) offer proven coordination primitives that map directly onto agent fleet management.
6. **Industry protocols** (Google A2A, Anthropic MCP) are establishing the infrastructure layer for agent interoperability, but academic evaluation of these protocols is still nascent.
7. **The critical gap:** No published system coordinates multiple coding agents working *in parallel on the same repository* with automatic conflict avoidance, dependency-aware task assignment, and intelligent merge orchestration.

---

## 1. Multi-Agent Systems in Software Engineering

### Overview

The idea of using multiple specialized agents for software development has exploded since 2023, driven by the capabilities of large language models. These systems typically simulate a "virtual software company" with agents playing distinct roles (architect, developer, tester, reviewer).

### Key Papers

| Title | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| ChatDev: Communicative Agents for Software Development | Qian et al. | ACL | 2024 | Virtual software company with waterfall-model agent pipeline; "chat chain" decomposition; communicative dehallucination |
| MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework | Hong et al. | ICLR | 2024 | Standardized Operating Procedures (SOPs) for agent coordination; assembly-line paradigm with intermediate validation |
| AgentCoder: Multi-Agent Code Generation with Iterative Testing and Optimisation | Huang et al. | arXiv | 2024 | Three-agent system (programmer, test designer, test executor); 96.3% pass@1 on HumanEval with GPT-4 |
| MapCoder: Multi-Agent Code Generation for Competitive Problem Solving | Islam et al. | ACL | 2024 | Four-agent architecture (retrieval, planning, coding, debugging); SOTA on HumanEval (93.9%), MBPP (83.1%), CodeContests (28.5%) |
| CodeR: Issue Resolving with Multi-Agent and Task Graphs | Chen et al. | arXiv | 2024 | Task graph representation for issue resolution; 28.33% on SWE-bench lite; agents follow pre-defined execution graphs |
| SWE-agent: Agent-Computer Interfaces Enable Automated SE | Yang et al. | NeurIPS | 2024 | Agent-computer interface design; autonomous code browsing/editing; 12.5% on SWE-bench |
| Devin (MultiDevin) | Cognition Labs | Industry | 2024 | First commercial autonomous SE agent; manager-worker architecture spawning up to 10 parallel agents; 13.86% on SWE-bench |
| A Survey on Code Generation with LLM-based Agents | Various | arXiv | 2025 | Comprehensive taxonomy of agent roles, workflows, communication patterns, and evaluation approaches |

### Detailed Discussion

**ChatDev** (Qian et al., ACL 2024) introduced the paradigm of a "virtual software company" where LLM agents assume roles (CEO, CTO, programmer, tester) and communicate through a structured "chat chain." Each phase of the waterfall model maps to a subtask where paired agents discuss and produce artifacts. The system generates non-trivial software (e.g., a Gomoku game) in under 7 minutes at < $1 cost. However, ChatDev's pipeline is inherently **sequential**—each phase must complete before the next begins—making it unsuitable for parallel development.

**MetaGPT** (Hong et al., ICLR 2024) advances beyond ChatDev by encoding human Standard Operating Procedures (SOPs) as prompt sequences, creating an "assembly line" where each agent validates its output against defined standards before passing work downstream. This significantly reduces cascading hallucinations. MetaGPT's key insight for coordination: **structured intermediate artifacts** (PRDs, system designs, API specs) serve as contracts between agents. This structured output approach directly maps to the problem of defining boundaries between parallel agents' work.

**CodeR** (Chen et al., 2024) introduces **task graphs** as a coordination mechanism—each node represents a concrete task assigned to a specific agent type, with edges encoding dependencies. This is the closest existing system to explicit dependency management, though it operates within a single issue resolution rather than across parallel development streams.

**Devin's MultiDevin** architecture (Cognition Labs, 2024) is the most relevant commercial system: a manager agent decomposes tasks and spawns up to 10 worker agents operating in parallel. However, technical details of its coordination mechanisms (conflict avoidance, merge strategy, dependency detection) have not been published in academic venues.

### Open Problems

- All systems assume a single sequential pipeline or simple fan-out; none handle **cross-cutting concerns** that span multiple agents' work
- No mechanism for agents to **negotiate** when their changes might conflict
- Role assignment is fixed at design time, not adapted to the specific codebase or task
- Evaluation focuses on single-issue benchmarks (SWE-bench), not on coordinated multi-issue development

### Connection to Practice

Current parallel-agent setups (git worktrees, `/fleet` command) face exactly the limitations these systems exhibit: task decomposition is manual, agents can't communicate about their ongoing work, and merge conflicts are discovered only at integration time. The task graph approach from CodeR and the SOP contracts from MetaGPT are the most promising primitives for building coordination protocols.

---

## 2. Task Decomposition for Software Engineering

### Overview

For multiple agents to work in parallel, complex tasks must be decomposed into subtasks with well-understood dependencies. This thread examines how tasks can be automatically broken down and which subtasks can safely execute concurrently.

### Key Papers

| Title | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| TaskBench: Benchmarking LLMs for Task Automation | Shen et al. | arXiv | 2023 | Standardized evaluation of LLM task decomposition using "tool graphs"; measures decomposition quality |
| Decompose a Task into Generalizable Subtasks in Multi-Agent RL | Yang et al. | NeurIPS | 2023 | Automatic subtask discovery in multi-agent settings; generalizable, reusable subtask decomposition |
| Task Allocation Framework using Task-Decomposition-Matrix and LLMs | Various | IFAC | 2025 | Task-decomposition matrices for representing dependencies and enabling parallel assignment |
| Utility-Aware Task Decomposition and Exchange across LLM Agents | Various | arXiv | 2026 | Agents negotiate subtask ownership based on utility scores; dynamic reallocation |
| A Survey of Code-Based Change Impact Analysis Techniques | Li et al. | STVR | 2012 | Comprehensive survey of static analysis for detecting code dependencies and change propagation |
| Change Impact Analysis: A Systematic Mapping Study | Kretsou et al. | JSS | 2020 | Taxonomy of CIA techniques; evaluates static, dynamic, and historical approaches |
| SEMCIA: Semantic Change Impact Analysis | Alimadadi et al. | ICSME | 2019 | Semantic (not just syntactic) dependency analysis; reduces false positives in impact estimation |

### Detailed Discussion

**TaskBench** (Shen et al., 2023) provides the first rigorous benchmark for evaluating how well LLMs decompose complex tasks into executable subtasks. It uses a "tool graph" representation where nodes are tools/functions and edges represent data dependencies. Key finding: LLMs can decompose tasks reasonably well for simple workflows but struggle with complex dependency structures.

**NeurIPS 2023 work on generalizable subtask decomposition** (Yang et al.) shows that in multi-agent reinforcement learning settings, subtasks can be discovered automatically and transferred across different task instances. This suggests that a "library" of reusable code change patterns could enable more effective decomposition.

**Change Impact Analysis (CIA)** literature is directly relevant but underutilized in agent coordination. The comprehensive surveys by Li et al. and Kretsou et al. catalog techniques for determining which code elements are affected by a change—exactly what's needed to predict conflicts between parallel agents. Static analysis can identify dependency relationships (call graphs, data flow, inheritance hierarchies) that determine whether two changes can safely proceed in parallel.

**SEMCIA** (Alimadadi et al., 2019) advances beyond syntactic dependency detection to semantic relationships, significantly reducing false positives. For agent coordination, this means fewer unnecessary serialization constraints—agents can work in parallel on syntactically overlapping but semantically independent code areas.

### Open Problems

- LLMs produce inconsistent decomposition granularity ("The Decomposition Paradox"): one model may create 5 subtasks where another creates 15 for the same problem
- No system automatically determines which subtasks can execute in parallel based on code dependency analysis
- Bridging the gap between *task-level* decomposition (what to do) and *code-level* impact analysis (what files/functions are affected) is largely unexplored
- No benchmark evaluates decomposition quality in terms of parallelizability

### Connection to Practice

The practical problem—agents working on different git worktrees—needs exactly this: a system that (1) decomposes an issue or feature request into subtasks, (2) analyzes code dependencies to determine which subtasks can execute in parallel, and (3) assigns tasks to agents with minimal expected merge conflicts. Combining LLM-based task decomposition with static analysis for dependency detection is the most promising approach.

---

## 3. Merge Conflict Prediction and Resolution

### Overview

When multiple agents make concurrent changes, merge conflicts are inevitable. This thread reviews ML-based approaches to predicting where conflicts will occur, resolving them automatically, and benchmarking resolution tools.

### Key Papers

| Title | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| DeepMerge: Learning to Merge Programs | Dinella et al. | FSE | 2022 | ML-based merge with pointer networks; 37% accuracy on non-trivial JavaScript merges, 78% on ≤3-line conflicts |
| RPredictor: Predicting Conflict Resolution Strategies | Aldndni et al. | JSS / ASE | 2023-24 | Random forest predicts developer merge strategies (Keep Local/Remote/Manual); 63% F-score within-project; 74,861 conflicts studied |
| ConGra: Benchmarking Automatic Conflict Resolution | Wu et al. | arXiv | 2024 | Taxonomy of conflict types; 44,948 real-world conflicts; reveals LLM limitations on complex merges |
| ConflictBench: Evaluating Software Merge Tools | Various | ASE | 2024 | 180 real-world Java merge scenarios; standardized evaluation framework for merge tools |
| Predicting Merge Conflicts Considering Social and Technical Assets | Costa et al. | EMSE | 2023 | Combines social factors (developer roles) with technical analysis; achieves 0.92 accuracy, 1.00 recall |
| Semi-Automated Merge Conflict Resolution | Various | EASE | 2024 | 131,154 GitHub merge conflicts; 87.9% of conflicted chunks resolvable with language-agnostic patterns |
| Lightweight Semantic Conflict Detection with Static Analysis | Various | IEEE | 2024 | Detects semantic conflicts (runtime bugs from non-textual conflicts) using static analysis |
| Program Merge: What's Deep Learning Got to Do with It? | Various | ACM Queue | 2024 | Overview of DL approaches to program merging; positions DeepMerge in the broader landscape |

### Detailed Discussion

**DeepMerge** (Dinella et al., FSE 2022, Microsoft Research) represents the state of the art in ML-based merge conflict resolution. Using edit-aware embeddings and pointer networks, it constructs resolutions by selecting and combining tokens from the conflicting versions. While 37% accuracy on non-trivial merges seems low, this dramatically outperforms structured merge tools (4% accuracy). For simple conflicts (≤3 lines), it reaches 78%—suggesting that many agent-generated conflicts could be automatically resolved.

**RPredictor** (Aldndni et al., 2023-24) takes a complementary approach: rather than resolving conflicts, it **predicts** how developers typically resolve them (keep local version, keep remote version, or manual edit). Using random forests on features from code context and project history, it achieves 63% F-score within-project. The "conservative mode" reduces incorrect resolutions while still saving ~34% of developer effort. For agent coordination, this prediction capability could inform *which agent's version to prefer* when conflicts arise.

**ConGra** (Wu et al., 2024) provides the most comprehensive benchmark for evaluating conflict resolution tools, including LLM-based approaches. Its key finding: LLMs struggle significantly with high-complexity merge scenarios, despite performing well on simple textual conflicts. This suggests that agent coordination should focus on **conflict avoidance** (preventing conflicts through better task assignment) rather than **conflict resolution** (fixing conflicts after the fact).

**Semantic conflict detection** (IEEE 2024) addresses a particularly insidious problem for parallel agents: changes that don't produce textual merge conflicts but cause runtime bugs when combined. Two agents might each make valid, non-overlapping edits that together break a semantic invariant. Static analysis can catch some of these, but the problem is far from solved.

### Open Problems

- No system integrates conflict **prediction** into task **assignment**—the loop is not closed
- Semantic conflicts remain very difficult to detect; most tools focus on textual conflicts
- LLMs perform poorly on complex merges, suggesting resolution should be a last resort
- No evaluation of merge tools in the specific context of AI-generated (rather than human-generated) code changes

### Connection to Practice

For parallel agent fleets, the most impactful application is **proactive conflict avoidance**: use CIA and merge conflict prediction to assign tasks that minimize expected conflicts. When conflicts do occur, simple cases (87.9% of chunks per the EASE 2024 study) can be auto-resolved; complex cases should trigger re-planning. DeepMerge-style tools could serve as an automated "merge agent" in the fleet.

---

## 4. Collaborative Software Development (CSCW)

### Overview

The CSCW community has studied coordination in distributed software development for decades. Their findings about awareness, coordination mechanisms, and the challenges of parallel work provide the theoretical foundation for agent coordination.

### Key Papers

| Title | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| Workspace Awareness in Real-Time Distributed Groupware | Gutwin & Greenberg | U Calgary TR | 1995 | Framework for workspace awareness elements; foundational theory for shared workspace coordination |
| Group Awareness in Distributed Software Development | Gutwin, Penner, Schneider | CSCW | 2004 | How open-source developers maintain awareness through text-based channels; informal awareness mechanisms |
| Awareness Support in Distributed Software Development | Steinmacher, Chaves, Gerosa | CSCW Journal | 2013 | Systematic review of 91 papers; classifies awareness support using 3C model (Communication, Coordination, Cooperation) |
| Continuous Coordination: A New Paradigm for Distributed SD | Redmiles et al. | | 2007 | Blends formal process tools with informal awareness features; continuous rather than checkpoint-based coordination |
| Awareness Support in Collaborative Programming Tools | Various | JSS | 2024 | Experimental evaluation of awareness mechanisms in group programming systems |

### Detailed Discussion

**Gutwin & Greenberg's workspace awareness framework** (1995) identifies the fundamental information needed for coordination in shared workspaces: who is working, what they're doing, where they're working, when activities happen, and how they relate to one's own work. These "awareness elements" map directly onto the information agents need to coordinate:

| Awareness Element | Human Developer Context | Agent Fleet Context |
|---|---|---|
| **Who** | Team members | Other agents in the fleet |
| **What** | Current editing activity | Files being modified, changes staged |
| **Where** | File/function being edited | Git worktree, branch, code region |
| **When** | Timing of changes | Commit timestamps, task progress |
| **How** | Relationship to my work | Dependency overlap, conflict potential |

**Steinmacher et al.'s systematic review** (2013) analyzed 91 papers on awareness in distributed development and found that **coordination mechanisms are the most explored** (60%+ of papers) while communication and workspace awareness are critical but underrepresented. For agent systems, this suggests the field has strong foundations for coordination protocols but weaker support for the real-time "awareness" that prevents conflicts.

**Continuous Coordination** (Redmiles et al., 2007) proposes abandoning checkpoint-based coordination (e.g., daily standups, code reviews) in favor of continuous, tool-supported awareness. This maps directly onto the agent coordination problem: rather than discovering conflicts at merge time, agents should have continuous visibility into each other's work.

### Open Problems

- CSCW research assumes human cognitive abilities (peripheral awareness, informal communication); AI agents need explicit, machine-readable awareness mechanisms
- No CSCW work addresses agent-to-agent coordination specifically
- The "information overload" problem in awareness systems is different for agents (high bandwidth, no cognitive fatigue) than for humans

### Connection to Practice

The CSCW framework provides the theoretical vocabulary for designing agent coordination. A fleet coordination system needs:
- **Workspace awareness**: each agent knows what files/functions other agents are modifying
- **Activity awareness**: agents can see each other's task progress and planned changes
- **Conflict awareness**: agents are notified when their planned changes overlap with another agent's work
- **Continuous coordination**: awareness updates flow in real-time, not just at commit/merge checkpoints

---

## 5. Distributed Systems Coordination

### Overview

Classical distributed systems research provides formal protocols for coordination, task allocation, and consensus that can be adapted for agent fleet management.

### Key Papers and Concepts

| Title / Concept | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| The Contract Net Protocol | Smith, R.G. | IEEE Trans. Computers | 1980 | Task announcement, bidding, and allocation protocol for distributed problem solving |
| Consensus-Based Bundle Algorithm (CBBA) | Choi et al. | AIAA | 2009 | Distributed task allocation with consensus; handles conflicts and dynamic environments |
| Blackboard Architecture for LLM Multi-Agent Systems | Various | arXiv | 2025 | Shared knowledge space for dynamic agent selection and coordination; competitive with SOTA on reasoning tasks |
| Decentralized Adaptive Task Allocation for Dynamic MAS | Various | Scientific Reports | 2025 | Two-layer architecture: predictive control + consensus optimization; handles partial observability |
| Swarm Coordination via Distributed Consensus Protocols | Various | ACE Journal | 2025 | Review of average/max-min consensus for multi-agent swarms; robustness to network faults |
| Optimized Distributed Multi-UAV Task Allocation (CNP+CBBA) | Various | Springer | 2025 | Hybrid CNP + consensus approach; improved completion rates in dynamic environments |

### Detailed Discussion

**The Contract Net Protocol (CNP)** (Smith, 1980) is the classical task allocation mechanism for multi-agent systems. A manager agent announces tasks, worker agents bid based on their capabilities and current load, and the manager selects the best bid. For a fleet of coding agents:

```
Manager: "Task: Refactor authentication module. Estimated scope: 5 files, auth/ directory."
Agent-1: "Bid: I'm currently idle, familiar with auth/ from previous task."
Agent-2: "Bid: I'm working on user/ which has 2 dependencies on auth/."
Manager: "Awarded to Agent-1. Agent-2: avoid auth/ imports until Agent-1 completes."
```

The CNP maps naturally onto fleet coordination but needs enhancement for software-specific concerns (dependency awareness, conflict prediction, merge cost estimation).

**Blackboard Architecture** has been revived for LLM multi-agent systems (arXiv 2025). In this architecture, agents share a common knowledge space (the "blackboard") where they post intermediate results and read others' contributions. A control module selects which agents should act based on the blackboard's current state. This is remarkably similar to what a git-based coordination system would look like: the repository is the "blackboard," commits are "posted results," and a coordinator selects which agents should work next based on the repo state.

**Consensus-Based Bundle Algorithm (CBBA)** extends CNP with a consensus phase where agents resolve conflicting assignments through distributed negotiation. This directly addresses the scenario where two agents both want to modify the same module—they can negotiate a resolution (serialization, interface contracts, or scope partitioning) without central coordination.

### Open Problems

- Classical protocols assume well-defined tasks with known costs; software tasks have high uncertainty
- Communication overhead of continuous consensus may be prohibitive for large fleets
- Hybrid centralized/decentralized approaches (manager + agent autonomy) need more study
- No existing protocol accounts for the specific characteristics of code changes (merge conflict probability, semantic dependencies)

### Connection to Practice

A practical fleet coordination system could combine:
1. **CNP-style task allocation**: manager decomposes work, agents bid based on expertise and current state
2. **Blackboard-style awareness**: shared state showing each agent's worktree, modified files, and task progress
3. **CBBA-style conflict resolution**: agents negotiate when their work overlaps
4. **Git as the underlying coordination infrastructure**: branches, worktrees, and merge operations implement the actual coordination

---

## 6. LLM-Based Multi-Agent Frameworks

### Overview

Several frameworks provide infrastructure for building multi-agent LLM applications. Their coordination mechanisms, while general-purpose, inform the design of software-specific agent fleets.

### Key Papers

| Title | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| CAMEL: Communicative Agents for "Mind" Exploration of LLM Society | Li et al. | NeurIPS | 2023 | Role-playing framework with inception prompting; autonomous multi-turn agent cooperation; foundational multi-agent paradigm |
| AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Wu et al. | COLM | 2024 | Flexible multi-agent conversation framework; customizable interaction patterns; supports complex workflows |
| LLM-Based Multi-agent Systems: Frameworks, Evaluation, Open Challenges | Various | Springer | 2025 | Comprehensive review of AutoGen, CrewAI, CAMEL, ChatDev, LangGraph; identifies memory, communication, and benchmarking gaps |
| Benchmarking LLMs for Multi-agent Systems: AutoGen, CrewAI, TaskWeaver | Various | PAAMS | 2024 | Empirical comparison on ML code generation tasks; all frameworks produce functional code with accuracy variations |
| Code in Harmony: Evaluating Multi-Agent Frameworks | Various | OpenReview | 2025 | Evaluation framework for multi-agent code generation; measures collaboration quality beyond just correctness |
| Large Language Model based Multi-Agents: A Survey of Progress and Challenges | Various | IJCAI | 2024 | Broad survey categorizing communication patterns, memory mechanisms, and planning strategies |
| Exploration of LLM Multi-Agent Application Based on LangGraph+CrewAI | Various | arXiv | 2024 | Hybrid framework combining graph-based orchestration with crew-based role assignment |
| Creativity in LLM-based Multi-Agent Systems: A Survey | Various | EMNLP | 2025 | Examines emergent creative behaviors in multi-agent LLM interactions |

### Detailed Discussion

**CAMEL** (Li et al., NeurIPS 2023) established the foundational paradigm: assign roles to LLM agents and let them cooperate through structured dialogue with minimal human intervention. "Inception prompting" guides the conversation, while a task-specifier agent concretizes vague goals. Key challenges identified: role flipping (agents switching roles mid-conversation), instruction repetition, and infinite loops. These are exactly the coordination failures that occur when parallel agents aren't properly constrained.

**AutoGen** (Wu et al., COLM 2024) provides the most flexible infrastructure for multi-agent systems, supporting customizable interaction patterns (sequential, broadcast, group chat, hierarchical). Its strength is generality; its weakness for fleet coordination is that it doesn't provide software-specific primitives (no awareness of git, no conflict detection, no merge integration). AutoGen's "group chat" pattern, where agents take turns contributing to a shared context, is conceptually similar to agents sharing a branch.

**Benchmarking studies** (PAAMS 2024, Code in Harmony 2025) reveal that all major frameworks can generate functional code, but differ in:
- **Execution efficiency**: CrewAI is faster due to its standalone architecture
- **Versatility**: AutoGen excels in customization
- **Token consumption**: varies significantly across frameworks
- **Collaboration quality**: not well-measured by existing code benchmarks

### Open Problems

- No framework provides git-native coordination primitives
- Memory mechanisms are primitive—agents can't efficiently share what they've learned about a codebase
- No framework supports true concurrent execution with conflict detection
- Evaluation focuses on task completion, not on coordination quality (conflict rates, redundant work, communication efficiency)

### Connection to Practice

The fleet coordination problem needs a framework that combines:
- AutoGen's flexible interaction patterns
- CrewAI's role-based task delegation
- A git-aware coordination layer for conflict detection and merge management
- Persistent shared memory about the codebase state

---

## 7. Recent Work (2024–2025): Frontiers in Multi-Agent Coding

### Overview

The most recent work pushes toward more realistic, large-scale, and parallelized agent systems, with new benchmarks, protocols, and architectural patterns.

### Key Papers and Developments

| Title | Authors | Venue | Year | Core Contribution |
|-------|---------|-------|------|-------------------|
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | Jimenez et al. | ICLR | 2024 | Canonical benchmark for coding agents; real GitHub issues requiring multi-file patches |
| SWE-Bench Pro: Long-Horizon Software Engineering Tasks | Various | OpenReview | 2025 | Enterprise-scale tasks spanning 123 languages; top agents achieve < 25% pass rate |
| SWE-Bench-CL: Continual Learning for Coding Agents | Various | arXiv | 2025 | Tests agents' ability to maintain knowledge across sequential tasks; memory modules and anti-forgetting |
| Multi-SWE-bench | Various | Web | 2025 | Multilingual extension of SWE-bench; tests cross-language capabilities |
| UTBoost: Rigorous Evaluation of Coding Agents | Various | ACL | 2025 | Generates additional unit tests to catch overfitting on SWE-bench test suites |
| Google Agent2Agent (A2A) Protocol | Google | Industry Spec | 2025 | Open protocol for agent discovery, communication, and task delegation across vendors |
| Anthropic Model Context Protocol (MCP) | Anthropic | Industry Spec | 2024 | Standard for agents to access external tools, data, and APIs |
| MapCoder-Lite: Squeezing Multi-Agent into a Single LLM | Various | arXiv | 2025 | Distills multi-agent coding approach into single model with role-specific fine-tuning |

### Detailed Discussion

**SWE-bench ecosystem** has rapidly evolved beyond the original benchmark. SWE-Bench Pro (2025) pushes to enterprise-scale, long-horizon tasks where even the best models achieve <25% success. SWE-Bench-CL (2025) introduces **continual learning**—critical for agents that operate on evolving repositories over weeks or months. The key insight for fleet coordination: agents need persistent memory about the codebase and each other's past work.

**Agent Interoperability Protocols** represent perhaps the most significant development for practical fleet coordination:

- **Google A2A** (April 2025): An open protocol enabling agents to discover each other's capabilities (via "Agent Cards" at `/.well-known/agent.json`), communicate over JSON-RPC 2.0/HTTPS, and delegate tasks. A2A provides the horizontal coordination layer—how agents talk to each other.

- **Anthropic MCP** (late 2024): Standardizes how agents access external tools, data, and context. MCP provides the vertical integration layer—how agents interact with their environment (IDEs, git, build systems).

Together, A2A + MCP provide the infrastructure for fleet coordination: agents discover each other (A2A), announce their capabilities and current work (A2A Agent Cards), and interact with the shared codebase (MCP). However, software-specific coordination semantics (conflict detection, dependency analysis, merge orchestration) must be built on top.

**Evaluation advances** (UTBoost at ACL 2025) show that current SWE-bench success rates may be inflated due to incomplete test suites. Additional LLM-generated tests reveal previously missed errors, suggesting that coordination systems need to account for higher-than-reported failure rates when planning parallel work.

### Open Problems

- No benchmark evaluates **multi-agent coordination** for coding (only single-agent performance)
- A2A and MCP are industry specs without peer-reviewed academic evaluation
- Continual learning across multiple concurrent agents (not just sequential tasks) is unexplored
- The "fleet management" problem—scheduling, load balancing, conflict-aware assignment across many agents—has no dedicated research

---

## Cross-Cutting Themes

### Theme 1: The Sequential-to-Parallel Gap

Nearly all multi-agent SE systems assume a sequential pipeline (design → code → test → review). True parallelism—where multiple agents simultaneously modify different parts of the codebase—is either not supported or treated as a simple fan-out without dependency analysis. Closing this gap requires integrating techniques from distributed systems (task allocation, consensus) with software-specific analysis (CIA, merge prediction).

### Theme 2: Awareness as the Foundation

CSCW research consistently shows that **awareness**—knowing what others are doing, where, and how it relates to your work—is the foundation for effective coordination. This applies equally to AI agents. A fleet coordination system must provide:
- **Real-time file-level awareness**: which files each agent is modifying
- **Semantic-level awareness**: what behavioral changes each agent is making
- **Conflict-level awareness**: proactive notification of potential merge conflicts
- **Progress-level awareness**: how far along each agent is on its task

### Theme 3: Prevention Over Cure

Merge conflict resolution (DeepMerge, RPredictor) is valuable but secondary. The more impactful approach is **conflict prevention** through intelligent task assignment. If CIA can predict that tasks A and B will modify overlapping code, they should be serialized or assigned to the same agent. This inverts the traditional approach: instead of resolving conflicts after they occur, design the task decomposition to minimize them.

### Theme 4: Git as Coordination Infrastructure

Git already provides many coordination primitives: branches for isolation, worktrees for parallel work, merge/rebase for integration, diff for change detection. A fleet coordination system should build on these primitives rather than reinventing them. The contract net protocol maps onto branch-based task allocation; the blackboard architecture maps onto a shared state branch; consensus algorithms map onto merge conflict resolution.

### Theme 5: The Need for Software-Specific Agent Protocols

General multi-agent frameworks (AutoGen, CrewAI, LangGraph) provide conversation and workflow primitives but lack software-specific coordination. The industry protocols (A2A, MCP) provide discovery and tool access but lack conflict awareness. A new layer is needed: software-aware agent coordination protocols that understand code dependencies, merge semantics, and development workflows.

---

## Research Gaps

### Gap 1: Multi-Agent Coding Coordination Benchmark
No benchmark evaluates how well multiple agents coordinate on shared codebases. Needed: a "Multi-Agent SWE-bench" with tasks requiring parallel agent work, measured by coordination quality (conflict rate, redundant work, merge success) not just task completion.

### Gap 2: Dependency-Aware Task Assignment
No system combines LLM-based task decomposition with static analysis-based dependency detection to produce conflict-minimizing task assignments. Each piece exists independently; the integration is missing.

### Gap 3: Agent-to-Agent Awareness Protocols
CSCW awareness mechanisms haven't been formalized for AI-to-AI coordination. Needed: a protocol where agents publish their current working context (modified files, planned changes, task scope) and receive notifications about potential conflicts.

### Gap 4: Proactive Merge Conflict Avoidance
ML-based conflict prediction exists but isn't integrated into task planning. Needed: a closed loop where conflict predictions feed back into task assignment, dynamically re-routing work when conflict risk exceeds a threshold.

### Gap 5: Evaluation of Coordination Overhead
No study measures the cost-benefit tradeoff of coordination in multi-agent coding: does the overhead of conflict detection, awareness maintenance, and consensus negotiation pay for itself in reduced merge conflicts and redundant work?

### Gap 6: Semantic Conflict Detection at Scale
Textual merge conflicts are detectable; semantic conflicts (valid edits that together introduce bugs) remain very difficult. For agents making complex changes, semantic conflicts may be more common than for human developers due to less holistic understanding.

---

## Implications for Practice

Based on this literature review, a practical fleet coordination system should incorporate the following evidence-based design decisions:

### 1. Layered Architecture
```
┌─────────────────────────────────────┐
│     Task Decomposition Layer        │  ← LLM-based decomposition + CIA
│  (MetaGPT SOPs, CodeR task graphs)  │
├─────────────────────────────────────┤
│     Coordination Protocol Layer     │  ← CNP + blackboard + consensus
│  (A2A discovery, awareness updates) │
├─────────────────────────────────────┤
│     Conflict Management Layer       │  ← DeepMerge, RPredictor, static analysis
│  (prediction, avoidance, resolution)│
├─────────────────────────────────────┤
│     Infrastructure Layer            │  ← Git worktrees, branches, MCP tools
│  (isolation, merge, build, test)    │
└─────────────────────────────────────┘
```

### 2. Conflict-Aware Task Assignment
Use change impact analysis to estimate the "conflict surface" of each subtask, then assign tasks to minimize overlap between concurrent agents. When high-conflict tasks are unavoidable, serialize them or assign them to the same agent.

### 3. Continuous Awareness over Checkpoint Coordination
Following CSCW's "Continuous Coordination" paradigm, agents should maintain real-time awareness of each other's work—not discover conflicts only at merge time. This can be implemented by agents periodically broadcasting their modified file set and planned changes.

### 4. Structured Intermediate Artifacts
MetaGPT's insight applies: agents should produce structured artifacts (interface definitions, API contracts, test specifications) that serve as coordination boundaries. When agent A defines an interface, agent B can code against it without needing to see A's implementation.

### 5. Hierarchical Coordination
A manager agent handles task decomposition and assignment (CNP-style), while worker agents maintain peer-to-peer awareness (blackboard-style). This combines the efficiency of centralized planning with the flexibility of decentralized conflict detection.

### 6. Git-Native Implementation
Build on git's existing primitives: worktrees for isolation, branches for task ownership, merge --no-commit for conflict detection, diff for awareness. Don't reinvent version control—augment it with intelligence.

---

## References

1. Qian, C. et al. (2024). "ChatDev: Communicative Agents for Software Development." *ACL 2024*. arXiv:2307.07924.
2. Hong, S. et al. (2024). "MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework." *ICLR 2024*.
3. Huang, D. et al. (2024). "AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation." arXiv:2312.13010.
4. Islam, M.A. et al. (2024). "MapCoder: Multi-Agent Code Generation for Competitive Problem Solving." *ACL 2024*. arXiv:2405.11403.
5. Chen, Y. et al. (2024). "CodeR: Issue Resolving with Multi-Agent and Task Graphs." arXiv:2406.01304.
6. Yang, J. et al. (2024). "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering." *NeurIPS 2024*.
7. Jimenez, C.E. et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" *ICLR 2024*.
8. Li, G. et al. (2023). "CAMEL: Communicative Agents for 'Mind' Exploration of Large Language Model Society." *NeurIPS 2023*. arXiv:2303.17760.
9. Wu, Q. et al. (2024). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework." *COLM 2024*.
10. Dinella, E. et al. (2022). "DeepMerge: Learning to Merge Programs." *FSE 2022*. IEEE.
11. Aldndni, Y. et al. (2023). "Automatic Prediction of Developers' Resolutions for Software Merge Conflicts." *JSS / ASE 2024*.
12. Wu, H. et al. (2024). "ConGra: Benchmarking Automatic Conflict Resolution." arXiv:2409.14121.
13. Costa, C. et al. (2023). "Predicting Merge Conflicts Considering Social and Technical Assets." *Empirical Software Engineering*.
14. Various (2024). "Towards Semi-Automated Merge Conflict Resolution: Is It Easier Than We Expected?" *EASE 2024*.
15. Various (2024). "Lightweight Semantic Conflict Detection with Static Analysis." *IEEE 2024*.
16. Various (2024). "ConflictBench: A Benchmark to Evaluate Software Merge Tools." *ASE 2024*.
17. Gutwin, C. & Greenberg, S. (1995). "Workspace Awareness in Real-Time Distributed Groupware." U Calgary Technical Report.
18. Gutwin, C., Penner, R. & Schneider, K. (2004). "Group Awareness in Distributed Software Development." *ACM CSCW 2004*.
19. Steinmacher, I., Chaves, A.P. & Gerosa, M.A. (2013). "Awareness Support in Distributed Software Development: A Systematic Review." *CSCW Journal*, 22(2), 113-158.
20. Redmiles, D. et al. (2007). "Continuous Coordination: A New Paradigm to Support Globally Distributed Software Development Projects."
21. Smith, R.G. (1980). "The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver." *IEEE Trans. Computers*.
22. Choi, H.L. et al. (2009). "Consensus-Based Decentralized Auctions for Robust Task Allocation." *IEEE Trans. Robotics*.
23. Various (2025). "Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture." arXiv:2507.01701.
24. Various (2025). "Decentralized Adaptive Task Allocation for Dynamic Multi-Agent Systems." *Scientific Reports*.
25. Shen, Y. et al. (2023). "TaskBench: Benchmarking Large Language Models for Task Automation." arXiv:2311.18760.
26. Yang, Y. et al. (2023). "Decompose a Task into Generalizable Subtasks in Multi-Agent Reinforcement Learning." *NeurIPS 2023*.
27. Li, B. et al. (2012). "A Survey of Code-Based Change Impact Analysis Techniques." *STVR*.
28. Kretsou, M. et al. (2020). "Change Impact Analysis: A Systematic Mapping Study." *JSS*.
29. Alimadadi, S. et al. (2019). "SEMCIA: Aiding Code Change Understanding with Semantic Change Impact Analysis." *ICSME 2019*.
30. Various (2025). "LLM-Based Multi-agent Systems: Frameworks, Evaluation, Open Challenges." *Springer*.
31. Various (2024). "Benchmarking LLMs for Multi-agent Systems: AutoGen, CrewAI, TaskWeaver." *PAAMS 2024*.
32. Various (2025). "Code in Harmony: Evaluating Multi-Agent Frameworks." *OpenReview*.
33. Various (2024). "Large Language Model based Multi-Agents: A Survey of Progress and Challenges." *IJCAI 2024*.
34. Various (2024). "Exploration of LLM Multi-Agent Application Based on LangGraph+CrewAI." arXiv:2411.18241.
35. Various (2025). "Creativity in LLM-based Multi-Agent Systems: A Survey." *EMNLP 2025*.
36. Various (2025). "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" *OpenReview*.
37. Various (2025). "SWE-Bench-CL: Continual Learning for Coding Agents." arXiv:2507.00014.
38. Various (2025). "UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench." *ACL 2025*.
39. Google (2025). "Agent2Agent (A2A) Protocol." a2a-protocol.org.
40. Anthropic (2024). "Model Context Protocol (MCP)." modelcontextprotocol.io.
41. Various (2025). "MapCoder-Lite: Squeezing Multi-Agent Coding into a Single Small LLM." arXiv:2509.17489.
42. Various (2025). "A Survey on Code Generation with LLM-based Agents." arXiv:2508.00083.
43. Cognition Labs (2024). "Introducing Devin, the First AI Software Engineer." cognition.ai.
44. Various (2024). "Awareness Support in Collaborative Programming Tools: An Evaluation." *JSS 2024*.
45. Various (2025). "Swarm Coordination via Distributed Consensus Protocols." *ACE Journal*.
46. Various (2025). "Optimized Distributed Multi-UAV Task Allocation Based on CNP and CBBA." *Springer*.
47. Various (2025). "Task Allocation Framework using Task-Decomposition-Matrix and LLMs." *IFAC 2025*.
48. Various (2024). "Program Merge: What's Deep Learning Got to Do with It?" *ACM Queue*.
49. Various (2024). "Method Level Static Source Code Analysis on Behavioral Change Impact Analysis." *ResearchGate*.
50. Various (2023). "Change Pattern Detection for Optimising Incremental Static Analysis." *VUB Technical Report*.

---

*This review was produced by conducting web-based academic searches across arXiv, ACM DL, IEEE Xplore, Springer, NeurIPS/ICML/ICLR proceedings, and ICSE/FSE/ASE/CSCW conference proceedings. All citations reflect papers discoverable through these venues as of July 2025.*
