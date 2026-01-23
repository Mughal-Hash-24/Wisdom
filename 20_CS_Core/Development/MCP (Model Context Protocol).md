# Model Context Protocol (MCP)

**Tags:** #protocol #AI #standard #development #interoperability
**Created:** 2026-01-07

## Overview
The **Model Context Protocol (MCP)** is an open-source standard introduced by Anthropic (November 2024) designed to standardize how AI models (especially LLMs) interact with external data, tools, and systems.

It solves the "m-to-n" problem where every AI application currently needs a custom integration for every data source. MCP provides a universal interface—analogous to a **USB-C port for AI applications**—allowing them to plug into various resources without bespoke connectors.

## Core Concepts

### Purpose
* **Context Awareness:** Enables AI to access real-time data (not just training data).
* **Action Execution:** Allows AI to perform actions via tools.
* **Standardization:** Removes the need for proprietary integration code for each new tool or database.

### Architecture
The protocol follows a Client-Host-Server model, typically communicating via **JSON-RPC 2.0**.

1. **MCP Host:** The AI application or environment (e.g., Claude Desktop, an IDE, an AI Agent) that "consumes" the context.
2. **MCP Client:** The component within the Host that initiates requests.
3. **MCP Server:** The external service that exposes data or capabilities (e.g., a Google Drive server, a Postgres database server, a local file system server).

### Mechanism
* **Resources:** File-like data that can be read by clients (e.g., logs, code files).
* **Prompts:** Pre-written templates that help users employ the server's capabilities effectively.
* **Tools:** Executable functions that the model can call (e.g., "query_database", "resize_image").
* **Sampling:** Allows servers to request completions from the host model (enabling agentic workflows).

## Benefits

* **For Developers:** Write a connector once (as an MCP Server), and it works with any MCP-compliant AI application (Claude, generic agents, IDEs).
* **For Users:** AI assistants become significantly more capable, able to interact with personal data (Calendar, Notion, Local Files) securely and efficiently.
* **Ecosystem:** Major adoption by players like OpenAI and Google DeepMind supports its status as an industry standard.

## Resources
* [Official Documentation](https://modelcontextprotocol.io)
* SDKs available for: Python, TypeScript, Java, C#.
