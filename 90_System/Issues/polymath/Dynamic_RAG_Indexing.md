# Dynamic RAG: Growing the Vector Bank

A common misconception about Vector Databases (RAG) is that you have to re-compute and re-embed the entire vault every time you add a single new note. This is mathematically and computationally expensive, and completely unnecessary. 

Here is how Kybernetes can maintain a dynamic, self-updating RAG pipeline without re-embedding the whole system.

## The Solution: Incremental Indexing

A Vector Database (like ChromaDB or FAISS) is not a static block of concrete. It is a collection of individual records. Each record has:
1. **An ID** (usually the file path + chunk number).
2. **The Vector Array** (the embedded meaning).
3. **Metadata** (tags, title, last modified date).

You do not need to drop the database to add a note. You can perform `Upserts` (Update or Insert operations) on individual files.

## The Implementation Architecture

To ensure the `@polymath` agent always has up-to-date knowledge, we integrate the embedding process directly into your existing OS file pipeline.

### 1. The Pre-Computation (Run Once)
The very first time we set up the system, we run a batch script (`build_index.py`). It scans the entire `30_Knowledge_Base`, embeds every file, and builds the initial `vector_store.db`. This might take 5-10 minutes. We only do this once.

### 2. The OS Daemon (The Continuous Sync)
We don't want to run a script manually every time we write a note. We automate it. There are two ways to hook this into Kybernetes:

#### Option A: The `/os:sort` Hook (Event-Driven)
You currently use `/os:sort` to ingest raw prompts, dispatch domain agents, stitch the files (`@surgeon`), and organize the files (`@librarian`). 

We simply add one final step to the `inbox-sort` skill: The **Indexer**.
After `@librarian` moves the final generated file into `10_Concepts` or `30_Frameworks`, the script takes that specific file path, chunks the text, runs it through the local embedding model, and pushes *only* that file's vectors into the existing database. 

*Result:* Every time a new idea is fully processed by the OS, its meaning is instantly added to the Vector Bank.

#### Option B: The Observer Script (Filesystem Watcher)
If you also write notes manually (bypassing `/os:sort`), we set up a lightweight background Python script using the `Watchdog` library. It constantly monitors the `30_Knowledge_Base` directory. 
- When a file is modified, it runs an `Upsert` (replacing the old vectors for that specific `file_path` ID with the new vectors).
- When a file is deleted, it removes that ID from the database.

*Result:* The Vector Bank acts like a shadow mirror of your Obsidian Vault, staying perfectly synchronized in real-time.

## Conclusion
You will never have to re-embed the entire system. By utilizing Incremental Indexing and hooking into the existing Kybernetes workflow, the RAG engine will dynamically and effortlessly grow alongside your Knowledge Base.
