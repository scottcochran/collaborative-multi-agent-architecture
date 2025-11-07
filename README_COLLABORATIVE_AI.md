# Collaborative AI

"This document contains architecture notes and component ideas for a collaborative AI system. It is organized into high-level principles, policy and consensus components, messaging infrastructure, deployment hints, and observability considerations."

## Principles

- AI-First model
    - Let AI replace hard-coded business logic where safe and appropriate
    - Policy-aware behavior (policies govern allowed actions)

## Declarative Policy

- Edge-map definition of state flow (JSON)
- Pre-generate adjacency maps for state transitions
- REGO policy definitions for fine-grained rules
- Distributed policy evaluation & enforcement (OPA WASM)
    - AI
    - Agent control logic
    - Consensus layer
    - Tooling

## Consensus (Paxos)

- Support for leaderless, multi-leader, and Byzantine-tolerant modes
- Consensus behavior and constraints described as REGO policies

## Communication (Kafka topics)

- Quorum topic(s)
- Agent topics
- Task topic(s)
- Audit topic(s)

## Deployment

### Docker

- agent-network

### Helm charts

- Kafka
- OPA
- Agent(s)

### MCP

- Kafka
- OPA

## Agent components

- Claude (or other LLM) agent runtime
- API key management
- Kafka producer / consumer
- OPA API client
- OPA WASM-based enforcement (optional)
- Python-based policy enforcement hooks
- LLM policy awareness and guardrails
- "Earmuffs" / strict limiting controls for risky operations
- Evaluation hooks (Evals)
- Quorum awareness
    - Python-side quorum logic
    - LLM-side quorum awareness
- Channels
    - Quorum(s)
    - Main input
    - Chain-of-thought (CoT)
    - Audit

## OPA (Open Policy Agent)

- Paxos / consensus policy definitions
    - Quorum requirements
    - Quorum evolution rules
    - Task lifecycle constraints
    - Tool usage constraints
    - Topic naming and mapping rules
- Schema requirements: JSON for policy inputs and state

## Kafka topic recommendations

- Quorum topic: permanent (e.g., 30-day retention/rotation)
- Agent topics: permanent (e.g., 7-day retention)
    - main
    - audit
    - cot (chain-of-thought)
    - context
    - memory
- Task topic: short-lived (e.g., 24-hour deletion)
- Enable auto topic creation where appropriate (with governance)

## Observability

- Grafana for dashboards and visualization
- OpenTelemetry for distributed tracing and metrics

## Misc / Notes

- Consider Node.js components where ecosystem fits
- Chat and admin interfaces (TBD)

Repository reference:

https://github.com/Japan-AISI/aisev