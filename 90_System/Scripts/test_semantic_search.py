import sys
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

VAULT_ROOT = Path(r"D:\WISDOM\Kybernetes")
smart_env_dir = VAULT_ROOT / ".smart-env" / "multi"

query = "What is active RAG and how does it relate to PKM?"
print(f"Loading model and embedding query: '{query}'...")
model = SentenceTransformer('TaylorAI/bge-micro-v2')
query_vec = model.encode([query])[0]

print("Scanning vector database...")
results_list = []

for json_file in smart_env_dir.glob("*.ajson"):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if line.endswith(','): line = line[:-1]
                try:
                    data = json.loads(f"{{{line}}}")
                except Exception as e:
                    continue
                
                for item_key, val in data.items():
                    embeddings = val.get("embeddings", {})
                    if "TaylorAI/bge-micro-v2" in embeddings:
                        vec = embeddings["TaylorAI/bge-micro-v2"].get("vec")
                        if vec:
                            v1 = np.array(query_vec)
                            v2 = np.array(vec)
                            norm1 = np.linalg.norm(v1)
                            norm2 = np.linalg.norm(v2)
                            if norm1 == 0 or norm2 == 0: continue
                            sim = np.dot(v1, v2) / (norm1 * norm2)
                            
                            is_block = item_key.startswith("smart_blocks:")
                            note_key = val.get("key") or val.get("path")
                            if not note_key:
                                note_key = item_key.split(":", 1)[-1]
                                
                            results_list.append({
                                "key": note_key,
                                "sim": float(sim),
                                "is_block": is_block
                            })
    except Exception as e:
        print(f"Error reading {json_file.name}: {e}")

if not results_list:
    print("❌ No embeddings found in the DB.")
    sys.exit(1)

results_list.sort(key=lambda x: x["sim"], reverse=True)
seen = set()
top_results = []
for r in results_list:
    path = r["key"].split("#")[0]
    if path not in seen:
        seen.add(path)
        top_results.append(r)
    if len(top_results) >= 5:
        break

print("\n### Semantic Search Results")
for i, res in enumerate(top_results, 1):
    print(f"**{i}.** `[[{res['key']}]]` *(Score: {res['sim']:.3f})*")
