# Talk to Your Money Monorepo

This repository is organized as a monorepo to support modular development across backend, frontend, infrastructure, and documentation components.

## Directory Structure

- `backend/` — Main backend application (FastAPI, Firebase integration, etc.)
  - `auth/` — Authentication and user management
  - `agents/` — AI agents and related logic
  - `apis/` — API endpoints and integrations
  - (add more backend components as needed)
- `frontend/` — React/TypeScript frontend (see `frontend/README.md` for details)
- `infrastructure/` — Infrastructure as code (Terraform, scripts, etc.)
- `docs/` — Project documentation, architecture diagrams, and PRDs
- `fi-mcp-dev/` — Prototype/mock MCP server for development and testing (not part of production backend)
- `test/` — Test harnesses, integration tests, and experimental agents

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd talk_to_your_money
   ```
2. **Install dependencies:**
   - Backend: See `backend/README.md` (to be created)
   - Frontend: See `frontend/README.md`
   - Infrastructure: See `infrastructure/` for Terraform and scripts
3. **Directory Conventions:**
   - All new backend code should go in `backend/` (not `fi-mcp-dev/`)
   - Use subdirectories for logical separation (e.g., `auth/`, `agents/`, `apis/`)
   - Place all infrastructure code in `infrastructure/`
   - Place all documentation in `docs/`

## Notes

- `fi-mcp-dev/` is a development/prototyping server and is not the production backend.
- Please update this README as the project evolves.
