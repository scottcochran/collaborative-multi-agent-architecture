# An Multi Agent Collaboration Architecture

# Components
1. Open Policy Agent
2. Kafka
3. NodeJS BFF
4. React UI
5. Paxos Policy Definitions in REGO
6. Anthropic Claude AI Agent

# Theory of Operation

The Paxos procedures for achieving quorum among agents are defined in REGO policy files served by OPA.

Messages among agents are exchanged via a kafka topic:

`agent_quorum`

Agents collaborate by joining a quorum by exchanging messages in the quorum topic following the Paxos procedures defined in the REGO policy files.

The agent LLMs have access to the following:

1. Paxos policies in REGO.
2. All messages in the quorum topic.

The agent control logic enforces the following:

1. UUID selection
2. Message schema conformance
3. Paxos policy evaluation
4. Skill access
5. Tool access
6. MCP access



