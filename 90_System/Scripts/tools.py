import sys
import os
import re
import json
import shutil
import asyncio
import threading
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
SERVER_NAME = "wisdom_os"
TOC_LOCK = threading.Lock()

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
                name="semantic_search",
                description="Queries the local Obsidian Smart Connections vector database using semantic similarity. Returns the most relevant chunks.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The concept or question to search for semantically."},
                        "k": {"type": "integer", "description": "Number of top results to return.", "default": 5}
                    },
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
                description="Writes expansion content to a pre-created temp file. ONLY works for files in 00_Inbox. Domain agents use this instead of create_note.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target_file": {"type": "string", "description": "The exact temp_file path provided by the orchestrator payload (e.g. '00_Inbox/_expand_123.md')."},
                        "content": {"type": "string", "description": "The full expansion content to write."}
                    },
                    "required": ["target_file", "content"]
                },
            ),

            # --- 🧭 ORCHESTRATION ---
            types.Tool(
                name="prepare_dispatch",
                description="Prepares everything needed to dispatch a domain agent for a single expansion block. Creates the temp file, loads the card/template content, masks other {{...}} blocks in context, and returns a structured dispatch payload. Purely mechanical.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "block_id": {"type": "string", "description": "The block_id from scan_inbox (e.g. 'Design_Patterns_OOP_1')"},
                        "source_path": {"type": "string", "description": "Vault-relative path to the source note (e.g. '00_Inbox/Design_Patterns_OOP.md')"},
                        "domain": {"type": "string", "description": "Domain agent name from @classifier (e.g. 'turing')"},
                        "card_type": {"type": "string", "enum": ["template", "card"], "description": "'template' for A-I letters, 'card' for principle cards"},
                        "card_value": {"type": "string", "description": "Template letter (A-I) or card filename without .md (e.g. 'A' or 'narrative_history')"}
                    },
                    "required": ["block_id", "source_path", "domain", "card_type", "card_value"]
                },
            ),
            types.Tool(
                name="organize_file",
                description="Organizes a file: generates Uni IDs if needed, writes YAML frontmatter tags, injects TOC uplink, inserts table rows in parent TOC, and moves the file to the final destination.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source_path": {"type": "string", "description": "Vault-relative path to stitched file"},
                        "destination_dir": {"type": "string", "description": "Vault-relative target directory"},
                        "toc_parent": {"type": "string", "description": "Target TOC filename"},
                        "category": {"type": "string", "description": "Table category under which to place the note"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Frontmatter tags"}
                    },
                    "required": ["source_path", "destination_dir", "toc_parent", "category", "tags"]
                },
            ),
            types.Tool(
                name="inject_subblocks",
                description="Phase 1 of the Two-Pass system. Takes a Planner agent's JSON output (a list of sections with titles and sub-prompts) and deterministically injects them as @expand sub-blocks into the source file. Converts the original @blueprint/@deep tag into an HTML comment to prevent re-processing, then writes one '## Title\\n{{@expand prompt}}' block per section. Returns the count of injected sub-blocks.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source_path": {"type": "string", "description": "Vault-relative path to the source note (e.g. '00_Inbox/GoF_Patterns.md')"},
                        "block_id": {"type": "string", "description": "The unique block ID (e.g. 'Philosophy_1')"},
                        "directive": {"type": "string"},
                        "prompt": {"type": "string", "description": "The exact original prompt string inside the target block"},
                        "n": {"type": "integer", "description": "The N value from @blueprint:N, or null for @deep"},
                        "sections": {
                            "type": "array",
                            "description": "Ordered list of sections from the Planner agent",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "prompt": {"type": "string"}
                                },
                                "required": ["title", "prompt"]
                            }
                        }
                    },
                    "required": ["source_path", "block_id", "directive", "sections"]
                },
            ),
            types.Tool(
                name="append_summary",
                description="Appends a 1-2 sentence summary entry to the running context summary file for a source note. Called by the orchestrator after each block is verified. The summary file is read by subsequent domain agents as lightweight cross-block context, replacing the old masked-context approach.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "summary_file": {"type": "string", "description": "Vault-relative path to the summary file (e.g. '00_Inbox/_summary_Kafka.md')"},
                        "entry": {"type": "string", "description": "1-2 sentence summary of what this block covered"}
                    },
                    "required": ["summary_file", "entry"]
                },
            ),
            types.Tool(
                name="stitch_files",
                description="Deterministic alternative to the old @surgeon agent. Replaces {{...}} blocks in the source note with the content of their corresponding expanded temp files. Expects an array of {block_id, temp_file} pairs.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source_path": {"type": "string", "description": "Vault-relative path to the source note (e.g. '00_Inbox/Concept.md')"},
                        "blocks": {
                            "type": "array",
                            "description": "List of block_ids and their temp file paths to stitch",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "block_id": {"type": "string"},
                                    "temp_file": {"type": "string"}
                                },
                                "required": ["block_id", "temp_file"]
                            }
                        }
                    },
                    "required": ["source_path", "blocks"]
                },
            ),

            # --- 🕌 FIQH PIPELINE ---
            types.Tool(
                name="prepare_fiqh_dispatch",
                description="Phase 0 of the Fiqh pipeline. Pre-creates a temp file for one madhab agent or the synthesizer, loads the selected card, and returns a structured dispatch payload. Must be called once per school before dispatching any agent.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slug": {"type": "string", "description": "URL-safe question slug, e.g. 'gold-jewelry-men'. Only lowercase letters, digits, and hyphens."},
                        "school": {"type": "string", "enum": ["hanafi", "maliki", "shafii", "hanbali", "synthesizer"], "description": "The madhab agent to prepare for, or 'synthesizer'."},
                        "card": {"type": "string", "enum": ["fiqh_ruling", "fiqh_usul_deep", "fiqh_historical", "fiqh_contemporary"], "description": "The card that narrows the agent's output framing."},
                        "question": {"type": "string", "description": "The full original question text."},
                        "query_type": {"type": "string", "enum": ["Classical", "Derived", "Mixed"], "description": "Query classification from Step 0."},
                        "madhab_temp_files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "(Synthesizer only) Vault-relative paths to the four madhab temp files. Ignored for madhab schools."
                        }
                    },
                    "required": ["slug", "school", "card", "question", "query_type"]
                },
            ),
            types.Tool(
                name="fiqh_link_and_finalize",
                description="Final step of the Fiqh pipeline. Injects frontmatter into all 5 temp files, adds cross-links, moves files to their permanent vault location, and updates T.O.C (Fiqh).md. Aborts entirely if any temp file is missing — no partial moves.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slug": {"type": "string", "description": "The question slug used throughout the pipeline."},
                        "question": {"type": "string", "description": "Original full question text. Used as the display text in T.O.C (Fiqh).md."},
                        "concept": {"type": "string", "description": "The concept/ tag value, e.g. 'gold-jewelry'. Derived from the slug by the orchestrator in Step 0."}
                    },
                    "required": ["slug", "question", "concept"]
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

        elif name == "semantic_search":
            query = arguments.get("query", "")
            k = arguments.get("k", 5)

            try:
                from sentence_transformers import SentenceTransformer
                import numpy as np
            except ImportError:
                return [types.TextContent(type="text", text="❌ Missing libraries. Run: pip install sentence-transformers numpy")]

            # Lazy load the model in globals so it persists across calls
            global _EMBEDDING_MODEL
            if "_EMBEDDING_MODEL" not in globals():
                try:
                    _EMBEDDING_MODEL = SentenceTransformer('TaylorAI/bge-micro-v2')
                except Exception as e:
                    return [types.TextContent(type="text", text=f"❌ Failed to load embedding model: {e}")]

            try:
                # Embed the query
                query_vec = _EMBEDDING_MODEL.encode([query])[0]
            except Exception as e:
                return [types.TextContent(type="text", text=f"❌ Failed to encode query: {e}")]

            smart_env_dir = VAULT_ROOT / ".smart-env" / "multi"
            if not smart_env_dir.exists():
                return [types.TextContent(type="text", text="❌ Smart Connections database not found at .smart-env/multi")]

            results_list = []
            
            # Fast scan of the .ajson files (json lines format)
            for json_file in smart_env_dir.glob("*.ajson"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if not line: continue
                            if line.endswith(','): line = line[:-1]
                            
                            # Parse single loose JSON line containing the dictionary entry
                            try:
                                data = json.loads(f"{{{line}}}")
                            except:
                                continue
                            
                            for item_key, val in data.items():
                                embeddings = val.get("embeddings", {})
                                if "TaylorAI/bge-micro-v2" in embeddings:
                                    vec = embeddings["TaylorAI/bge-micro-v2"].get("vec")
                                    if vec:
                                        # Calculate cosine similarity using pure numpy (fast)
                                        v1 = np.array(query_vec)
                                        v2 = np.array(vec)
                                        norm1 = np.linalg.norm(v1)
                                        norm2 = np.linalg.norm(v2)
                                        if norm1 == 0 or norm2 == 0: continue
                                        sim = np.dot(v1, v2) / (norm1 * norm2)
                                        
                                        is_block = item_key.startswith("smart_blocks:")
                                        # Smart Connections block references usually have a 'key', 
                                        # files have a 'path'
                                        note_key = val.get("key") or val.get("path")
                                        if not note_key:
                                            note_key = item_key.split(":", 1)[-1]
                                            
                                        results_list.append({
                                            "key": note_key,
                                            "sim": float(sim),
                                            "is_block": is_block
                                        })
                except Exception:
                    pass

            if not results_list:
                return [types.TextContent(type="text", text="❌ No embeddings found in the DB. Ensure Smart Connections is fully synced.")]

            # Sort by similarity descending
            results_list.sort(key=lambda x: x["sim"], reverse=True)
            
            # Deduplicate by retaining only the highest score for a given file
            seen = set()
            top_results = []
            for r in results_list:
                # Group chunks by root path; if an entire document is mapped, it uses just the path
                path = r["key"].split("#")[0]
                if path not in seen:
                    seen.add(path)
                    top_results.append(r)
                if len(top_results) >= k:
                    break
                    
            output_lines = [f"### Semantic Search Results for: '{query}'\n"]
            for i, res in enumerate(top_results, 1):
                # Using Obsidian vault formatting where possible for easy reading
                output_lines.append(f"**{i}.** `[[{res['key']}]]` *(Score: {res['sim']:.3f})*")
                
            return [types.TextContent(type="text", text="\n".join(output_lines))]

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
                # --- Directive-aware block extraction ---
                DIRECTIVE_RE = re.compile(
                    r'\{\{(?:@(blueprint):(\d+)|@(deep)|@(expand))?\s*(.*?)\}\}',
                    re.DOTALL
                )
                # --- H1 boundary map ---
                h1_re = re.compile(r'^# (?!#)(.+)$', re.MULTILINE)
                h1_boundaries = [(m.start(), m.group(1).strip()) for m in h1_re.finditer(content)]

                def get_h1_for_pos(pos):
                    section, idx = "Untitled", 0
                    for i, (start, name) in enumerate(h1_boundaries):
                        if start <= pos:
                            section, idx = name, i
                    return section, idx

                prompt_blocks = []
                for i, m in enumerate(DIRECTIVE_RE.finditer(content)):
                    if m.group(1) == "blueprint":
                        directive = "blueprint"
                        n = int(m.group(2))
                        raw_prompt = m.group(5).strip()
                    elif m.group(3) == "deep":
                        directive = "deep"
                        n = None
                        raw_prompt = m.group(5).strip()
                    elif m.group(4) == "expand":
                        directive = "expand"
                        n = None
                        raw_prompt = m.group(5).strip()
                    else:
                        # No prefix — legacy blocks default to @expand
                        directive = "expand"
                        n = None
                        raw_prompt = m.group(5).strip()
                    # Skip empty matches (HTML comments or whitespace-only blocks)
                    if not raw_prompt:
                        continue
                    h1_name, h1_idx = get_h1_for_pos(m.start())
                    prompt_blocks.append({
                        "block_id": f"{f.stem}_{i+1}",
                        "prompt": raw_prompt,
                        "directive": directive,
                        "n": n,
                        "h1_section": h1_name,
                        "h1_index": h1_idx
                    })
                headers = re.findall(r'^# (?!#)(.+)$', content, re.MULTILINE)
                topics = [h for h in headers if not h.startswith("Created")]
                results.append({
                    "filename": f.name,
                    "path": str(f.relative_to(VAULT_ROOT)),
                    "topics": topics,
                    "prompt_blocks": prompt_blocks,
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
            # --- Robust H1 Header Split (Ignore code blocks) ---
            lines = body.split("\n")
            sections = []
            current_section = []
            in_codeblock = False
            
            for line in lines:
                if line.strip().startswith("```"):
                    in_codeblock = not in_codeblock
                
                if not in_codeblock and line.startswith("# "):
                    if current_section:
                        sections.append("\n".join(current_section))
                    current_section = [line]
                else:
                    current_section.append(line)
                    
            if current_section:
                sections.append("\n".join(current_section))

            sections = [s.strip() for s in sections if s.strip()]
            
            if len(sections) <= 1:
                return [types.TextContent(type="text", text=f"Only 1 true H1 section found. No split needed.")]
            new_files = []
            inbox = VAULT_ROOT / "00_Inbox"
            for i, section in enumerate(sections):
                first_line = section.split("\n")[0]
                # Check if section starts with H1; if not, it's pre-header content
                if first_line.startswith("# "):
                    title = first_line.lstrip("# ").strip()
                else:
                    title = f"Preamble_{target.stem}"
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)[:80].strip()
                out_path = inbox / f"{i+1:02d} - {safe_title}.md"
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
            target_file_str = arguments.get("target_file", "")
            content = arguments.get("content", "")
            
            target = VAULT_ROOT / target_file_str
            
            if not target.exists():
                return [types.TextContent(type="text", text=f"❌ Target file not found: {target_file_str}. The orchestrator must pre-create this file before writing.")]
            # Safety: never write to a file that doesn't carry an allowed prefix or directory
            if not ("00_Inbox" in target.parts and (target.name.startswith("_expand_") or target.name.startswith("_fiqh_"))):
                return [types.TextContent(type="text", text=f"❌ Security: write_expansion can only write to 00_Inbox files starting with _expand_ or _fiqh_")]
            target.write_text(content, encoding="utf-8")
            words = len(content.split())
            return [types.TextContent(type="text", text=f"✅ Written {words} words to {target.name}")]

        elif name == "prepare_dispatch":
            block_id = arguments.get("block_id", "")
            source_path = arguments.get("source_path", "")
            domain = arguments.get("domain", "")
            card_type = arguments.get("card_type", "")
            card_value = arguments.get("card_value", "")

            # --- COLD PATH A: Validate classifier output before any file work ---
            VALID_DOMAINS = ["turing", "euler", "newton", "alhaytham", "iqbal", "nabokov", "ibnkhaldun", "davinci", "machiavelli"]
            VALID_CARD_TYPES = ["card"]
            VALID_CARDS = [
                # turing cards
                "turing_concept", "turing_comparison", "turing_language", "turing_history",
                "turing_algorithm", "turing_debugger", "turing_design", "turing_case",
                # euler cards
                "euler_proof", "euler_concept",
                # other domain cards
                "comparison_philosophy", "comparison_historical",
                "comparison_literary", "comparison_social",
                "explaining_physics", "explaining_science", "explaining_social",
                "philosophical", "thought_experiment", "narrative_history",
                "biography", "case_history", "case_science", "case_social",
                "critical_reading", "character_study", "craft", "craft_art",
                "aesthetic", "design_review", "process", "derivation", "game_theory"
            ]
            errors = []
            if domain not in VALID_DOMAINS:
                errors.append(f"domain='{domain}' not in valid list")
            if card_type not in VALID_CARD_TYPES:
                errors.append(f"card_type='{card_type}' must be 'card'")
            if card_value not in VALID_CARDS:
                errors.append(f"card_value='{card_value}' is not a known card name")
            if errors:
                error_payload = json.dumps({
                    "error": "invalid_classification",
                    "domain_received": domain,
                    "card_type_received": card_type,
                    "card_value_received": card_value,
                    "issues": errors,
                    "valid_domains": VALID_DOMAINS,
                    "valid_cards": VALID_CARDS
                }, indent=2)
                return [types.TextContent(type="text", text=error_payload)]
            # --- END COLD PATH A ---

            # 1. Pre-create temp file
            temp_file = VAULT_ROOT / "00_Inbox" / f"_expand_{block_id}.md"
            temp_file.write_text("", encoding="utf-8")

            # 2. Load card or template content
            # 2. Load card content
            card_path = VAULT_ROOT / "90_System" / "Cards" / f"{card_value}.md"

            if not card_path.exists():
                return [types.TextContent(type="text",
                    text=f"❌ Card not found: {card_path.name}")]
            card_content = card_path.read_text(encoding="utf-8")

            # 3. Read source note and mask all {{...}} blocks
            source_file = VAULT_ROOT / source_path
            if not source_file.exists():
                return [types.TextContent(type="text",
                    text=f"❌ Source note not found: {source_path}")]
            source_content = source_file.read_text(encoding="utf-8")

            # Extract the target prompt from the source
            prompts = re.findall(r'\{\{(.+?)\}\}', source_content, re.DOTALL)
            # block_id format: {filestem}_{index} where index is 1-based
            parts = block_id.rsplit("_", 1)
            block_index = int(parts[-1]) - 1 if parts[-1].isdigit() else 0
            if block_index < len(prompts):
                prompt = prompts[block_index].strip()
            else:
                return [types.TextContent(type="text",
                    text=f"❌ Block index {block_index+1} not found in {source_path} (has {len(prompts)} blocks)")]

            # 4. Return structured payload as JSON
            payload = {
                "block_id": block_id,
                "agent": domain,
                "prompt": prompt,
                "card_content": card_content,
                "card_type": card_type,
                "temp_file": str(temp_file.relative_to(VAULT_ROOT))
            }
            return [types.TextContent(type="text", text=json.dumps(payload, indent=2))]

        elif name == "organize_file":
            source_path = arguments.get("source_path", "")
            dest_dir = arguments.get("destination_dir", "")
            toc_parent = arguments.get("toc_parent", "")
            category = arguments.get("category", "")
            suggested_name = arguments.get("suggested_name", "")
            tags = arguments.get("tags", [])
            
            source_file = VAULT_ROOT / source_path
            if not source_file.exists():
                return [types.TextContent(type="text", text=f"❌ Source note not found: {source_path}")]
            
            content = source_file.read_text(encoding="utf-8")
            
            # --- 1. FRONTMATTER INJECTION ---
            content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            yaml_lines = ["---", "tags:"]
            for t in tags:
                yaml_lines.append(f"  - {t}")
            yaml_lines.append("---")
            yaml_str = "\n".join(yaml_lines) + "\n\n"
            
            # --- 2. UPLINK INJECTION ---
            alias = toc_parent.replace("T.O.C (", "").replace(").md", "")
            uplink = f"[[{toc_parent}|Up to {alias}]]\n\n"
            
            final_content = yaml_str + uplink + content.lstrip()
            
            # --- 3. ID GENERATION & TOC UPDATE ---
            raw_name = suggested_name if suggested_name else source_file.stem
            raw_name = re.sub(r'\.md$', '', raw_name, flags=re.IGNORECASE)
            core_name = re.sub(r'^\d+\s*-\s*', '', raw_name).strip()
            
            final_name = f"{core_name}.md"
            
            with TOC_LOCK:
                if "30_Knowledge_Base" in dest_dir:
                    toc_path = VAULT_ROOT / "30_Knowledge_Base" / "00_Atlas" / toc_parent
                    if toc_path.exists():
                        toc_text = toc_path.read_text(encoding="utf-8")
                        prefix = "E" if category.lower() == "entity" else "C" if category.lower() == "concept" else "F"
                        ids = re.findall(rf'\|\s*\*\*{prefix}\.(\d+)\*\*\s*\|', toc_text)
                        next_num = max([int(i) for i in ids]) + 1 if ids else 1
                        new_id = f"{prefix}.{next_num:02d}"
                        
                        tags_str = " ".join(f"#{t}" for t in tags)
                        toc_tags = f"`{tags_str}`" if tags_str else ""
                        new_row = f"| **{new_id}** | {category} | [[{core_name}]] | {toc_tags} |"
                        
                        final_name = f"{new_id} - {core_name}.md"
                    
                    lines = toc_text.split('\n')
                    insert_idx = len(lines) - 1
                    for i in range(len(lines)-1, -1, -1):
                        if lines[i].strip().startswith("|"):
                            insert_idx = i
                            break
                    lines.insert(insert_idx + 1, new_row)
                    toc_path.write_text("\n".join(lines), encoding="utf-8")
                    
                elif "20_CS_Core" in dest_dir:
                    toc_path = VAULT_ROOT / "20_CS_Core" / toc_parent
                    if toc_path.exists():
                        toc_text = toc_path.read_text(encoding="utf-8")
                        new_row = f"- [[{core_name}]]"
                        toc_path.write_text(toc_text.rstrip() + "\n" + new_row + "\n", encoding="utf-8")

                elif "10_University" in dest_dir:
                    dest_path_dir = VAULT_ROOT / dest_dir
                    toc_path = dest_path_dir / toc_parent
                
                # Fallback: If AI guessed TOC name incorrectly (e.g. "SDA" instead of "Software Design"), find it explicitly
                if not toc_path.exists() and dest_path_dir.exists():
                    for f in dest_path_dir.iterdir():
                        if f.name.startswith("T.O.C") and f.suffix == ".md":
                            toc_path = f
                            break

                sessional = "1"
                parts = Path(dest_dir).parts
                semester = next((p for p in parts if re.match(r'Semester_?\s*\d+', p, re.IGNORECASE)), None)
                if semester:
                    deadlines = VAULT_ROOT / "10_University" / semester / "Admin" / "Deadlines.md"
                    if deadlines.exists():
                        match = re.search(r'\*\*Current Period:\s*(\d+)\*\*', deadlines.read_text(encoding="utf-8"), re.IGNORECASE)
                        if match: sessional = match.group(1)
                
                if toc_path.exists():
                    toc_text = toc_path.read_text(encoding="utf-8")
                    clean_toc = toc_text.replace('**', '')
                    lines = toc_text.split('\n')
                    
                    # 1. Search for the category anywhere in the table (ignores current sessional constraint)
                    cat_match = re.search(rf'\|\s*(\d+\.\d+)\s*\|\s*[^|]*?{re.escape(category)}[^|]*?\|', clean_toc, re.IGNORECASE)
                    
                    if cat_match:
                        base_id = cat_match.group(1)
                        zs = re.findall(rf'\|\s*{re.escape(base_id)}\.(\d+)\s*\|', clean_toc)
                        next_z = max([int(z) for z in zs]) + 1 if zs else 1
                        new_id = f"{base_id}.{next_z}"
                        
                        final_name = f"{new_id} - {source_file.stem}.md"
                        new_row = f"| {new_id} | | [[{final_name.replace('.md', '')}]] |"
                        
                        insert_idx = -1
                        for i, line in enumerate(lines):
                            if re.search(rf'\|\s*\*{0,2}{re.escape(base_id)}(\.\d+)?\*{0,2}\s*\|', line):
                                insert_idx = i
                        
                        if insert_idx != -1:
                            lines.insert(insert_idx + 1, new_row)
                            toc_path.write_text("\n".join(lines), encoding="utf-8")
                            
                    else:
                        # 2. Category doesn't exist! Create it dynamically under the CURRENT sessional
                        sess_match_idx = -1
                        for i, line in enumerate(lines):
                            if re.search(rf'\|\s*\*{0,2}{sessional}\.0\*{0,2}\s*\|', line):
                                sess_match_idx = i
                                break
                                
                        if sess_match_idx == -1:
                            # Sessional header doesn't exist, build it at the bottom of the table
                            for i in range(len(lines)-1, -1, -1):
                                if lines[i].strip().startswith('|'):
                                    sess_match_idx = i
                                    break
                            if sess_match_idx != -1:
                                lines.insert(sess_match_idx + 1, f"| **{sessional}.0** | **Sessional {sessional}** | |")
                                sess_match_idx += 1
                        
                        # Find highest category ID under this sessional to append after
                        highest_cat = 0
                        last_row_idx = sess_match_idx
                        if sess_match_idx != -1:
                            for i in range(sess_match_idx + 1, len(lines)):
                                if not lines[i].strip().startswith('|'):
                                    break
                                last_row_idx = i
                                # Stop if we hit a new Sessional (e.g. 3.0)
                                if re.search(rf'\|\s*\*{0,2}\d+\.0\*{0,2}\s*\|', lines[i]):
                                    last_row_idx = i - 1
                                    break
                                
                                m = re.search(rf'\|\s*\*{0,2}{sessional}\.(\d+)\*{0,2}\s*\|', lines[i])
                                if m:
                                    highest_cat = max(highest_cat, int(m.group(1)))
                                    
                        new_cat_id = f"{sessional}.{highest_cat + 1}"
                        new_id = f"{new_cat_id}.1"
                        
                        final_name = f"{new_id} - {core_name}.md"
                        cat_row = f"| **{new_cat_id}** | **{category}** | |"
                        new_row = f"| {new_id} | | [[{final_name.replace('.md', '')}]] |"
                        
                        if last_row_idx != -1:
                            lines.insert(last_row_idx + 1, cat_row)
                            lines.insert(last_row_idx + 2, new_row)
                            toc_path.write_text("\n".join(lines), encoding="utf-8")
                
            # --- 4. OVERWRITE AND MOVE ---
            source_file.write_text(final_content, encoding="utf-8")
            
            import shutil
            dest_dir_path = VAULT_ROOT / dest_dir
            dest_dir_path.mkdir(parents=True, exist_ok=True)
            target_path = dest_dir_path / final_name
            shutil.move(str(source_file), str(target_path))
            
            return [types.TextContent(type="text", text=f"✅ Successfully organized {final_name} to {dest_dir_path}")]

        elif name == "inject_subblocks":
            source_path = arguments.get("source_path", "")
            block_id = arguments.get("block_id", "")
            directive = arguments.get("directive", "")
            prompt_string = arguments.get("prompt", "")
            n = arguments.get("n", None)
            sections = arguments.get("sections", [])

            # --- Validate sections ---
            if not sections:
                return [types.TextContent(type="text", text="❌ inject_subblocks: 'sections' array is empty.")]
            if n is not None and len(sections) != n:
                return [types.TextContent(type="text", text=f"❌ inject_subblocks: @blueprint:{n} requires exactly {n} sections, but received {len(sections)}.")]
            if not prompt_string:
                return [types.TextContent(type="text", text="❌ inject_subblocks: 'prompt' string is required to locate the block safely.")]

            source_file = VAULT_ROOT / source_path
            if not source_file.exists():
                return [types.TextContent(type="text", text=f"❌ Source file not found: {source_path}")]

            content = source_file.read_text(encoding="utf-8")

            # --- Target the exact block by its prompt text ---
            # By escaping the prompt, we guarantee we modify exactly this block
            # independent of how many blocks were injected before it.
            escaped_prompt = re.escape(prompt_string)
            pattern1 = r'\{\{\s*(?:@(blueprint):\d+|@(deep)|@(expand))?\s*' + escaped_prompt + r'\s*\}\}'
            search_re = re.compile(pattern1, re.DOTALL)
            
            target_match = search_re.search(content)
            if not target_match:
                # Fallback: maybe the prompt has weird whitespace, try stripping
                escaped_stripped = re.escape(prompt_string.strip())
                pattern2 = r'\{\{\s*(?:[^}]+)?' + escaped_stripped + r'\s*\}\}'
                stripped_re = re.compile(pattern2, re.DOTALL)
                target_match = stripped_re.search(content)
                if not target_match:
                    return [types.TextContent(type="text", text=f"❌ Target block for prompt not found in {source_path}.")]

            original_prompt = prompt_string

            # --- Build replacement: HTML comment + injected sub-blocks ---
            comment = f"<!-- @{directive}" + (f":{n}" if n else "") + f" processed: {original_prompt} -->"

            sub_blocks = []
            for section in sections:
                title = section.get("title", "").strip()
                prompt = section.get("prompt", "").strip()
                if not title or not prompt:
                    continue
                sub_blocks.append(f"\n## {title}\n{{{{@expand {prompt}}}}}")

            replacement = comment + "\n" + "\n".join(sub_blocks)

            # Perform the substitution at the exact match position
            new_content = content[:target_match.start()] + replacement + content[target_match.end():]
            source_file.write_text(new_content, encoding="utf-8")

            return [types.TextContent(type="text", text=f"✅ inject_subblocks: {len(sub_blocks)} sub-blocks injected into {source_path}")]

        elif name == "append_summary":
            summary_file_path = arguments.get("summary_file", "")
            entry = arguments.get("entry", "").strip()
            if not entry:
                return [types.TextContent(type="text", text="❌ append_summary: 'entry' is empty.")]
            summary_file = VAULT_ROOT / summary_file_path
            summary_file.parent.mkdir(parents=True, exist_ok=True)
            existing = summary_file.read_text(encoding="utf-8") if summary_file.exists() else ""
            updated = existing + f"- {entry}\n"
            summary_file.write_text(updated, encoding="utf-8")
            count = len([l for l in updated.splitlines() if l.startswith("- ")])
            return [types.TextContent(type="text", text=f"✅ append_summary: {count} entries in {summary_file_path}")]

        elif name == "stitch_files":
            source_path = arguments.get("source_path", "")
            blocks = arguments.get("blocks", [])

            if not blocks:
                return [types.TextContent(type="text", text="❌ stitch_files: 'blocks' array is empty.")]

            source_file = VAULT_ROOT / source_path
            if not source_file.exists():
                return [types.TextContent(type="text", text=f"❌ Source file not found: {source_path}")]

            content = source_file.read_text(encoding="utf-8")
            
            DIRECTIVE_RE = re.compile(
                r'\{\{(?:@(blueprint):(\d+)|@(deep)|@(expand))?\s*(.*?)\}\}',
                re.DOTALL
            )
            
            all_matches = list(DIRECTIVE_RE.finditer(content))
            
            temp_contents = {}
            for b in blocks:
                b_id = b.get("block_id", "")
                t_file = b.get("temp_file", "")
                
                parts = b_id.rsplit("_", 1)
                if not parts[-1].isdigit():
                    continue
                b_idx = int(parts[-1]) - 1
                
                t_path = VAULT_ROOT / t_file
                if t_path.exists():
                    temp_contents[b_idx] = (t_path.read_text(encoding="utf-8"), t_path)
            
            stitched_count = 0
            for idx in range(len(all_matches) - 1, -1, -1):
                if idx in temp_contents:
                    match = all_matches[idx]
                    replacement_text, t_path = temp_contents[idx]
                    content = content[:match.start()] + replacement_text + content[match.end():]
                    t_path.unlink()  # Delete temp file
                    stitched_count += 1
            
            source_file.write_text(content, encoding="utf-8")
            return [types.TextContent(type="text", text=f"✅ stitch_files: {stitched_count} blocks stitched into {source_path}")]

        elif name == "prepare_fiqh_dispatch":
            slug = arguments.get("slug", "").strip()
            school = arguments.get("school", "")
            card = arguments.get("card", "")
            question = arguments.get("question", "").strip()
            query_type = arguments.get("query_type", "")
            madhab_temp_files = arguments.get("madhab_temp_files", [])

            VALID_SCHOOLS = ["hanafi", "maliki", "shafii", "hanbali", "synthesizer"]
            VALID_CARDS = ["fiqh_ruling", "fiqh_usul_deep", "fiqh_historical", "fiqh_contemporary"]
            VALID_QUERY_TYPES = ["Classical", "Derived", "Mixed"]

            # --- Validation ---
            errors = []
            if not slug:
                errors.append("'slug' is required and cannot be empty.")
            elif not re.match(r'^[a-z0-9\-]+$', slug):
                errors.append(f"'slug' must contain only lowercase letters, digits, and hyphens. Received: '{slug}'")
            if school not in VALID_SCHOOLS:
                errors.append(f"'school' must be one of {VALID_SCHOOLS}. Received: '{school}'")
            if card not in VALID_CARDS:
                errors.append(f"'card' must be one of {VALID_CARDS}. Received: '{card}'")
            if not question:
                errors.append("'question' is required and cannot be empty.")
            if query_type not in VALID_QUERY_TYPES:
                errors.append(f"'query_type' must be one of {VALID_QUERY_TYPES}. Received: '{query_type}'")
            if school == "synthesizer" and not madhab_temp_files:
                errors.append("'madhab_temp_files' is required when school is 'synthesizer'.")
            if school == "synthesizer" and len(madhab_temp_files) != 4:
                errors.append(f"'madhab_temp_files' must contain exactly 4 paths (one per school). Received {len(madhab_temp_files)}.")
            if errors:
                return [types.TextContent(type="text", text=json.dumps({"error": "validation_failed", "issues": errors}, indent=2))]

            # --- Load card ---
            card_path = VAULT_ROOT / "90_System" / "Cards" / f"{card}.md"
            if not card_path.exists():
                return [types.TextContent(type="text", text=json.dumps({
                    "error": "card_not_found",
                    "path_checked": str(card_path),
                    "hint": f"Create '90_System/Cards/{card}.md' as part of Phase 3 before dispatching agents."
                }, indent=2))]
            card_content = card_path.read_text(encoding="utf-8")

            # --- Pre-create temp file ---
            block_id = f"fiqh_{school}_{slug}"
            inbox = VAULT_ROOT / "00_Inbox"
            if not inbox.exists():
                return [types.TextContent(type="text", text=json.dumps({"error": "inbox_not_found", "path_checked": str(inbox)}, indent=2))]
            temp_file = inbox / f"_fiqh_{block_id}.md"
            # Always overwrite — idempotent; a stale file from a failed run should not block a retry
            temp_file.write_text("", encoding="utf-8")

            # --- Verify madhab temp files exist (synthesizer only) ---
            if school == "synthesizer":
                missing = [p for p in madhab_temp_files if not (VAULT_ROOT / p).exists()]
                if missing:
                    return [types.TextContent(type="text", text=json.dumps({
                        "error": "madhab_files_missing",
                        "missing": missing,
                        "hint": "Verify all four madhab agents completed successfully (word_count > 0) before calling synthesizer."
                    }, indent=2))]

            # --- Build payload ---
            payload = {
                "block_id": block_id,
                "temp_file": str(temp_file.relative_to(VAULT_ROOT)),
                "school": school,
                "question": question,
                "query_type": query_type,
                "card": card,
                "card_content": card_content,
            }
            if school == "synthesizer":
                payload["madhab_temp_files"] = madhab_temp_files

            return [types.TextContent(type="text", text=json.dumps(payload, indent=2))]

        elif name == "fiqh_link_and_finalize":
            slug = arguments.get("slug", "").strip()
            question = arguments.get("question", "").strip()
            concept = arguments.get("concept", "").strip()

            # --- Validation ---
            errors = []
            if not slug:
                errors.append("'slug' is required.")
            if not question:
                errors.append("'question' is required.")
            if not concept:
                errors.append("'concept' is required.")
            if errors:
                return [types.TextContent(type="text", text=json.dumps({"error": "validation_failed", "issues": errors}, indent=2))]

            SCHOOLS = ["hanafi", "maliki", "shafii", "hanbali"]
            SCHOOL_DISPLAY = {"hanafi": "Hanafi", "maliki": "Maliki", "shafii": "Shafii", "hanbali": "Hanbali"}
            inbox = VAULT_ROOT / "00_Inbox"

            # --- Pre-flight: verify ALL 5 temp files exist before touching anything ---
            temp_paths = {}
            for school in SCHOOLS:
                block_id = f"fiqh_{school}_{slug}"
                p = inbox / f"_fiqh_{block_id}.md"
                temp_paths[school] = p
            synth_block_id = f"fiqh_synthesizer_{slug}"
            synth_temp = inbox / f"_fiqh_{synth_block_id}.md"
            temp_paths["synthesizer"] = synth_temp

            missing = [str(p.relative_to(VAULT_ROOT)) for p in temp_paths.values() if not p.exists()]
            if missing:
                return [types.TextContent(type="text", text=json.dumps({
                    "error": "preflight_failed",
                    "missing_temp_files": missing,
                    "hint": "All 5 temp files must exist before finalization. Check that all agents ran and word_count > 0 for each."
                }, indent=2))]

            # Also verify no temp file is empty (agent wrote nothing)
            empty = [str(p.relative_to(VAULT_ROOT)) for p in temp_paths.values() if p.stat().st_size == 0]
            if empty:
                return [types.TextContent(type="text", text=json.dumps({
                    "error": "preflight_failed",
                    "empty_temp_files": empty,
                    "hint": "These temp files are empty — the agent did not write output. Re-dispatch the affected agent(s)."
                }, indent=2))]

            # --- Create destination folder ---
            dest_dir = VAULT_ROOT / "30_Knowledge_Base" / "Fiqh" / slug
            dest_dir.mkdir(parents=True, exist_ok=True)

            # --- Build standard tags ---
            madhab_tags = ["field/humanities", f"concept/{concept}", "subject/fiqh"]
            synth_tags = ["field/humanities", f"concept/{concept}", "subject/fiqh", "type/map"]

            # --- Helper: inject/merge frontmatter then write ---
            def inject_frontmatter(file_path: Path, new_tags: list) -> None:
                content = file_path.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(content)
                if fm is not None and "tags" in fm:
                    existing = set(fm["tags"])
                    for tag in new_tags:
                        existing.add(tag.strip())
                    all_tags = sorted(existing)
                else:
                    all_tags = sorted(set(t.strip() for t in new_tags))
                new_content = build_frontmatter(all_tags) + "\n" + body
                file_path.write_text(new_content, encoding="utf-8")

            # --- Helper: inject back-link after the first [[...]] wikilink line ---
            def inject_backlink(file_path: Path, backlink: str) -> None:
                content = file_path.read_text(encoding="utf-8")
                # Find first line that contains a wikilink (the uplink line after frontmatter)
                lines = content.split("\n")
                insert_idx = None
                in_frontmatter = False
                fm_closed = False
                for i, line in enumerate(lines):
                    if i == 0 and line.strip() == "---":
                        in_frontmatter = True
                        continue
                    if in_frontmatter and line.strip() == "---":
                        in_frontmatter = False
                        fm_closed = True
                        continue
                    if fm_closed and "[[" in line and "]]" in line:
                        insert_idx = i
                        break
                if insert_idx is not None:
                    # Append backlink on the same header line, separated by " | "
                    # Only add if not already present
                    if backlink not in lines[insert_idx]:
                        lines[insert_idx] = lines[insert_idx].rstrip() + " | " + backlink
                else:
                    # Fallback: prepend after frontmatter block
                    for i, line in enumerate(lines):
                        if fm_closed and i > 0:
                            lines.insert(i, backlink)
                            break
                file_path.write_text("\n".join(lines), encoding="utf-8")

            # --- Process each madhab file ---
            results = {}
            synthesis_link = f"[[Synthesis - {slug}|View Synthesis]]"
            for school in SCHOOLS:
                temp = temp_paths[school]
                display = SCHOOL_DISPLAY[school]
                final_name = f"{display} - {slug}.md"
                final_path = dest_dir / final_name

                inject_frontmatter(temp, madhab_tags)
                inject_backlink(temp, synthesis_link)
                shutil.move(str(temp), str(final_path))
                words = len(final_path.read_text(encoding="utf-8").split())
                results[school] = {"file": str(final_path.relative_to(VAULT_ROOT)), "words": words}

            # --- Process synthesis file ---
            synth_final_name = f"Synthesis - {slug}.md"
            synth_final_path = dest_dir / synth_final_name
            inject_frontmatter(synth_temp, synth_tags)
            shutil.move(str(synth_temp), str(synth_final_path))
            synth_words = len(synth_final_path.read_text(encoding="utf-8").split())
            results["synthesizer"] = {"file": str(synth_final_path.relative_to(VAULT_ROOT)), "words": synth_words}

            # --- Update T.O.C (Fiqh).md ---
            toc_path = VAULT_ROOT / "30_Knowledge_Base" / "Fiqh" / "T.O.C (Fiqh).md"
            toc_link = f"- [[Synthesis - {slug}|{question}]]"
            if toc_path.exists():
                toc_text = toc_path.read_text(encoding="utf-8")
                # Guard: don't add the same entry twice
                if toc_link not in toc_text:
                    if "## Questions" in toc_text:
                        # Insert after the ## Questions header line
                        toc_text = toc_text.replace(
                            "## Questions",
                            "## Questions\n" + toc_link
                        )
                    else:
                        # Fallback: T.O.C exists but missing ## Questions section — append it
                        toc_text = toc_text.rstrip() + "\n\n## Questions\n" + toc_link + "\n"
                    toc_path.write_text(toc_text, encoding="utf-8")
                toc_status = "updated"
            else:
                # T.O.C missing entirely — create a minimal one so the vault doesn't break
                toc_content = (
                    "---\ntags:\n  - type/map\n  - field/humanities\n  - subject/fiqh\n---\n"
                    "# T.O.C (Fiqh)\n\n"
                    "[[T.O.C (30_Knowledge_Base)|Up to Knowledge Base]]\n\n"
                    "---\n\n## Questions\n" + toc_link + "\n"
                )
                toc_path.write_text(toc_content, encoding="utf-8")
                toc_status = "created"

            # --- Return summary ---
            summary = {
                "status": "ok",
                "slug": slug,
                "destination": str(dest_dir.relative_to(VAULT_ROOT)),
                "toc": toc_status,
                "tags_applied": {"madhab_files": madhab_tags, "synthesis_file": synth_tags},
                "files": results,
            }
            return [types.TextContent(type="text", text=json.dumps(summary, indent=2))]

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