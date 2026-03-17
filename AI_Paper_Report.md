# Mixture-of-Depths Attention

**Authors**: Lianghui Zhu, Yuxin Fang, Bencheng Liao, Shijie Wang, Tianheng Cheng, Zilong Huang, Chen Chen, Lai Wei, Yutao Zeng, Ya Wang, Yi Lin, Yu Li, Xinggang Wang
**Published**: 2026-03-16 17:59:55+00:00
**arXiv ID**: 2603.15619v1
**URL**: http://arxiv.org/abs/2603.15619v1

## Abstract
Scaling depth is a key driver for large language models (LLMs). Yet, as LLMs become deeper, they often suffer from signal degradation: informative features formed in shallow layers are gradually diluted by repeated residual updates, making them harder to recover in deeper layers. We introduce mixture-of-depths attention (MoDA), a mechanism that allows each attention head to attend to sequence KV pairs at the current layer and depth KV pairs from preceding layers. We further describe a hardware-efficient algorithm for MoDA that resolves non-contiguous memory-access patterns, achieving 97.3% of FlashAttention-2's efficiency at a sequence length of 64K. Experiments on 1.5B-parameter models demonstrate that MoDA consistently outperforms strong baselines. Notably, it improves average perplexity by 0.2 across 10 validation benchmarks and increases average performance by 2.11% on 10 downstream tasks, with a negligible 3.7% FLOPs computational overhead. We also find that combining MoDA with post-norm yields better performance than using it with pre-norm. These results suggest that MoDA is a promising primitive for depth scaling.

## Report
Problem and Motivation:
- Modern Transformer LLMs scale poorly with depth due to information dilution: repeated residual updates compress layer history into a single trajectory and dilute salient shallow-layer signals, making them harder to recover in deep stacks. Dense cross-layer connections (DenseNet-style) mitigate dilution but are prohibitively expensive in parameters and compute at LLM scale.
- The paper asks whether adaptive, data-dependent retrieval of depth-history (cross-layer states) can be combined with sequence attention efficiently and practically for large-scale training.

Key idea — Mixture-of-Depths Attention (MoDA):
- MoDA extends standard attention by letting each attention head jointly attend to (a) sequence KV (keys/values of the current layer across positions) and (b) depth KV (per-position keys/values collected from preceding layers at the same sequence position). All logits are combined and normalized under a single softmax (a unified softmax over sequence+depth slots).
- Intuition: attention's data-dependent mixing that works for temporal sequence retrieval can be used along the depth axis to adaptively retrieve useful intermediate representations formed earlier in the stack, reducing information dilution without quadratic-depth costs.
- Design decisions:
  - Reuse the sequence attention query projection for depth attention (no separate depth-query projection) to keep parameter cost low, especially under Grouped Query Attention (GQA).
  - Optionally include FFN-derived depth KV entries (project FFN inputs to KV) to capture depth information beyond attention-layer outputs. Experiments show FFN-side KV helps.

Asymptotic complexity and comparison:
- Depth-dense (concatenation of all layers) has quadratic growth in depth and width: impractical for large L.
- Depth-attention (attending to concatenated historical per-position states) reduces parameters/compute to O(LD^2) / O(TL2D) terms but still adds cost.
- MoDA further reduces parameter complexity (reusing query projections) to O(LD^2/G) with compute and cache scaling that remain practical (linear-in-width behavior) for typical transformer settings with GQA.

Hardware-aware implementation (critical contribution):
- A naïve implementation causes non-contiguous memory access to depth KV and poor GPU utilization. The authors engineer a fused, flash-compatible kernel for MoDA with three main optimizations:
  1) Flash-compatible depth-KV layout: flatten depth KV per token so the L depth states for each sequence position are contiguous; this makes depth reads contiguous and compatible with FlashAttention-style kernels.
  2) Chunk-aware depth-KV layout: group queries into chunks of length C and pack the corresponding local depth-KV region (C×L) so each chunk only scans a small local depth span rather than the global T×L axis; improves depth utilization from 1/T to 1/C.
  3) Group-aware indexing (exploiting GQA): G adjacent query rows share the same base-time index and can reuse the same depth KV blocks, further reducing the effective depth span to (C/G)×L and increasing utilization to G/C.
- Fused online-softmax accumulator: sequence and depth logits are streamed into a shared online-softmax state on-chip, avoiding intermediate materialization and enabling a single normalization step.
- Efficiency results: the fused kernel reaches high practical efficiency (reported as 97.3% of FlashAttention-2 efficiency at a 64K sequence length in the abstract). Controlled experiments show predictable scaling: MoDA has modest extra overhead that diminishes as sequence length or G increases; kernel ablations show the three optimizations together lead to large speedups over naive PyTorch (e.g., 1458× in a fixed setting vs. naive) and bring MoDA runtime close to FlashAttention-2.

