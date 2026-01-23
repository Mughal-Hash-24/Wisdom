import sys
import os
import shutil
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

# --- 🚨 SAFE IMPORTS 🚨 ---
try:
    from mcp.server.models import InitializationOptions
    import mcp.types as types
    from mcp.server import Server, NotificationOptions
    from mcp.server.stdio import stdio_server
except ImportError:
    # If this fails, it writes a log so you know why
    with open("D:\\WISDOM\\crash_log.txt", "w") as f:
        f.write("CRASH: Missing 'mcp' library. Run: pip install mcp")
    sys.exit(1)

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
# Verified path from your screenshot
VAULT_ROOT = Path(r"D:\WISDOM\WISDOM")
SERVER_NAME = "wisdom-os"


async def run():
    server = Server(SERVER_NAME)

    # ==========================================
    # 🛠️ TOOL DEFINITIONS
    # ==========================================

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            # --- 📂 EXPLORATION & SEARCH ---
            types.Tool(
                name="list_files",
                description="Lists all files in a specific folder (e.g., '20_CS_Core').",
                inputSchema={
                    "type": "object",
                    "properties": {"folder": {"type": "string", "description": "Relative path from vault root"}},
                },
            ),
            types.Tool(
                name="search_vault",
                description="Searches the CONTENT of all notes for a keyword (Semantic-like search).",
                inputSchema={
                    "type": "object",
                    "properties": {"query": {"type": "string", "description": "The exact text to look for"}},
                    "required": ["query"]
                },
            ),
            types.Tool(
                name="read_note",
                description="Reads the full content of a specific note.",
                inputSchema={
                    "type": "object",
                    "properties": {"path": {"type": "string", "description": "Filename or relative path"}},
                    "required": ["path"]
                },
            ),

            # --- 📝 WRITING & EDITING ---
            types.Tool(
                name="create_note",
                description="Creates a NEW note. If folder is not specified, Gemini decides the best PARA location.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "content": {"type": "string"},
                        "folder": {"type": "string", "description": "Optional: e.g. '10_University/Semester_2'"}
                    },
                    "required": ["topic"]
                },
            ),
            types.Tool(
                name="append_to_note",
                description="Adds text to the END of an existing note. (Great for study logs).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Just the name (e.g. 'Python_Intro')"},
                        "content": {"type": "string"}
                    },
                    "required": ["filename", "content"]
                },
            ),

            # --- 🎓 UNIVERSITY WORKFLOW ---
            types.Tool(
                name="graduate_concept",
                description="Moves a note from 'Inbox' or 'University' to 'CS_Core' (Refactoring).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "destination_subfolder": {"type": "string", "description": "e.g., 'Theory/Algorithms'"}
                    },
                    "required": ["filename", "destination_subfolder"]
                },
            ),

            # --- 🚀 PROJECT MANAGEMENT ---
            types.Tool(
                name="init_project",
                description="Creates a new project folder in '40_Projects' with a template.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "status": {"type": "string", "enum": ["Active", "Backlog"], "default": "Active"}
                    },
                    "required": ["name"]
                },
            ),

            # --- 📅 DAILY PLANNER ---
            types.Tool(
                name="daily_log",
                description="Logs a task or thought to TODAY's daily note.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entry": {"type": "string"},
                        "is_task": {"type": "boolean", "default": False}
                    },
                    "required": ["entry"]
                },
            ),
            types.Tool(
                name="get_daily_plan",
                description="Reads today's daily note (tasks and schedule).",
                inputSchema={
                    "type": "object",
                    "properties": {"offset": {"type": "integer", "description": "0=Today, 1=Tomorrow", "default": 0}},
                },
            ),
        ]

    # ==========================================
    # ⚡ TOOL LOGIC
    # ==========================================

    @server.call_tool()
    async def handle_call_tool(
            name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:

        # --- 📂 FILES ---
        if name == "list_files":
            folder = arguments.get("folder", "")
            target = VAULT_ROOT / folder
            if not target.exists(): return [types.TextContent(type="text", text=f"❌ Folder '{folder}' not found.")]

            items = [f"{'📁' if i.is_dir() else '📄'} {i.name}" for i in target.iterdir() if not i.name.startswith(".")]
            return [types.TextContent(type="text", text="\n".join(items))]

        elif name == "search_vault":
            query = arguments.get("query", "").lower()
            results = []
            # Scans every .md file in the vault
            for p in VAULT_ROOT.rglob("*.md"):
                try:
                    if query in p.read_text(encoding="utf-8").lower():
                        results.append(str(p.relative_to(VAULT_ROOT)))
                except:
                    continue

            if not results: return [types.TextContent(type="text", text=f"No notes found containing '{query}'.")]
            return [types.TextContent(type="text", text="Found matches in:\n" + "\n".join(results[:15]))]

        elif name == "read_note":
            path_str = arguments.get("path")
            target = VAULT_ROOT / path_str
            # Intelligent fallback: If path doesn't exist, try finding the filename
            if not target.exists():
                for p in VAULT_ROOT.rglob(f"*{path_str}*"):
                    if p.suffix == ".md": target = p; break

            if not target or not target.exists(): return [types.TextContent(type="text", text="❌ Note not found.")]
            return [types.TextContent(type="text", text=target.read_text(encoding="utf-8"))]

        # --- 📝 EDITING ---
        elif name == "create_note":
            topic = arguments.get("topic")
            content = arguments.get("content", "")
            folder = arguments.get("folder")

            # Smart Placement Logic
            if folder:
                final_path = VAULT_ROOT / folder / f"{topic}.md"
            else:
                final_path = VAULT_ROOT / "00_Inbox" / f"{topic}.md"

            final_path.parent.mkdir(parents=True, exist_ok=True)
            final_path.write_text(f"# {topic}\nCreated: {datetime.now()}\n\n{content}", encoding="utf-8")
            return [types.TextContent(type="text", text=f"✅ Created: {final_path}")]

        elif name == "append_to_note":
            filename = arguments.get("filename")
            content = arguments.get("content")

            # Find the file anywhere in the vault
            target = None
            for p in VAULT_ROOT.rglob(f"{filename}*"):
                if p.suffix == ".md": target = p; break

            if not target: return [types.TextContent(type="text", text=f"❌ Could not find note '{filename}'")]

            with open(target, "a", encoding="utf-8") as f:
                f.write(f"\n\n{content}")
            return [types.TextContent(type="text", text=f"📝 Appended to {target.name}")]

        # --- 🎓 UNIVERSITY ---
        elif name == "graduate_concept":
            filename = arguments.get("filename")
            dest_sub = arguments.get("destination_subfolder")

            # Find source in Inbox or University
            src = None
            for folder in [VAULT_ROOT / "00_Inbox", VAULT_ROOT / "10_University"]:
                for p in folder.rglob(f"{filename}*"):
                    if p.is_file(): src = p; break
                if src: break

            if not src: return [
                types.TextContent(type="text", text=f"❌ '{filename}' not found in Inbox or University.")]

            dest = VAULT_ROOT / "20_CS_Core" / dest_sub / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dest)
            return [types.TextContent(type="text", text=f"🎓 Graduated '{src.name}' to CS_Core/{dest_sub}")]

        # --- 🚀 PROJECTS ---
        elif name == "init_project":
            name = arguments.get("name")
            status = arguments.get("status")
            safe_name = name.replace(" ", "_")
            path = VAULT_ROOT / "40_Projects" / status / safe_name
            path.mkdir(parents=True, exist_ok=True)

            (path / f"{safe_name}.md").write_text(f"# {name}\n#project/{status}\n\n## Goals\n- [ ] ", encoding="utf-8")
            return [types.TextContent(type="text", text=f"🚀 Project initialized: {safe_name}")]

        # --- 📅 DAILY ---
        elif name == "daily_log":
            entry = arguments.get("entry")
            is_task = arguments.get("is_task")

            date_str = datetime.now().strftime("%Y-%m-%d")
            path = VAULT_ROOT / "60_Planner" / "Daily" / f"{date_str}.md"
            path.parent.mkdir(parents=True, exist_ok=True)

            if not path.exists():
                path.write_text(f"# Daily Note: {date_str}\n\n## Log\n", encoding="utf-8")

            prefix = "- [ ]" if is_task else "-"
            timestamp = datetime.now().strftime("%H:%M")
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n{prefix} {entry} ({timestamp})")
            return [types.TextContent(type="text", text=f"📅 Logged to {date_str}")]

        elif name == "get_daily_plan":
            offset = arguments.get("offset", 0)
            date_str = (datetime.now() + timedelta(days=offset)).strftime("%Y-%m-%d")
            path = VAULT_ROOT / "60_Planner" / "Daily" / f"{date_str}.md"

            if not path.exists(): return [types.TextContent(type="text", text=f"No daily note found for {date_str}")]
            return [types.TextContent(type="text", text=path.read_text(encoding="utf-8"))]

        raise ValueError(f"Unknown tool: {name}")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())