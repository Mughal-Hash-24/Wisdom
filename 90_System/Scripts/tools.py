import sys
import os
import re
import json
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
VAULT_ROOT = Path(r"D:\WISDOM\Kybernetes")
SERVER_NAME = "wisdom-os"


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def find_toc_file(folder_path: Path):
    """Finds the T.O.C file for a given folder.
    Convention: T.O.C ({folder_name}).md
    """
    folder_name = folder_path.name
    toc_path = folder_path / f"T.O.C ({folder_name}).md"
    if toc_path.exists():
        return toc_path
    for f in folder_path.iterdir():
        if f.name.startswith("T.O.C") and f.suffix == ".md":
            return f
    return None


def add_link_to_toc(toc_path: Path, note_name: str):
    """Adds a [[note_name]] wikilink to a T.O.C file if not already present."""
    stem = Path(note_name).stem
    link = f"[[{stem}]]"
    content = toc_path.read_text(encoding="utf-8")
    if link not in content:
        content = content.rstrip() + f"\n- {link}\n"
        toc_path.write_text(content, encoding="utf-8")


def remove_link_from_toc(toc_path: Path, note_name: str):
    """Removes a [[note_name]] wikilink from a T.O.C file."""
    stem = Path(note_name).stem
    content = toc_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    lines = [l for l in lines if f"[[{stem}]]" not in l and f"[[{stem}|" not in l]
    toc_path.write_text("\n".join(lines), encoding="utf-8")


def parse_frontmatter(content: str):
    """Splits a note into YAML frontmatter (as dict) and body.
    Returns (None, full_content) if no frontmatter exists.
    """
    if not content.startswith("---"):
        return None, content
    end = content.find("---", 3)
    if end == -1:
        return None, content
    fm_text = content[3:end].strip()
    body = content[end + 3:].lstrip("\n")
    fm = {}
    if "tags:" in fm_text:
        tags = re.findall(r'-\s+"?([^"\n]+)"?', fm_text)
        fm["tags"] = [t.strip() for t in tags]
    return fm, body


