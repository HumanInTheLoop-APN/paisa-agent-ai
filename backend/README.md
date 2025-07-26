# Talk to Your Money Backend

A FastAPI-based backend for the Talk to Your Money application with agent orchestration using Google ADK (Agent Development Kit).

## Features

- **Chat Session Management**: Create, read, update, and delete chat sessions with user distinction
- **Message Handling**: Store and retrieve messages with proper user and session ownership
- **Artifact Management**: Store generated artifacts (charts, reports, analyses) from agent interactions
- **Agent Orchestration**: Runner manager service using InMemorySessionService for agent coordination
- **Authentication**: Firebase-based authentication with proper user distinction
- **Health Checks**: Comprehensive health, readiness, and liveness endpoints

## Architecture

### Models

- `ChatSession`: Chat session with user ownership and metadata
- `Message`: Messages with role-based content and tool call support
- `Artifact`: Generated artifacts with type classification and status tracking

### Services

- `ChatSessionService`: Business logic for session management
- `MessageService`: Message handling with user/session validation
- `ArtifactService`: Artifact creation and management
- `RunnerManagerService`: Agent orchestration using InMemorySessionService

### Repositories

- `BaseRepository`: In-memory storage with common operations
- `ChatSessionRepository`: Session-specific data access
- `MessageRepository`: Message-specific data access
- `ArtifactRepository`: Artifact-specific data access

## API Endpoints

### Chat Sessions

- `POST /chat/sessions` - Create a new chat session
- `GET /chat/sessions` - Get all sessions for the current user
- `GET /chat/sessions/{session_id}` - Get a specific session
- `PUT /chat/sessions/{session_id}` - Update a session
- `DELETE /chat/sessions/{session_id}` - Delete a session
- `POST /chat/sessions/{session_id}/deactivate` - Deactivate a session
- `GET /chat/sessions/{session_id}/summary` - Get session summary

### Messages

- `POST /chat/{session_id}/messages` - Create a new message
- `GET /chat/{session_id}/messages` - Get all messages for a session
- `GET /chat/{session_id}/messages/{message_id}` - Get a specific message
- `PUT /chat/{session_id}/messages/{message_id}` - Update a message
- `DELETE /chat/{session_id}/messages/{message_id}` - Delete a message
- `POST /chat/{session_id}/chat` - Send a chat message and get AI response
- `GET /chat/{session_id}/messages/role/{role}` - Get messages by role
- `GET /chat/{session_id}/messages/{message_id}/thread` - Get conversation thread
- `GET /chat/conversation` - Get all user messages across sessions

### Artifacts

- `POST /chat/{session_id}/artifacts` - Create a new artifact
- `GET /chat/{session_id}/artifacts` - Get all artifacts for a session
- `GET /chat/{session_id}/artifacts/{artifact_id}` - Get a specific artifact
- `PUT /chat/{session_id}/artifacts/{artifact_id}` - Update an artifact
- `DELETE /chat/{session_id}/artifacts/{artifact_id}` - Delete an artifact
- `POST /chat/{session_id}/artifacts/chart` - Create a chart artifact
- `POST /chat/{session_id}/artifacts/report` - Create a report artifact
- `POST /chat/{session_id}/artifacts/analysis` - Create an analysis artifact
- `GET /chat/{session_id}/artifacts/type/{artifact_type}` - Get artifacts by type
- `GET /chat/{session_id}/artifacts/status/{status}` - Get artifacts by status
- `GET /chat/{session_id}/messages/{message_id}/artifacts` - Get message artifacts
- `PUT /chat/{session_id}/artifacts/{artifact_id}/status` - Update artifact status
- `GET /chat/artifacts` - Get all user artifacts across sessions

### Health Checks

- `GET /healthz` - Basic health check
- `GET /readiness` - Readiness check for Kubernetes
- `GET /liveness` - Liveness check for Kubernetes
- `GET /health` - Legacy health check

## Setup

### Prerequisites

- Python 3.12+
- Firebase project with service account key
- MCP server running on localhost:8080

### Installation

1. Install dependencies:

```bash
pip install -e .
```

2. Set up environment variables:

```bash
# Create .env file
FIREBASE_CRED_PATH=backend/keys/serviceAccountKey.json
GOOGLE_APPLICATION_CREDENTIALS=backend/keys/serviceAccountKey.json
```

3. Run the development server:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
pytest tests/
```

## Agent Orchestration

The backend uses Google ADK with InMemorySessionService for agent orchestration:

- **RunnerManagerService**: Manages agent runners and sessions per user
- **MCP Integration**: Connects to MCP server for tool access
- **Session Isolation**: Each user gets their own agent instance
- **Message Processing**: Handles user messages through agent system

### Agent Flow

1. User sends message via `/chat/{session_id}/chat`
2. Message is saved to backend
3. Agent processes message through MCP tools
4. Response is saved and returned to user
5. Artifacts can be created from agent interactions

## Security

- **User Distinction**: All endpoints validate user ownership
- **Session Isolation**: Messages and artifacts are scoped to sessions
- **Authentication**: Firebase-based authentication required
- **CORS**: Configured for frontend integration
- **Trusted Hosts**: Middleware for host validation

## Development

### Code Style

- Black for code formatting
- isort for import sorting
- flake8 for linting

### Testing

- pytest for unit tests
- httpx for API testing
- pytest-asyncio for async test support

## API Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json
