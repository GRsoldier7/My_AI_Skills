---
name: mcp-server-builder
description: |
  Expert MCP (Model Context Protocol) server architect and builder. Use when designing,
  building, debugging, or deploying MCP servers that extend Claude Code and other AI
  tools with custom capabilities.

  EXPLICIT TRIGGER on: "MCP", "MCP server", "Model Context Protocol", "build an MCP",
  "custom tool for Claude", "extend Claude", "Claude Code tool", "MCP transport",
  "stdio server", "SSE server", "MCP resource", "MCP prompt", "tool server",
  "connect Claude to", "give Claude access to", "MCP client", "mcp.json",
  ".mcp.json", "MCP configuration", "custom MCP", "MCP TypeScript", "MCP Python".

  Also trigger when the user wants Claude to interact with an external system that
  doesn't have an existing MCP server — the answer may be to build one.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: app-security-architect, n8n-workflow-architect, ai-agentic-specialist
  last-reviewed: "2026-03-21"
  review-trigger: "MCP spec updates, new transport types, SDK version changes"
  capability-assumptions:
    - "TypeScript or Python SDK available for MCP server development"
    - "Claude Code as primary MCP client"
    - "npm/npx or pip/uvx for running servers"
  fallback-patterns:
    - "If user unfamiliar with MCP: explain concept before building"
    - "If complex integration: recommend starting with minimal viable server, iterate"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: capability need, integration requirement, or MCP server to build/debug
- Output produces: MCP server code, configuration, or architecture design
- Can chain from: ai-agentic-specialist (agent needs tool → build MCP server)
- Can chain into: app-security-architect (secure the server), docker-infrastructure (deploy it)
- Orchestrator notes: always start with the simplest server that solves the problem

---

## MCP Architecture Overview

### What MCP Servers Provide
- **Tools** — functions Claude can call (read database, call API, run script)
- **Resources** — data Claude can read (files, database records, API responses)
- **Prompts** — reusable prompt templates with parameters

### Transport Types
| Transport | Use When | How |
|-----------|----------|-----|
| **stdio** | Local development, Claude Code | Server runs as subprocess |
| **SSE** | Remote/shared servers | Server runs as HTTP service |
| **Streamable HTTP** | Modern remote deployment | Replaces SSE, bidirectional |

### Server Lifecycle
```
Client (Claude Code) → starts server process (stdio) or connects (SSE/HTTP)
  → server registers capabilities (tools, resources, prompts)
  → client calls tools / reads resources as needed
  → server processes requests and returns results
```

---

## Building an MCP Server (TypeScript)

### Minimal Server Template
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

// Define a tool
server.tool(
  "get_data",
  "Fetches data from the system",
  {
    query: z.string().describe("The search query"),
    limit: z.number().optional().default(10).describe("Max results"),
  },
  async ({ query, limit }) => {
    const results = await fetchData(query, limit);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// Define a resource
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [{ uri: uri.href, mimeType: "application/json", text: JSON.stringify(config) }],
  })
);

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Project Setup
```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init  # set "module": "node16", "outDir": "./dist"
```

### package.json Configuration
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

---

## Building an MCP Server (Python)

### Minimal Server Template
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def get_data(query: str, limit: int = 10) -> str:
    """Fetches data from the system."""
    results = await fetch_data(query, limit)
    return json.dumps(results, indent=2)

@mcp.resource("config://app")
async def get_config() -> str:
    """Returns application configuration."""
    return json.dumps(config)

if __name__ == "__main__":
    mcp.run()
```

### Project Setup
```bash
mkdir my-mcp-server && cd my-mcp-server
pip install mcp  # or: uv add mcp
```

---

## Registering with Claude Code

### In .mcp.json (project-level, committed)
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/dist/index.js"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

### In ~/.claude/settings.json (user-level)
Add to `enabledMcpjsonServers` array to auto-approve.

### Python Server Registration
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {}
    }
  }
}
```

---

## Design Patterns

### Database Connector
Expose database queries as tools — never give Claude raw SQL access:
```typescript
server.tool("query_users", "Search users by criteria", {
  email: z.string().optional(),
  role: z.enum(["admin", "user"]).optional(),
}, async ({ email, role }) => {
  // Parameterized query — never string interpolation
  const users = await db.query(
    "SELECT id, name, email FROM users WHERE ($1::text IS NULL OR email = $1) AND ($2::text IS NULL OR role = $2)",
    [email, role]
  );
  return { content: [{ type: "text", text: JSON.stringify(users) }] };
});
```

### API Wrapper
Wrap external APIs with authentication handled server-side:
```typescript
server.tool("search_tickets", "Search support tickets", {
  status: z.enum(["open", "closed", "pending"]),
  query: z.string().optional(),
}, async ({ status, query }) => {
  const response = await fetch(`${API_BASE}/tickets?status=${status}&q=${query}`, {
    headers: { Authorization: `Bearer ${process.env.API_KEY}` },
  });
  return { content: [{ type: "text", text: await response.text() }] };
});
```

### File System Scope
Provide scoped file access to specific directories:
```typescript
server.tool("read_config", "Read a config file", {
  filename: z.string(),
}, async ({ filename }) => {
  const safePath = path.resolve(CONFIG_DIR, path.basename(filename));
  if (!safePath.startsWith(CONFIG_DIR)) throw new Error("Path traversal blocked");
  const content = await fs.readFile(safePath, "utf-8");
  return { content: [{ type: "text", text: content }] };
});
```

---

## Security

- **Never expose raw database access** — wrap in parameterized query tools
- **Validate all inputs** with Zod schemas — reject malformed requests
- **Path traversal protection** — always resolve and verify paths stay within allowed directories
- **Credentials server-side** — API keys in env vars, never sent to the client
- **Least privilege** — each tool does one thing with minimum required permissions
- **Rate limiting** for resource-intensive operations
- **Audit logging** — log tool calls for debugging and security review

---

## Testing and Debugging

### Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector node dist/index.js
```
Opens a web UI to test tools interactively without Claude.

### Debug Logging
```typescript
server.tool("debug_tool", "...", {}, async () => {
  console.error("Debug: tool called");  // stderr = logs (doesn't interfere with stdio)
  return { content: [{ type: "text", text: "ok" }] };
});
```
Use `stderr` for logs — `stdout` is the MCP transport channel in stdio mode.

---

## Self-Evaluation (run before presenting output)

Before presenting an MCP server design, silently check:
[ ] Does each tool have a clear Zod/type schema for inputs?
[ ] Are credentials handled server-side, not passed through tool arguments?
[ ] Is input validation sufficient to prevent injection or path traversal?
[ ] Does the server do one domain well rather than trying to do everything?
[ ] Is the server testable with MCP Inspector before deploying?
If any check fails, revise before presenting.
