# Da Agent API Server

A FastAPI-based HTTP server that provides REST API access to the Da Agent functionality.

## Quick Start

### Foreground Mode
```bash
python da/api/server.py
```

### Daemon Mode
```bash
# Start the server in background
python da/api/server.py --daemon

# Check server status
python da/api/server.py --action status

# Stop the server
python da/api/server.py --action stop

# Restart the server
python da/api/server.py --action restart
```

## Configuration

### Basic Options
```bash
python da/api/server.py \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

### Agent Configuration
```bash
python da/api/server.py \
  --datasource your_datasource \
  --config conf/agent.yml \
  --max_steps 20 \
  --workflow fixed
```

### Daemon Options
```bash
python da/api/server.py \
  --daemon \
  --pid-file /custom/path/server.pid \
  --daemon-log-file /custom/path/server.log
```

## Default Paths

- **API Endpoint**: `http://localhost:8000`
- **PID File**: `~/.da/run/da-agent-api.pid`
- **Log File**: `logs/da-agent-api.log`

## API Endpoints

Once the server is running, you can access:

- **Interactive Docs**: `http://localhost:8000/docs`
- **Health Check**: `GET /health`
- **Authentication**: `POST /auth/token`
- **Workflow Execution**: `POST /workflows/run`
- **Feedback Recording**: `POST /workflows/feedback`

## Usage Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Access Token
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=your_id&client_secret=your_secret"
```

### Run Workflow (Synchronous)
```bash
curl -X POST "http://localhost:8000/workflows/run" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find all users from database",
    "datasource": "your_datasource",
    "workflow": "workflow_name",
    "mode": "sync"
  }'
```

### Run Workflow (Streaming)
```bash
curl -X POST "http://localhost:8000/workflows/run" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "task": "Find all users from database",
    "datasource": "your_datasource",
    "workflow": "workflow_name",
    "mode": "async"
  }'
```

### Record Feedback
```bash
curl -X POST "http://localhost:8000/workflows/feedback" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "your_task_id",
    "status": "success"
  }'
```

## Development Mode

For development with auto-reload:
```bash
python da/api/server.py --reload
```

Note: `--daemon` and `--reload` are mutually exclusive.

## Troubleshooting

### Check if server is running
```bash
python da/api/server.py --action status
```

### View logs
```bash
tail -f logs/da-agent-api.log
```

### Force stop
```bash
pkill -f "da/api/server.py"
```