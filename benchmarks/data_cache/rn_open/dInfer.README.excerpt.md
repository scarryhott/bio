<div align="center">
  <img src="assets/logo.svg" width="40%" alt="dInfer" />
</div>

<h4 align="center">

[![License: MIT](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![HuggingFace: Models](https://img.shields.io/badge/HuggingFace-Models-yellow)](https://huggingface.co/inclusionAI/LLaDA-MoE-7B-A1B-Instruct)
[![Technical Report: Arxiv](https://img.shields.io/badge/Technical%20Report-Arxiv-red)](https://arxiv.org/abs/2510.08666)

<!-- [![arXiv][arxiv-image]][arxiv-url] -->

</h4>

## Introduction
dInfer is an efficient and extensible inference framework for dLLMs. As illustrated in the following architecture, it modularizes inference into four components:
*model*, *diffusion iteration manager*, *decoder* and *KV-cache manager*. It provides well-designed APIs for
flexible algorithms combinations in each component. Now supports batched inference for improved throughput.

<p align="center">
  <img src="assets/Framework2.png" alt="dInfer v0.1 architecture" width="600">
  <br>
  <b>Figure</b>: Overall Architecture of dInfer
</p>

dInfer supports multiple dLLM variants, including LLaDA and LLaDA-MoE.

**Algorithmic improvements:**
- Soft diffusion iteration for smoother denoising
- Hierarchical and credit decoding for enhanced parallel decoding
- Vicinity refresh strategy for KV-cache management to mitigate cache staleness

**System-level optimizations:**
- Tensor Parallelism (TP) and Expert Parallelism (EP) to maximize GPU utilization across batch sizes
- Dynamic batching support for improved throughput on multi-request workloads
- PyTorch compilation and NVIDIA CUDA Graphs for efficient kernel execution
- Loop unrolling mechanism to eliminate CUDA stream bubbles across diffusion iterations

## Contents
- [Supported Models](#supported-models)
- [Benchmark Results](#benchmark-results)
- [Getting Started](#getting-started)

## Supported Models

dInfer supports multiple diffusion language model variants with different architectures and sizes. Below are the HuggingFace model links and their corresponding implementation files:

### LLaDA2.0
**Implementation**: [modeling_llada2_moe.py](python/dinfer/model/modeling_llada2_moe.py)

| Model | Size | HuggingFace Link | Description |
|-------|------|------------------|-------------|
| LLaDA2.0-mini-preview | 16B | [inclusionAI/LLaDA2.0-mini-preview](https://huggingface.co/inclusionAI/LLaDA2.0-mini-preview) | MoE dLLM focused on efficient reasoning and tool use |
| LLaDA2.0-flash-preview | 100B | [inclusionAI/LLaDA2.0-flash-preview](https://huggingface.co/inclusionAI/LLaDA2.0-flash-preview) | Large MoE dLLM targeting advanced code/math reasoning |

**Features**:
- Trained using Block Diffusion to improve throughput and stability
- Supports tool calling and complex agent-based task execution
- Excels at complex mathematical reasoning and code generation
- Supports both Expert Parallelism (EP) and Tensor Parallelism (TP)
- **Decoding algorithms**: Hierarchical, Credit, Threshold

### LLaDA-MoE Models (Mixture-of-Experts)

**Implementation**: [modeling_fused_olmoe.py](python/dinfer/model/modeling_fused_olmoe.py)

| Model | Size | HuggingFace Link | Description |
|-------|------|------------------|-------------|
| LLaDA-MoE-7B-A1B-Base | 7B | [inclusionAI/LLaDA-MoE-7B-A1B-Base](https://huggingface.co/inclusionAI/LLaDA-MoE-7B-A1B-Base) | Pretrained MoE dLLM |
| LLaDA-MoE-7B-A1B-Instruct | 7B | [inclusionAI/LLaDA-MoE-7B-A1B-Instruct](https://huggingface.co/inclusionAI/LLaDA-MoE-7B-A1B-Instruct) | Instruction-tuned MoE variant |

**Features**:
- Sparse Mixture-of-Experts with 64 experts
- FusedMoE optimization for efficient inference
- Support both Expert Parallelism (EP) and Tensor Parallelism (TP)
- **Decoding algorithms**: Hierarchical, Credit, Threshold

### LLaDA Models (Dense)

**Implementation**: [modeling_llada.py](python/dinfer/model/modeling_llada.py)

| Model | Size | HuggingFace Link | Description |
|-------|------|------------------|-------------|
| LLaDA-8B-B
…
