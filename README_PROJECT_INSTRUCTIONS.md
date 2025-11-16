# Project Services Setup Instructions for macOS

This guide provides comprehensive instructions for configuring and starting all services in the project ecosystem on macOS.

## Table of Contents

- [Global Prerequisites](#global-prerequisites)
- [Network Setup](#network-setup)
- [Service Overview](#service-overview)
- [Installation Instructions](#installation-instructions)
  - [1. Kafka (kafka-docker)](#1-kafka-kafka-docker)
  - [2. Node BFF (node-bff)](#2-node-bff-node-bff)
  - [3. Kafka MCP HTTP Server (kakfa-mcp-http)](#3-kafka-mcp-http-server-kakfa-mcp-http)
  - [4. OPA (opa)](#4-opa-opa)
  - [5. Go Claude Agent (go-claude-agent)](#5-go-claude-agent-go-claude-agent)
  - [6. Python Claude Agent (python-claude-agent)](#6-python-claude-agent-python-claude-agent)
  - [7. TypeScript Claude Agent (typescript-claude-agent)](#7-typescript-claude-agent-typescript-claude-agent)
- [Starting All Services](#starting-all-services)
- [Service Health Checks](#service-health-checks)
- [Troubleshooting](#troubleshooting)
- [Service Dependencies](#service-dependencies)

---

## Global Prerequisites

### Required macOS Applications

Install the following applications using Homebrew:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Docker Desktop
brew install --cask docker

# Install Node.js (v18 or higher)
brew install node

# Install Go (1.22+)
brew install go

# Install Python (3.8+)
brew install python@3.14

# Install uv (Python package manager)
brew install uv

# Install Git (version control)
brew install git

# Install GitHub CLI (required for repo management)
brew install gh
```

### Docker Desktop Configuration

1. **Start Docker Desktop**:
   - Open Docker Desktop from Applications
   - Wait for Docker to start completely (whale icon in menu bar should be steady)

2. **Verify Docker is Running**:
   ```bash
   docker --version
   docker-compose --version
   docker ps
   ```

3. **Recommended Docker Desktop Settings**:
   - **Memory**: At least 4GB (8GB recommended)
   - **CPUs**: At least 2 cores (4 recommended)
   - **Disk**: At least 20GB free space

### API Keys

Several services require API keys. Set these in your shell profile (`~/.zshrc` or `~/.bash_profile`):

```bash
# Anthropic API Key (required for Claude agents)
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
```

Reload your shell:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

### Clone Repositories

Clone all project repositories using the GitHub CLI:

```bash
# Authenticate with GitHub (if not already authenticated)
gh auth login

# Clone all repositories
gh repo clone scottcochran/architecture
gh repo clone scottcochran/kafka-docker
gh repo clone scottcochran/go-claude-agent
gh repo clone scottcochran/kakfa-mcp-http
gh repo clone scottcochran/my-manim-dir
gh repo clone scottcochran/node-bff
gh repo clone scottcochran/opa
gh repo clone scottcochran/python-claude-agent
gh repo clone scottcochran/typescript-claude-agent
```

**Note**: All repositories should be cloned into the same parent directory for consistent paths.

---

## Network Setup

All Docker services communicate via a shared network called `agent-network`. This network is created automatically by docker-compose when you start the first service.

**Note**: You do NOT need to manually create the `agent-network`. The docker-compose files will create it automatically if it doesn't exist.

### Verify Network Exists

After starting your first service, you can verify the network was created:

```bash
docker network ls | grep agent-network
docker network inspect agent-network
```

---

## Service Overview

| Service | Port(s) | Description | Dependencies |
|---------|---------|-------------|--------------|
| **Kafka** | 9092, 9093 | Apache Kafka message broker (KRaft mode) | None |
| **Node BFF** | 3000, 3443 | Backend-for-Frontend with Kafka APIs | Kafka |
| **Kafka MCP HTTP** | 8123 | MCP HTTP server for Kafka operations | Kafka |
| **OPA** | 8181 | Open Policy Agent for policy enforcement | None |
| **Go Claude Agent** | N/A | Docker container running Go-based Claude agent | Anthropic API, Kafka |
| **Python Claude Agent** | N/A | Docker container running Python-based Claude agent | Anthropic API, Kafka |
| **TypeScript Claude Agent** | N/A | Docker container running TypeScript agent with MCP | Anthropic API, Kafka |

---

## Installation Instructions

### 1. Kafka (kafka-docker)

Apache Kafka message broker running in KRaft mode (no Zookeeper required).

**Location**: `kafka-docker/`

**Prerequisites**:
- Docker Desktop running

**Setup**:
```bash
cd kafka-docker
```

**Start Kafka**:
```bash
docker-compose up -d
```

**Verify**:
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f kafka

# Test connection from host
docker run --rm --network agent-network apache/kafka:3.9.0 \
  /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:19092 --list
```

**Access**:
- **From host machine**: `localhost:9092`
- **From Docker containers**: `kafka:19092`

**Stop**:
```bash
docker-compose down
```

**Clean up (removes all data)**:
```bash
docker-compose down -v
```

---

### 2. Node BFF (node-bff)

Backend-for-Frontend service with REST APIs for Kafka operations.

**Location**: `node-bff/`

**Prerequisites**:
- Docker Desktop running
- Kafka running
- `agent-network` created

**Setup**:
```bash
cd node-bff

# For local development
npm install

# Create .env file
cp .env.example .env
```

**Configure** `.env`:
```bash
PORT=3000
KAFKA_BROKERS=localhost:9092  # For local dev
# KAFKA_BROKERS=kafka:19092   # For Docker deployment
NODE_ENV=development
ENABLE_HTTPS=false
```

**Start with Docker Compose** (recommended):
```bash
docker-compose up -d
```

**Start for Local Development**:
```bash
npm run dev
```

**Verify**:
```bash
# Health check
curl http://localhost:3000/health

# Test Kafka connection
curl http://localhost:3000/api/kafka/connect

# List topics
curl http://localhost:3000/api/kafka/admin/topics
```

**Stop**:
```bash
docker-compose down
```

---

### 3. Kafka MCP HTTP Server (kakfa-mcp-http)

MCP HTTP server providing Kafka operations as tools for AI assistants.

**Location**: `kakfa-mcp-http/`

**Prerequisites**:
- Docker Desktop running
- Kafka running

**Setup**:
```bash
cd kakfa-mcp-http

# For local development (optional)
npm install

# Create .env file
cp .env.example .env
```

**Configure** `.env`:
```bash
# For Docker container deployment
KAFKA_BROKERS=kafka:19092

# For local development
# KAFKA_BROKERS=localhost:9092
```

**Start with Docker Compose** (recommended):
```bash
docker-compose up -d
```

**Start for Local Development** (alternative):
```bash
# Build
npm run build

# Start (default port 8123)
npm start

# Custom port
node build/index.js --port=9000
```

**Verify**:
```bash
# Health check
curl http://localhost:8123/health

# Test MCP endpoint
curl -X POST http://localhost:8123/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

**Add to Claude Desktop** (optional):
```bash
claude mcp add -s project -t http kafka-mcp-http http://localhost:8123/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream"
```

**Access**:
- **From host machine**: `localhost:8123`
- **From Docker containers**: `kafka-mcp-http:8123`

**Stop**:
```bash
docker-compose down
```

---

### 4. OPA (opa)

Open Policy Agent for policy-based decision making.

**Location**: `opa/`

**Prerequisites**:
- Docker Desktop running

**Setup**:
```bash
cd opa

# Optional: Create policies directory if it doesn't exist
mkdir -p policies
```

**Start**:
```bash
docker-compose up -d
```

**Verify**:
```bash
# Health check
curl http://localhost:8181/health

# Check version
curl http://localhost:8181/v1/version

# List policies
curl http://localhost:8181/v1/policies
```

**Load a Test Policy**:
```bash
# Upload via API
curl -X PUT http://localhost:8181/v1/policies/example \
  -H "Content-Type: text/plain" \
  -d '
package example

default allow = false

allow {
    input.user == "alice"
    input.action == "read"
}
'

# Test the policy
curl -X POST http://localhost:8181/v1/data/example/allow \
  -H "Content-Type: application/json" \
  -d '{"input": {"user": "alice", "action": "read"}}'
```

**Access**:
- **From host machine**: `localhost:8181`
- **From Docker containers**: `opa:8181`

**Stop**:
```bash
docker-compose down
```

---

### 5. Go Claude Agent (go-claude-agent)

Docker container running Go-based Claude agent with Kafka integration.

**Location**: `go-claude-agent/`

**Prerequisites**:
- Docker Desktop running
- Kafka running
- `ANTHROPIC_API_KEY` environment variable set

**Setup**:
```bash
cd go-claude-agent

# Create .env file
cp .env.example .env
```

**Configure** `.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
KAFKA_BROKERS=kafka:19092
```

**Start with Docker Compose**:
```bash
docker-compose up -d
```

**Attach to Running Container** (for interactive use):
```bash
docker attach go-claude-agent
```

**Detach from Container** (without stopping it):
Press `Ctrl+P` then `Ctrl+Q`

**View Logs**:
```bash
docker-compose logs -f go-claude-agent
```

**Stop**:
```bash
docker-compose down
```

**Alternative - Local Development**:
```bash
# Download dependencies
go mod download

# Run directly
go run chat.go
```

---

### 6. Python Claude Agent (python-claude-agent)

Docker container running Python-based Claude agent with Kafka integration.

**Location**: `python-claude-agent/`

**Prerequisites**:
- Docker Desktop running
- Kafka running
- `ANTHROPIC_API_KEY` environment variable set

**Setup**:
```bash
cd python-claude-agent

# Create .env file
cp .env.example .env
```

**Configure** `.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
KAFKA_BROKERS=kafka:19092
```

**Start with Docker Compose**:
```bash
docker-compose up -d
```

**Attach to Running Container** (for interactive use):
```bash
docker attach python-claude-agent
```

**Detach from Container** (without stopping it):
Press `Ctrl+P` then `Ctrl+Q`

**View Logs**:
```bash
docker-compose logs -f python-claude-agent
```

**Stop**:
```bash
docker-compose down
```

**Alternative - Local Development**:
```bash
# Initialize with uv
uv init
uv venv
uv pip install -r requirements.txt

# Run with uv
uv run chat.py

# Or with python
python chat.py
```

---

### 7. TypeScript Claude Agent (typescript-claude-agent)

Docker container running production TypeScript agent with MCP and Kafka support.

**Location**: `typescript-claude-agent/`

**Prerequisites**:
- Docker Desktop running
- Kafka running
- `ANTHROPIC_API_KEY` environment variable set

**Setup**:
```bash
cd typescript-claude-agent

# Create .env file
cp .env.example .env
```

**Configure** `.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
KAFKA_BROKERS=kafka:19092
```

**Start with Docker Compose**:
```bash
docker-compose up -d
```

**Attach to Running Container** (for interactive use):
```bash
docker attach typescript-claude-agent
```

**Detach from Container** (without stopping it):
Press `Ctrl+P` then `Ctrl+Q`

**View Logs**:
```bash
docker-compose logs -f typescript-claude-agent
```

**Stop**:
```bash
docker-compose down
```

**Alternative - Local Development**:

```bash
# Install dependencies
npm install

# Build
npm run build

# Run modes:
# 1. Interactive CLI (Standard)
npm run dev

# 2. Interactive CLI with MCP Tools
npm run dev:mcp

# 3. MCP Server Mode (for Claude Desktop)
npm run mcp

# 4. Run Examples
npm run examples
```

**CLI Commands** (when attached):
- `/reset` - Clear conversation history
- `/tools` - List available tools (MCP mode)
- `/exit` or `/quit` - Exit the CLI

---

## Starting All Services

### Recommended Startup Order

Start services in this order to satisfy dependencies:

```bash
# 1. Start Kafka (foundation service - creates agent-network automatically)
cd kafka-docker && docker-compose up -d && cd ..

# 2. Wait for Kafka to be ready (30 seconds)
sleep 30

# 3. Start OPA (independent service)
cd opa && docker-compose up -d && cd ..

# 4. Start Node BFF (depends on Kafka)
cd node-bff && docker-compose up -d && cd ..

# 5. Start Kafka MCP HTTP (depends on Kafka)
cd kakfa-mcp-http && docker-compose up -d && cd ..

# 6. Start Claude agents (optional, for interactive use)
cd go-claude-agent && docker-compose up -d && cd ..
cd python-claude-agent && docker-compose up -d && cd ..
cd typescript-claude-agent && docker-compose up -d && cd ..

# 7. Attach to an agent for interactive chat
docker attach typescript-claude-agent
```

**Note**: The `agent-network` is created automatically by the first docker-compose that starts. You do NOT need to create it manually.

### Automated Startup Script

Create a script `start-all.sh` in the architecture directory:

```bash
#!/bin/bash

echo "Starting all services..."

# Navigate to project root
cd "$(dirname "$0")/.."

# Start Kafka (creates agent-network automatically)
echo "Starting Kafka..."
cd kafka-docker && docker-compose up -d && cd ..

# Wait for Kafka to be ready
echo "Waiting for Kafka to start..."
sleep 30

# Start OPA
echo "Starting OPA..."
cd opa && docker-compose up -d && cd ..

# Start Node BFF
echo "Starting Node BFF..."
cd node-bff && docker-compose up -d && cd ..

# Start Kafka MCP HTTP
echo "Starting Kafka MCP HTTP..."
cd kakfa-mcp-http && docker-compose up -d && cd ..

# Start Claude agents (optional)
echo "Starting Claude agents..."
cd go-claude-agent && docker-compose up -d && cd ..
cd python-claude-agent && docker-compose up -d && cd ..
cd typescript-claude-agent && docker-compose up -d && cd ..

echo "All services started!"
echo ""
echo "To attach to an agent for interactive chat:"
echo "  docker attach typescript-claude-agent"
echo "  docker attach python-claude-agent"
echo "  docker attach go-claude-agent"
echo ""
echo "To detach without stopping: Ctrl+P then Ctrl+Q"
```

Make it executable:
```bash
chmod +x architecture/start-all.sh
```

Run it:
```bash
./architecture/start-all.sh
```

---

## Service Health Checks

### Quick Health Check Script

```bash
#!/bin/bash

echo "Checking service health..."
echo ""

echo "Kafka:"
docker ps | grep kafka || echo "  Not running"

echo ""
echo "OPA:"
curl -s http://localhost:8181/health || echo "  Not responding"

echo ""
echo "Node BFF:"
curl -s http://localhost:3000/health || echo "  Not responding"

echo ""
echo "Kafka MCP HTTP:"
curl -s http://localhost:8123/health || echo "  Not responding"

echo ""
echo "Docker Network:"
docker network inspect agent-network >/dev/null 2>&1 && echo "  agent-network exists" || echo "  agent-network missing"
```

### Individual Service Checks

**Kafka**:
```bash
docker exec kafka kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

**OPA**:
```bash
curl http://localhost:8181/health
```

**Node BFF**:
```bash
curl http://localhost:3000/health
```

**Kafka MCP HTTP**:
```bash
curl http://localhost:8123/health
```

---

## Troubleshooting

### Common Issues

#### 1. Docker Network Issues

**Problem**: Service can't connect to Kafka
```
Error: Connection refused to kafka:19092
```

**Solution**:
```bash
# Ensure agent-network exists
docker network create agent-network

# Restart the service
docker-compose down && docker-compose up -d
```

#### 2. Port Already in Use

**Problem**: Port conflict
```
Error: bind: address already in use
```

**Solution**:
```bash
# Find process using the port (e.g., 9092)
lsof -i :9092

# Kill the process
kill -9 <PID>

# Or modify port in docker-compose.yaml
```

#### 3. Kafka Not Ready

**Problem**: Services can't connect to Kafka immediately after startup

**Solution**:
```bash
# Wait for Kafka health check
docker exec kafka kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Or add a delay before starting dependent services
sleep 30
```

#### 4. ANTHROPIC_API_KEY Not Set

**Problem**: Claude agents fail with authentication error

**Solution**:
```bash
# Add to ~/.zshrc or ~/.bash_profile
export ANTHROPIC_API_KEY='your-key-here'

# Reload shell
source ~/.zshrc
```

#### 5. Node Module Issues

**Problem**: `MODULE_NOT_FOUND` errors

**Solution**:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

#### 6. Python Package Issues

**Problem**: Import errors or package not found

**Solution**:
```bash
# With uv
uv venv
uv pip install -r requirements.txt

# With pip
pip install --upgrade -r requirements.txt
```

### Viewing Logs

```bash
# Kafka
cd kafka-docker && docker-compose logs -f kafka

# OPA
cd opa && docker-compose logs -f opa

# Node BFF
cd node-bff && docker-compose logs -f node-bff

# Kafka MCP HTTP
cd kakfa-mcp-http && docker-compose logs -f kafka-mcp-http

# Claude Agents
cd go-claude-agent && docker-compose logs -f go-claude-agent
cd python-claude-agent && docker-compose logs -f python-claude-agent
cd typescript-claude-agent && docker-compose logs -f typescript-claude-agent
```

### Clean Restart

To completely reset all services:

```bash
# Stop all services (including agents)
cd typescript-claude-agent && docker-compose down && cd ..
cd python-claude-agent && docker-compose down && cd ..
cd go-claude-agent && docker-compose down && cd ..
cd kakfa-mcp-http && docker-compose down && cd ..
cd node-bff && docker-compose down && cd ..
cd opa && docker-compose down && cd ..
cd kafka-docker && docker-compose down -v && cd ..

# Remove network (optional - will be recreated automatically)
docker network rm agent-network

# Start fresh (network will be created automatically)
cd kafka-docker && docker-compose up -d && cd ..
# ... continue with other services in order
```

---

## Service Dependencies

### Dependency Graph

```
agent-network (Docker Network - Created Automatically)
    |
    ├── kafka (Independent - creates network)
    |     ├── node-bff (Depends on Kafka)
    |     ├── kakfa-mcp-http (Depends on Kafka)
    |     ├── go-claude-agent (Depends on Kafka)
    |     ├── python-claude-agent (Depends on Kafka)
    |     └── typescript-claude-agent (Depends on Kafka)
    |
    └── opa (Independent)
```

### Start Order Summary

1. **First**: `kafka` (creates agent-network automatically)
2. **Second**: `opa` (can start in parallel with Kafka)
3. **Third**: `node-bff`, `kakfa-mcp-http` (after Kafka is ready)
4. **Fourth**: Claude agents (requires Kafka, ANTHROPIC_API_KEY)

---

## Environment Variables Reference

### Global Environment Variables

```bash
# Required for all Claude agents
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

### Service-Specific .env Files

**kakfa-mcp-http/.env**:
```
KAFKA_BROKERS=localhost:9092
```

**node-bff/.env**:
```
PORT=3000
KAFKA_BROKERS=localhost:9092
NODE_ENV=development
ENABLE_HTTPS=false
```

**typescript-claude-agent/.env**:
```
ANTHROPIC_API_KEY=your_api_key_here
```

---

## Additional Resources

- **Kafka Documentation**: See `kafka-docker/DOCKER-README.md`
- **Kafka MCP HTTP**: See `kakfa-mcp-http/README.md`
- **Node BFF**: See `node-bff/README.md`
- **OPA**: See `opa/README.md`
- **TypeScript Agent MCP Setup**: See `typescript-claude-agent/MCP.md`

---

## Version Information

- **Kafka**: 3.9.0 (Apache Kafka with KRaft)
- **Node.js**: 18+ required
- **Go**: 1.22+ required
- **Python**: 3.8+ (3.14 recommended)
- **Docker Compose**: 3.8
- **OPA**: Latest

---

Last Updated: 2025-11-16
