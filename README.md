# Agentic AI System for Distributed NL-to-SQL

A multi-agent system that translates natural language queries into SQL using distributed gRPC communication and a Gradio interface.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![gRPC](https://img.shields.io/badge/gRPC-244c5a?style=flat-square&logo=google&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=flat-square&logo=gradio&logoColor=white)

## Overview

This system uses two collaborative agents communicating over gRPC to process natural language input and generate executable SQL queries. A Gradio UI provides an accessible interface for submitting queries and viewing results.

## Architecture

- `agent1_server.py` - primary agent that receives NL queries and orchestrates SQL generation
- `agent2_server-1.py` - secondary agent handling query refinement and validation
- `nl2sql_gradio_ui.py` - Gradio web interface for submitting queries
- `nl2sql.proto` - Protocol Buffer definitions for gRPC service communication
- `nl2sql_pb2.py` - auto-generated protobuf message classes
- `nl2sql_pb2_grpc.py` - auto-generated gRPC service stubs

## Getting Started

### Prerequisites

- Python 3.9+
- gRPC and protobuf libraries

### Installation

```bash
pip install grpcio grpcio-tools gradio
```

### Run

```bash
# Terminal 1 - Start Agent 1
python agent1_server.py

# Terminal 2 - Start Agent 2
python agent2_server-1.py

# Terminal 3 - Launch UI
python nl2sql_gradio_ui.py
```

## License

MIT License