def build_frontmatter(tags: list) -> str:
    """Builds a YAML frontmatter string from a list of tags."""
    lines = ["---", "tags:"]
    for tag in tags:
        clean = tag.strip().strip('"')
        lines.append(f'  - {clean}')
    lines.append("---")
    return "\n".join(lines)



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
                description="Searches the CONTENT of all notes for an exact keyword match (case-insensitive substring search).",
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
                description="Creates or overwrites a note. Use 'path' for exact vault-relative placement (e.g. '00_Inbox/_expand_file_1.md'). Or use 'topic'+'folder' for auto-naming.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Exact vault-relative file path (e.g. '00_Inbox/my_note.md'). If provided, topic/folder are ignored."},
                        "topic": {"type": "string", "description": "Note title (used as filename if path not provided)."},
                        "content": {"type": "string"},
                        "folder": {"type": "string", "description": "Optional: e.g. '10_University/Semester_4'"},
                        "raw": {"type": "boolean", "description": "If true, write content exactly as-is without adding heading/timestamp."}
                    },
                    "required": ["content"]
                },
            ),
            types.Tool(
                name="rename_note",
                description="Renames a note file within the vault. Does not move between folders.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Current vault-relative path (e.g. '00_Inbox/old_name.md')"},
                        "new_name": {"type": "string", "description": "New filename only (e.g. '2.1.4 - New Title.md')"}
                    },
                    "required": ["path", "new_name"]
                },
            ),
            types.Tool(
                name="delete_note",
                description="Deletes a note file from the vault. Use for cleanup of temp files.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Vault-relative path to delete (e.g. '00_Inbox/_expand_file_1.md')"}
                    },
                    "required": ["path"]
                },
            ),
            types.Tool(
                name="move_note",
                description="Moves a note to a different folder in the vault.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Current vault-relative path (e.g. '00_Inbox/my_note.md')"},
                        "destination": {"type": "string", "description": "Destination folder (e.g. '30_Knowledge_Base/History_Culture')"}
                    },
                    "required": ["path", "destination"]
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

            # --- VAULT MANAGEMENT (v2) ---
            types.Tool(
                name="scan_inbox",
                description="Scans the 00_Inbox folder and returns structured JSON: detected topics, {{...}} prompt blocks, and whether each note needs splitting.",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="move_note",
                description="Moves a note within the vault. Automatically updates T.O.C files in both source and destination folders.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Relative source path (e.g., '00_Inbox/MyNote.md')"},
                        "destination": {"type": "string", "description": "Relative destination folder (e.g., '20_CS_Core/Theory')"}
                    },
                    "required": ["source", "destination"]
                },
            ),
            types.Tool(
                name="split_note",
                description="Splits a multi-topic note into separate files. Splits on H1 headers (# Title). Each section becomes a new file in 00_Inbox. Original is deleted.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative path to the multi-topic note"}
                    },
                    "required": ["path"]
                },
            ),
            types.Tool(
                name="ensure_toc_link",
                description="Ensures a note is linked to its parent T.O.C file. Adds uplink to the note and downlink from the T.O.C.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative path from vault root (e.g., '20_CS_Core/MyNote.md')"}
                    },
                    "required": ["path"]
                },
            ),
            types.Tool(
                name="add_frontmatter",
                description="Adds or merges YAML frontmatter tags on a vault note. Merges without duplicates.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative path from vault root"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags to add, e.g. ['#field/cs', '#subject/os']"}
                    },
                    "required": ["path", "tags"]
                },
            ),
            types.Tool(
                name="load_template",
                description="Returns the content of an expansion template by letter (A-I). Templates are in 90_System/Templates/Expansion/.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "letter": {"type": "string", "description": "Template letter: A-I", "enum": ["A","B","C","D","E","F","G","H","I"]}
                    },
                    "required": ["letter"]
                },
            ),
            types.Tool(
                name="expand_block",
                description="Creates an expansion stub by embedding a prompt into a template structure. Writes a pre-filled file for the LLM or @expander agent to complete.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "The original {{...}} prompt text"},
                        "template_letter": {"type": "string", "description": "Template letter A-I", "enum": ["A","B","C","D","E","F","G","H","I"]},
                        "output_path": {"type": "string", "description": "Relative output path (e.g., '00_Inbox/Expansion_VirtualMemory.md')"}
                    },
                    "required": ["prompt", "template_letter", "output_path"]
                },
            ),

            # --- 📊 UTILITIES ---
            types.Tool(
                name="word_count",
                description="Returns the exact word count of a note file. Use this instead of estimating word counts -- LLM estimates are inaccurate.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Vault-relative path to the note (e.g. '00_Inbox/_expand_file_1.md')"}
                    },
                    "required": ["path"]
                },
            ),

            # --- 🔒 SCOPED AGENT TOOLS ---
            types.Tool(
                name="write_expansion",
                description="Writes expansion content to a pre-created temp file. ONLY works for _expand_ files in 00_Inbox. Domain agents use this instead of create_note.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "block_id": {"type": "string", "description": "The block identifier provided by the orchestrator (e.g. 'Artificial_Intelligence_Semester_4_3'). Maps to 00_Inbox/_expand_{block_id}.md"},
                        "content": {"type": "string", "description": "The full expansion content to write."}
                    },
                    "required": ["block_id", "content"]
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
                except Exception:
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
            path_str = arguments.get("path")
            topic = arguments.get("topic")
            content = arguments.get("content", "")
            folder = arguments.get("folder")
            raw = arguments.get("raw", False)

            # Path-based creation (preferred -- prevents double-nesting)
            if path_str:
                # Ensure .md extension
                if not path_str.endswith(".md"):
                    path_str += ".md"
                final_path = VAULT_ROOT / path_str
            elif folder:
                final_path = VAULT_ROOT / folder / f"{topic}.md"
            else:
                final_path = VAULT_ROOT / "00_Inbox" / f"{topic}.md"

            # Safety: only create the parent directory, NOT arbitrary nested dirs
            if not final_path.parent.exists():
                # Only allow creating ONE level of new directory
                if final_path.parent.parent.exists():
                    final_path.parent.mkdir(exist_ok=True)
                else:
                    return [types.TextContent(type="text", text=f"❌ Parent directory does not exist: {final_path.parent}. Will not create nested directories.")]

            # Write content
            if raw:
                final_path.write_text(content, encoding="utf-8")
            else:
                title = topic or final_path.stem
                final_path.write_text(f"# {title}\nCreated: {datetime.now()}\n\n{content}", encoding="utf-8")
            return [types.TextContent(type="text", text=f"✅ Created: {final_path.relative_to(VAULT_ROOT)}")]

        elif name == "rename_note":
            path_str = arguments.get("path")
            new_name = arguments.get("new_name")
            target = VAULT_ROOT / path_str
            if not target.exists():
                return [types.TextContent(type="text", text=f"❌ Note not found: {path_str}")]
            new_path = target.parent / new_name
            if not new_path.suffix:
                new_path = target.parent / f"{new_name}.md"
            target.rename(new_path)
            return [types.TextContent(type="text", text=f"✅ Renamed: {path_str} → {new_path.relative_to(VAULT_ROOT)}")]

        elif name == "delete_note":
            path_str = arguments.get("path")
            target = VAULT_ROOT / path_str
            if not target.exists():
                return [types.TextContent(type="text", text=f"❌ Note not found: {path_str}")]
            if not target.is_file():
                return [types.TextContent(type="text", text=f"❌ Not a file (safety): {path_str}")]
            target.unlink()
            return [types.TextContent(type="text", text=f"✅ Deleted: {path_str}")]

        elif name == "move_note":
            path_str = arguments.get("path")
            dest_folder = arguments.get("destination")
            source = VAULT_ROOT / path_str
            if not source.exists():
                return [types.TextContent(type="text", text=f"❌ Note not found: {path_str}")]
            dest_dir = VAULT_ROOT / dest_folder
            if not dest_dir.exists():
                dest_dir.mkdir(parents=False, exist_ok=True)
            dest_path = dest_dir / source.name
            shutil.move(str(source), str(dest_path))
            return [types.TextContent(type="text", text=f"✅ Moved: {path_str} → {dest_path.relative_to(VAULT_ROOT)}")]

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
            project_name = arguments.get("name")
            status = arguments.get("status")
            safe_name = project_name.replace(" ", "_")
            path = VAULT_ROOT / "40_Projects" / status / safe_name
            path.mkdir(parents=True, exist_ok=True)

            (path / f"{safe_name}.md").write_text(f"# {project_name}\n#project/{status}\n\n## Goals\n- [ ] ", encoding="utf-8")
            return [types.TextContent(type="text", text=f"Project initialized: {safe_name}")]

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

        # ==========================================
        # v2 TOOL HANDLERS
        # ==========================================

        elif name == "scan_inbox":
            inbox = VAULT_ROOT / "00_Inbox"
            if not inbox.exists():
                return [types.TextContent(type="text", text="00_Inbox folder not found.")]
            results = []
            for f in sorted(inbox.iterdir()):
                if f.suffix != ".md" or f.name.startswith("T.O.C"):
                    continue
                content = f.read_text(encoding="utf-8")
                prompts = re.findall(r'\{\{(.+?)\}\}', content, re.DOTALL)
                headers = re.findall(r'^# (?!#)(.+)$', content, re.MULTILINE)
                topics = [h for h in headers if not h.startswith("Created")]
                results.append({
                    "filename": f.name,
                    "path": str(f.relative_to(VAULT_ROOT)),
                    "topics": topics,
                    "prompt_blocks": prompts,
                    "needs_split": len(topics) > 1
                })
            if not results:
                return [types.TextContent(type="text", text="Inbox is empty.")]
            return [types.TextContent(type="text", text=json.dumps(results, indent=2))]

        elif name == "move_note":
            source_str = arguments.get("source")
            dest_str = arguments.get("destination")
            source = VAULT_ROOT / source_str
            dest_folder = VAULT_ROOT / dest_str
            if not source.exists():
                return [types.TextContent(type="text", text=f"Source not found: {source_str}")]
            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_file = dest_folder / source.name
            src_toc = find_toc_file(source.parent)
            if src_toc:
                remove_link_from_toc(src_toc, source.name)
            shutil.move(str(source), str(dest_file))
            dst_toc = find_toc_file(dest_folder)
            if dst_toc:
                add_link_to_toc(dst_toc, dest_file.name)
            return [types.TextContent(type="text", text=f"Moved {source.name} to {dest_str}")]

        elif name == "split_note":
            path_str = arguments.get("path")
            target = VAULT_ROOT / path_str
            if not target.exists():
                return [types.TextContent(type="text", text=f"Note not found: {path_str}")]
            content = target.read_text(encoding="utf-8")
            fm_data, body = parse_frontmatter(content)
            # Preserve frontmatter block for propagation to split files
            fm_block = ""
            if fm_data is not None:
                end_idx = content.find("---", 3)
                fm_block = content[:end_idx + 3] + "\n\n"
            # Split on H1 headers only (# Title, not ## or ###)
            sections = re.split(r'^(?=# (?!#))', body, flags=re.MULTILINE)
            sections = [s.strip() for s in sections if s.strip()]
            if len(sections) <= 1:
                return [types.TextContent(type="text", text=f"Only 1 H1 section found. No split needed.")]
            new_files = []
            inbox = VAULT_ROOT / "00_Inbox"
            for i, section in enumerate(sections):
                first_line = section.split("\n")[0]
                # Check if section starts with H1; if not, it's pre-header content
                if first_line.startswith("# "):
                    title = first_line.lstrip("# ").strip()
                else:
                    title = f"Preamble_{target.stem}"
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                out_path = inbox / f"{safe_title}.md"
                # Prepend preserved frontmatter to each split file
                out_path.write_text(fm_block + section, encoding="utf-8")
                new_files.append(out_path.name)
            target.unlink()
            return [types.TextContent(type="text", text=f"Split into {len(new_files)} files: {', '.join(new_files)}")]

        elif name == "ensure_toc_link":
            path_str = arguments.get("path")
            target = VAULT_ROOT / path_str
            if not target.exists():
                return [types.TextContent(type="text", text=f"Note not found: {path_str}")]
            parent_folder = target.parent
            toc = find_toc_file(parent_folder)
            if toc is None:
                return [types.TextContent(type="text", text=f"No T.O.C file found in {parent_folder.name}")]
            content = target.read_text(encoding="utf-8")
            toc_stem = toc.stem
            folder_name = parent_folder.name
            uplink = f"[[{toc_stem}|Up to {folder_name}]]"
            if toc_stem not in content:
                fm, body = parse_frontmatter(content)
                if fm is not None:
                    fm_text = content[:content.find("---", 3) + 3]
                    new_content = fm_text + f"\n{uplink}\n\n" + body
                else:
                    new_content = f"{uplink}\n\n" + content
                target.write_text(new_content, encoding="utf-8")
            add_link_to_toc(toc, target.name)
            return [types.TextContent(type="text", text=f"T.O.C link ensured: {target.name} <-> {toc.name}")]

        elif name == "add_frontmatter":
            path_str = arguments.get("path")
            new_tags = arguments.get("tags", [])
            target = VAULT_ROOT / path_str
            if not target.exists():
                return [types.TextContent(type="text", text=f"Note not found: {path_str}")]
            content = target.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(content)
            if fm is not None and "tags" in fm:
                existing = set(fm["tags"])
                for tag in new_tags:
                    existing.add(tag.strip().strip('"'))
                all_tags = sorted(existing)
            else:
                all_tags = sorted(set(t.strip().strip('"') for t in new_tags))
            new_content = build_frontmatter(all_tags) + "\n" + body
            target.write_text(new_content, encoding="utf-8")
            return [types.TextContent(type="text", text=f"Frontmatter updated for {target.name} ({len(all_tags)} tags)")]

        elif name == "load_template":
            letter = arguments.get("letter", "").upper()
            template_map = {
                "A": "Template_A_DeepDive.md", "B": "Template_B_Arena.md",
                "C": "Template_C_RosettaStone.md", "D": "Template_D_Chronograph.md",
                "E": "Template_E_Algorithmist.md", "F": "Template_F_Debugger.md",
                "G": "Template_G_Blueprint.md", "H": "Template_H_Mathematician.md",
                "I": "Template_I_CaseStudy.md",
            }
            if letter not in template_map:
                return [types.TextContent(type="text", text=f"Unknown template letter: {letter}. Valid: A-I")]
            template_path = VAULT_ROOT / "90_System" / "Templates" / "Expansion" / template_map[letter]
            if not template_path.exists():
                return [types.TextContent(type="text", text=f"Template file not found: {template_map[letter]}")]
            tmpl_content = template_path.read_text(encoding="utf-8")
            return [types.TextContent(type="text", text=tmpl_content)]

        elif name == "expand_block":
            prompt = arguments.get("prompt")
            letter = arguments.get("template_letter", "").upper()
            output_str = arguments.get("output_path")
            template_map = {
                "A": "Template_A_DeepDive.md", "B": "Template_B_Arena.md",
                "C": "Template_C_RosettaStone.md", "D": "Template_D_Chronograph.md",
                "E": "Template_E_Algorithmist.md", "F": "Template_F_Debugger.md",
                "G": "Template_G_Blueprint.md", "H": "Template_H_Mathematician.md",
                "I": "Template_I_CaseStudy.md",
            }
            if letter not in template_map:
                return [types.TextContent(type="text", text=f"Unknown template: {letter}")]
            template_path = VAULT_ROOT / "90_System" / "Templates" / "Expansion" / template_map[letter]
            if not template_path.exists():
                return [types.TextContent(type="text", text=f"Template file missing: {template_map[letter]}")]
            tmpl_content = template_path.read_text(encoding="utf-8")
            output = VAULT_ROOT / output_str
            output.parent.mkdir(parents=True, exist_ok=True)
            stub = f'---\ntags:\n  - "#type/expansion"\n---\n\n> **Seed:** "{prompt}"\n\n---\n\n{tmpl_content}\n\n---\n*Expand the seed prompt above following the template structure.*\n'
            output.write_text(stub, encoding="utf-8")
            return [types.TextContent(type="text", text=f"Expansion stub written to {output_str}")]

        elif name == "word_count":
            path_str = arguments.get("path")
            target = VAULT_ROOT / path_str
            if not target.exists():
                return [types.TextContent(type="text", text=f"Note not found: {path_str}")]
            content = target.read_text(encoding="utf-8")
            # Strip YAML frontmatter before counting
            _, body = parse_frontmatter(content)
            words = len(body.split())
            return [types.TextContent(type="text", text=f"{words}")]

        elif name == "write_expansion":
            block_id = arguments.get("block_id", "")
            content = arguments.get("content", "")
            # Construct path: ONLY _expand_ files in 00_Inbox
            target = VAULT_ROOT / "00_Inbox" / f"_expand_{block_id}.md"
            if not target.exists():
                return [types.TextContent(type="text", text=f"❌ Target file not found: _expand_{block_id}.md. The orchestrator must pre-create this file before you can write to it.")]
            if not target.name.startswith("_expand_"):
                return [types.TextContent(type="text", text=f"❌ Security: write_expansion can only write to _expand_ prefixed files.")]
            target.write_text(content, encoding="utf-8")
            # Return word count for verification
            words = len(content.split())
            return [types.TextContent(type="text", text=f"✅ Written {words} words to _expand_{block_id}.md")]

        raise ValueError(f"Unknown tool: {name}")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())