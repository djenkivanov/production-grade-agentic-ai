# From Experiments to Expertise: Scientific Knowledge Consolidation for AI-Driven Computational Research

**Authors**: Haonan Huang
**Published**: 2026-03-13 17:25:47+00:00
**arXiv ID**: 2603.13191v1
**URL**: http://arxiv.org/abs/2603.13191v1

## Abstract
While large language models (LLMs) have transformed AI agents into proficient executors of computational materials science, performing a hundred simulations does not make a researcher. What distinguishes research from routine execution is the progressive accumulation of knowledge -- learning which approaches fail, recognizing patterns across systems, and applying understanding to new problems. However, the prevailing paradigm in AI-driven computational science treats each execution in isolation, largely discarding hard-won insights between runs. Here we present QMatSuite, an open-source platform closing this gap. Agents record findings with full provenance, retrieve knowledge before new calculations, and in dedicated reflection sessions correct erroneous findings and synthesize observations into cross-compound patterns. In benchmarks on a six-step quantum-mechanical simulation workflow, accumulated knowledge reduces reasoning overhead by 67% and improves accuracy from 47% to 3% deviation from literature -- and when transferred to an unfamiliar material, achieves 1% deviation with zero pipeline failures.

## Report
Overview

This paper introduces QMatSuite, an open-source platform that equips AI-driven computational materials-science agents with a persistent, provenance-backed 'scientific memory' so that experience accumulated across runs is preserved, reviewed, and abstracted into higher-level knowledge. The core motivation is that autonomous agents have largely solved execution (running simulations) but do not accumulate cross-session insights the way human researchers do. QMatSuite implements a graded knowledge hierarchy, integrated retrieval/recording nudges in the tool interface, and explicit reflection sessions to synthesize patterns and correct mistakes. The platform is engine-agnostic (15 simulation engines supported) and model-agnostic via the Model Context Protocol (MCP).

Platform design and implementation
- Three core design pillars: (1) engine-agnostic structured tools (intent-level APIs to hide engine specifics); (2) reproducible storage and end-to-end provenance; (3) persistent scientific memory with graded knowledge entries and three libraries (builtin curated best practices, local agent-generated insights, shareable community knowledge packs).
- Knowledge entries include scope tags, links to source calculations, and free-text reasoning; stored in SQLite with full-text search. Recording and review are performed through structured tools.
- The platform nudges agents at workflow junctions (pre-configuration searches, post-execution prompts). Recording is automated and lightweight.

Scale and cross-engine validation
- Solid-state validation: an agent ran structural relaxations and band-structure tasks on 135 materials with an 85.2% completion rate. Lattice constants showed a mean absolute error (MAE) of 1.02%; band gaps for non-metals displayed a MAE of 1.76 eV.
- Molecular validation: GPT 5.4 with ORCA 6.1.1 successfully completed 91 of 98 molecule geometry optimizations, achieving MAEs consistent with benchmarks.

Key experiment — AHC learning curve (Fe anomalous Hall conductivity)
- Three runs, using the same model and prompts, varied only by accumulated insights. As knowledge increased, reasoning time dropped and accuracy improved significantly.
- A crucial insight was documented that saved considerable debugging time in subsequent runs, demonstrating the effective transfer of knowledge.

Knowledge quality, review, and self-correction
- The agents recorded various insights during the AHC runs, most of which were found to be correct. One flawed recommendation was corrected during a dedicated review session.
- The experiments indicated that reviewed knowledge significantly improves operational efficiency compared to unreviewed knowledge.

Cross-material transfer (Fe → Ni)
- Applying knowledge from Fe to Ni yielded highly accurate results in fewer executions compared to the baseline, demonstrating the value of knowledge accumulated.

Knowledge consolidation and reflection
- An experiment across multiple zinc-blende semiconductors streamlined the process of generating patterns from findings, emphasizing the importance of reflection.

System-level observations and metrics
- Nudge compliance rates suggest that systematic reflection is necessary for effective knowledge synthesis.
- The retrieval mechanism, while useful, can sometimes fail to identify relevant insights.

Limitations and risks
- Some performance challenges remain, such as enhancing the retrieval mechanism and ensuring the reliability of insights.

Practical details and availability
- QMatSuite supports multiple tools and engines, is open-source, and is designed for broad applicability across computational research domains. Data will be publicly available upon publication.

Overall Assessment
- The framework laid out in the paper presents a plausible method for enhancing AI-driven computational science and encourages a shift towards a model of continuous learning and expertise building.
