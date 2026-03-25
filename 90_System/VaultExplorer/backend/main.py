import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VAULT_ROOT = r"d:\WISDOM\Kybernetes"

def build_tree(dir_path):
    tree = []
    try:
        for entry in sorted(os.scandir(dir_path), key=lambda x: (not x.is_dir(), x.name)):
            if entry.name.startswith(".") or entry.name in ["node_modules", "tmp", "Archive"]:
                continue
            
            node = {
                "name": entry.name,
                "path": entry.path.replace(VAULT_ROOT, "").lstrip("\\/").replace("\\", "/"),
                "isDir": entry.is_dir()
            }
            if entry.is_dir():
                node["children"] = build_tree(entry.path)
            tree.append(node)
    except PermissionError:
        pass
    return tree

@app.get("/api/tree")
def get_tree():
    if not os.path.exists(VAULT_ROOT):
        raise HTTPException(status_code=404, detail="Vault not found")
    return build_tree(VAULT_ROOT)

@app.get("/api/file")
def get_file(path: str):
    full_path = os.path.join(VAULT_ROOT, path.replace("/", "\\"))
    full_path = os.path.abspath(full_path)
    if not full_path.startswith(os.path.abspath(VAULT_ROOT)) or not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(full_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}
