# Practical Guide to Prompt Selection in Customer Support

## Executive Summary

This guide provides evidence-based recommendations for selecting prompt engineering strategies based on benchmark empirical findings across 50 golden customer support test cases.

---

## Benchmarked Prompt Strategies Comparison

| Strategy | Benchmark Score | Format Compliance | Average Latency | Best Use Case |
|---|---|---|---|---|
| **v1.0 Zero-Shot Baseline** | 83.28% | 100.0% | ~340ms | Quick informal queries, non-critical FAQs |
| **v1.1 Few-Shot Specialist** | **99.36%** | **100.0%** | **~420ms** | **Core support workflows, policy enforcement (WINNER)** |
| **v1.2 Chain-of-Thought (CoT)** | 94.88% | 100.0% | ~890ms | Complex multi-step technical troubleshooting, de-escalation |
| **v1.3 Structured Template** | 94.72% | 100.0% | ~510ms | Automated API consumption, ticket routing pipelines |

---

## When to Use Which Strategy

### 1. Zero-Shot (`v1.0`)
- **When to use**: Simple, high-speed intent matching where latency is paramount and risks are low.
- **When NOT to use**: Hostile inputs, out-of-scope requests, or security boundaries (Zero-Shot suffered boundary failures on out-of-scope guardrails).

### 2. Few-Shot (`v1.1`)
- **When to use**: Daily customer support operations. Provides the optimal balance of highest accuracy (99.36%), 100% format compliance, and low latency (~420ms).
- **Key benefit**: Concrete exemplars prevent instruction drift and hallucination without doubling token costs.

### 3. Chain-of-Thought (`v1.2`)
- **When to use**: High-stakes de-escalations, billing disputes, and technical troubleshooting requiring step-by-step reasoning.
- **Trade-off**: Higher latency (~890ms) and token consumption. Note: Performs slightly below Few-Shot on standard support tasks.

### 4. Structured JSON Template (`v1.3`)
- **When to use**: Backend automated pipelines, programmatic routing, and CRM webhooks.
- **Best Practice**: Always pair structured JSON prompts with schema validation filters or native API JSON mode.

---

## Key Parameters Guide

- **Temperature**:
  - `0.0 - 0.2`: Recommended for support responses, billing, and policy enforcement (ensures consistency).
  - `0.5 - 0.7`: Useful for creative marketing copy (do NOT use for technical customer support).
- **Max Output Tokens**: Set cap at `500` tokens for customer responses to prevent verbose rambling.

---

## Uncomfortable Truth Finding

> Empirical benchmark data proves that elaborate Chain-of-Thought prompts do NOT always justify their cost and latency. For standard support inquiries, a clean **Few-Shot prompt (`v1.1`)** performed 4.48% higher than CoT (99.36% vs 94.88%) while executing in half the time (~420ms vs ~890ms). Measure before engineering!