Experiments and empirical findings:
- Training setup: decoder-only LLMs at 700M and 1.5B parameters, trained on a 400B-token OLMo2-style recipe (batch 1024, context 4096) in bf16.
- Main empirical findings:
  - MoDA yields consistent improvements in language modeling loss (perplexity) and downstream task performance across scales.
  - At 1.5B (400B tokens): average downstream improvement +2.11% across 10 tasks; validation perplexity reduced (e.g., average PPL from 13.67 to 13.47 across domains); training/C4 PPL also improved.
  - At 700M: average downstream +1.76 (Table results), validation and per-domain PPL improvements are consistent.
  - Variant ablations: (i) simply adding depth KV by reusing attention-side sequence KV yields notable gains at negligible cost; (ii) adding FFN-side KV projections further improves accuracy with moderate overhead; (iii) adding separate extra attention-side depth projections gives marginal gains while increasing parameters — near saturation.
  - MoDA is compatible with post-layernorm and, in deeper stacks, post-norm benefits more from depth-KV than pre-norm (authors observe post-norm + MoDA yields better optimization gains in deeper models).

Analysis and qualitative observations:
- Attention visualizations show persistent and substantial mass on depth-KV blocks (middle and late layers), indicating active retrieval of cross-layer states. Some heads distribute probability across sequence and depth slots instead of collapsing into fixed attention sinks; MoDA reduces attention-sink phenomena.
- Layer-number studies: MoDA improves validation loss in both shallow and deep models; gains are larger in post-norm deep models; FFN-KV additions help further.
- Kernel ablation: flash-compatible layout already orders-of-magnitude speeds up naïve code; chunk-aware and group-aware steps are each critical to reach near-FlashAttention efficiency.

Costs and limitations discussed by authors:
- Memory/bandwidth: caching depth KV from all preceding layers grows linearly with depth and can become a bottleneck at industrial scale. The paper suggests bounded depth-KV slot buffers (fixed S slots) with policies (recency, top-scoring, hybrid) to control memory.
- Engineering: while the current Triton-based fused kernel is efficient, additional CUDA and distributed-engineering is needed for trillion-parameter production runs (memory scheduling, pipelining, overlap with communication).

Practical implications and potential impact:
- MoDA is a practical, parameter-efficient primitive to help scale model depth by enabling adaptive, data-dependent retrieval from earlier layers without the quadratic costs of dense cross-layer connections.
- It provides a way to preserve and reuse informative shallow-layer features that would otherwise be diluted, potentially improving sample efficiency and final model quality when increasing depth instead of only width or data.
- The fused attention+depth engine is designed to be compatible with long-context training; thus MoDA fits modern long-context LLM training stacks.
- Because MoDA is architecture-agnostic, it could be applied in multimodal transformers, vision transformers, and world models where cross-layer state retrieval might be beneficial.

Key numerical highlights (selected):
- Hardware/fusion: fused MoDA reaches 97.3% of FlashAttention-2 efficiency at 64K sequence length (reported in abstract).
- Compute overhead: small; abstract cites a 3.7% FLOPs overhead for reported setups.
- Downstream gains: +2.11% average at 1.5B over a strong open-source baseline (OLMo2) on 10 tasks; +1.76 at 700M.
- Perplexity improvements: average validation PPL reductions (e.g., 1.5B average PPL 13.67 -> 13.47).
- Kernel ablation: flash-compatible layout reduces runtime from 2128.9 ms (naïve) to 13.102 ms; chunk-aware reduces to 6.286 ms; adding group-aware indexing reduces to 1.460 ms in the reported setting.

Conclusions and future directions:
- MoDA successfully integrates depth-history retrieval with sequence attention in a unified softmax, giving robust gains in modeling quality with modest overhead and a hardware-aware implementation suitable for long-context training.
- Future work: (1) industrial-scale CUDA/C++ kernels and distributed optimizations for trillion-parameter training; (2) bounded depth-slot caching and learned selection policies to control memory in very deep models; (3) deeper study of how depth attention changes emergent attention patterns and whether it can be combined with other depth-scaling approaches (e.g., adaptive routing, mixture-of-experts) or sparsity.

Overall assessment:
- The paper proposes a clear, well-motivated architectural primitive (MoDA) addressing a concrete problem (information dilution with depth) and backs it with algorithmic complexity analysis, practical fused-kernel engineering, and thorough empirical validation on language-model scales and benchmarks. The combined algorithm+systems approach makes the idea actionable for realistic LLM training and suggests an appealing new direction for depth scaling in transformer-based models.
