import fs from 'fs';
import path from 'path';

// For local testing vs actual deployment in 90_System
const isLocalTesting = process.cwd().includes('PROJECTS');
const VAULT_ROOT = isLocalTesting ? 'D:\\WISDOM\\Kybernetes' : path.resolve(process.cwd(), '../..');
const API_DIR = path.resolve(process.cwd(), 'public/api');

const ignoreDirs = new Set(['.obsidian', '.git', 'node_modules', 'tmp', '90_System', 'Archive', 'dist', 'public']);

if (!fs.existsSync(API_DIR)) {
  fs.mkdirSync(API_DIR, { recursive: true });
}

const fileMap = {};

function buildTree(dirPath) {
  const nodes = [];
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    if (ignoreDirs.has(entry.name) || entry.name.startsWith('.')) continue;

    const fullPath = path.join(dirPath, entry.name);
    // Use relative path to root for consistency
    const relativePath = path.relative(VAULT_ROOT, fullPath).replace(/\\/g, '/');

    if (entry.isDirectory()) {
      const children = buildTree(fullPath);
      if (children.length > 0) {
        nodes.push({
          name: entry.name,
          path: relativePath,
          isDir: true,
          children
        });
      }
    } else if (entry.name.endsWith('.md')) {
      nodes.push({
        name: entry.name,
        path: relativePath,
        isDir: false
      });
      // Add text content to mega map
      fileMap[relativePath] = fs.readFileSync(fullPath, 'utf8');
    }
  }

  // Sort nodes: folders first, then alphabetically
  return nodes.sort((a, b) => {
    if (a.isDir !== b.isDir) return b.isDir ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
}

console.log(`Scanning vault at: ${VAULT_ROOT}`);
const tree = buildTree(VAULT_ROOT);

fs.writeFileSync(path.join(API_DIR, 'tree.json'), JSON.stringify(tree, null, 2));
fs.writeFileSync(path.join(API_DIR, 'files.json'), JSON.stringify(fileMap));
console.log(`Successfully built vault API. Indexed ${Object.keys(fileMap).length} markdown files.`);
