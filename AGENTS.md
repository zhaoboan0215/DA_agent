# DA
An intelligent data analytics agent platform that connects LLMs to databases, tools, and semantic layers for automated SQL generation, multi-step reasoning, and dashboard assembly.

## Architecture
DA follows a modular agent architecture with a clear separation between core agent logic, tool integrations, LLM adapters, storage backends, and user interfaces. The agent node graph (defined in `da/agent/workflow.yml`) coordinates plan, execute, and reflect cycles, with specialized nodes for SQL generation, comparison, dashboard assembly, and feedback. A comprehensive tool ecosystem provides access to databases, semantic layers, BI tools, MCP servers, search, and skills—each with its own registry and permission layer. Multiple consumption channels are available: a Textual-based CLI/TUI, a FastAPI REST API (used by a web chatbot), and gateway adapters for Slack and Feishu. The LLM backend is abstracted through model adapters supporting Claude, Codex, and many others via LiteLLM.

```
┌─────────────────────────────────────────────────────────┐
│                   User Interfaces                       │
│  CLI (Textual)  │  Web Chatbot  │  Slack / Feishu GW   │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  Agent Core (da/agent/)                 │
│  Workflow Runner  →  Plan → Execute → Reflect          │
│  Specialized nodes: chat, compare, dashboard, feedback  │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────┬───────▼────────┬───────────────────────┐
│  LLM Models   │  Tool Layer    │  Storage Layer        │
│  (adapters)   │  - db_tools    │  - SQLite (RDB)       │
│  Claude       │  - sem. tools  │  - LanceDB (Vector)   │
│  Codex        │  - bi_tools    │  - entity stores      │
│  LiteLLM      │  - mcp_tools   │    (semantic models,  │
│               │  - search      │     reference SQL, etc)
│               │  - skills      │                       │
└───────────────┴────────────────┴───────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 External Services                       │
│  Databases (DuckDB, etc.)  │  MCP Servers  │  APIs      │
└─────────────────────────────────────────────────────────┘
```

## Directory Map
| Directory | Purpose | Key Entry Point | Consumer |
|-----------|---------|----------------|----------|
| `da/agent/` | Agentic workflow graph, nodes, and runner; implements plan/execute/reflect loops | `workflow.yml`, `workflow_runner.py`, `agent.py` | Internal core |
| `da/tools/` | Extensible tool framework: registry, permission, and implementations for DB, semantic layer, BI, MCP, search, skills | `registry/tool_registry.py`, individual tool packages | Agent nodes |
| `da/models/` | LLM abstraction and adapters (Claude, Codex, LiteLLM, etc.) | `base.py`, model-specific files | Agent, tools |
| `da/storage/` | Persistence layer: RDB (SQLite), vector (LanceDB), and domain stores (semantic models, reference SQL, documents, metrics, etc.) | `backend_holder.py`, store modules | Agent, tools, CLI/API |
| `da/schemas/` | Pydantic models for actions, agent state, messaging, and bus events | `action_bus.py`, `agent_models.py` | All components |
| `da/prompts/` | Prompt templates (Jinja2) for chat, SQL generation, planning, etc. | `prompt_manager.py`, `.j2` files | Agent nodes |
| `da/cli/` | Command-line interface built with Textual (TUI) and web components; rich display and streaming | `_cli_utils.py`, `tui/app.py`, `web/chatbot.py` | End users |
| `da/api/` | FastAPI REST API with routes, services, SSE streaming, and authentication | `main.py`, routes and services packages | Web chatbot, external apps |
| `da/gateway/` | Chat platform bridge: adapters for Slack, Feishu; richtext rendering | `main.py`, `bridge.py`, adapters | External chat platforms |
| `da/conf/` | Default providers configuration for services and model endpoints | `providers.yml` | Agent, tools |
| `benchmark/` | Evaluation datasets, scripts for benchmark generation and execution (SQL, multi-round) | `scripts/evaluation.py`, `gen_benchmark.py` | Evaluators, CI |
| `tests/` | Unit, integration, regression, and data files for testing | `conftest.py`, test packages | CI, developers |
| `ci/` | CI helper scripts (audit, coverage, packaging) | `post-audit-comment.js`, `audit_tests.py` | GitHub Actions |
| `build_scripts/` | Dockerfile, PyPI packaging, and dependency management | `Dockerfile`, `build_pypi_package.py` | DevOps, packaging |
| `quickstart/` | Docker Compose environments for Airflow and Superset examples | `data_engineering/airflow/docker-compose.yml` | Quick start users |
| `sample_data/` | Demo DuckDB database, CSV files, reference SQL templates | `duckdb-demo.duckdb`, `california_schools/` | Agent, tests, demos |
| `scripts/` | Utility scripts (corruption fix, debug, regression runner, recall optimization) | `run_regression.sh`, `optimize_recall/evaluate_recall.py` | Developers |

## Services
| Name | Type | Connection / Details |
|------|------|---------------------|
| demo | DuckDB (local) | `duckdb:///sample_data/duckdb-demo.duckdb` |
| airflow | Apache Airflow | `quickstart/data_engineering/airflow/docker-compose.yml` (development stack) |
| superset | Apache Superset | `quickstart/data_engineering/superset/docker-compose.yml` (development stack) |

The demo service is always available for development and testing. Airflow and Superset are optional services used by the data engineering quickstart; they can be started with `docker compose up` from their respective directories.

## Artifacts
- **Semantic models** – definitions stored in `da/storage/semantic_model` (auto‑created, synchronized) that describe database objects.
- **Reference SQL** – curated SQL examples and templates stored per subject in `da/storage/reference_sql` and used for in‑context learning.
- **Prompt templates** – versioned Jinja2 templates in `da/prompts/prompt_templates/*.j2`; consumed by the agent prompt manager.
- **Evaluation benchmarks** – datasets and success stories in `benchmark/semantic_layer/` (CSV) and generated execution results; used to measure agent performance.
- **Dashboard layouts** – input YAML files for BI dashboard assembly (e.g., `tests/data/BIDashboardInput.yaml`).
- **Sample databases** – DuckDB file and associated CSV/SQLite files in `sample_data/`; used as a local sandbox for demos and testing.
- **Configuration files** – agent workflow rules (`conf/agent.yml`, `agent.yml.example`), providers (`conf/providers.yml`), and auth clients (`conf/auth_clients.yml.example`).
- **API schemas** – OpenAPI description auto‑generated by FastAPI at runtime from the `da/api` service.
- **Python package** – `da_agent` wheel/sdist built by `build_scripts/build_pypi_package.py` and stored in `da_agent.egg-info`.