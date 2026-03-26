import fs from 'fs';
import path from 'path';

// Support both local testing and Vercel edge deployment
const isLocalTesting = process.cwd().includes('PROJECTS');
const VAULT_ROOT = isLocalTesting ? 'D:\\WISDOM\\Kybernetes' : path.resolve(process.cwd(), '../..');
const API_DIR = path.resolve(process.cwd(), 'public/api');

const ignoreDirs = new Set(['.obsidian', '.git', 'node_modules', 'tmp', '90_System', 'Archive', 'dist', 'public']);

if (!fs.existsSync(API_DIR)) {
  fs.mkdirSync(API_DIR, { recursive: true });
}

const fileMap = {};
const graphNodes = [];
const graphLinks = [];
const nodeIds = new Set();
const rawLinksTmp = [];

function extractTags(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return [];
  const lines = match[1].split('\n');
  const tagsLine = lines.find(l => l.startsWith('tags:'));
  if (!tagsLine) return [];
  return tagsLine.replace('tags:', '').split(',').map(t => t.trim().replace(/"|'/g, '').replace(/^- |^\[|\]$/g, '').trim()).filter(t => t);
}

function extractLinks(content, sourcePath) {
  const sourceName = path.basename(sourcePath, '.md').toLowerCase();
  const regex = /\[\[([\s\S]*?)\]\]/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const targetRaw = match[1].split('|')[0].split('#')[0].split('^')[0].replace(/\.md$/i, '').trim();
    const parts = targetRaw.split(/[/\\]/);
    const baseTarget = parts[parts.length - 1].toLowerCase().replace(/\s+/g, '');
    rawLinksTmp.push({ source: sourceName, targetMatcher: baseTarget });
  }
}

function buildTree(dirPath) {
  const nodes = [];
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    if (ignoreDirs.has(entry.name) || entry.name.startsWith('.')) continue;

    const fullPath = path.join(dirPath, entry.name);
    const relativePath = path.relative(VAULT_ROOT, fullPath).replace(/\\/g, '/');

    if (entry.isDirectory()) {
      const children = buildTree(fullPath);
      if (children.length > 0) {
        nodes.push({ name: entry.name, path: relativePath, isDir: true, children });
      }
    } else if (entry.name.endsWith('.md')) {
      nodes.push({ name: entry.name, path: relativePath, isDir: false });
      
      const content = fs.readFileSync(fullPath, 'utf8');
      fileMap[relativePath] = content;
      
      const baseName = path.basename(entry.name, '.md');
      const lowerBase = baseName.toLowerCase();
      const matchBase = lowerBase.replace(/\s+/g, '');
      
      nodeIds.add(matchBase);
      
      const tags = extractTags(content);
      let group = 0; 
      // Theming groups based on Kybernetes system
      if (tags.some(t => t.includes('cs'))) group = 1; 
      else if (tags.some(t => t.includes('math'))) group = 2; 
      else if (tags.some(t => t.includes('humanities'))) group = 3; 
      else if (tags.some(t => t.includes('ai'))) group = 4; 
      else if (tags.some(t => t.includes('os'))) group = 5; 
      else if (tags.some(t => t.includes('map') || t.includes('system'))) group = 6; 

      graphNodes.push({
        id: matchBase,
        label: baseName,
        path: relativePath,
        group: group,
        val: 1
      });

      extractLinks(content, relativePath);
    }
  }
  return nodes.sort((a, b) => {
    if (a.isDir !== b.isDir) return b.isDir ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
}

console.log(`Scanning vault at: ${VAULT_ROOT}`);
const tree = buildTree(VAULT_ROOT);

// Prune dead links and calculate gravity mass (val)
for (const link of rawLinksTmp) {
  if (nodeIds.has(link.targetMatcher)) {
    graphLinks.push({ source: link.source.replace(/\s+/g, ''), target: link.targetMatcher });
    const targetNode = graphNodes.find(n => n.id === link.targetMatcher);
    const sourceNode = graphNodes.find(n => n.id === link.source.replace(/\s+/g, ''));
    if (targetNode) targetNode.val += 0.5;
    if (sourceNode) sourceNode.val += 0.2;
  }
}

fs.writeFileSync(path.join(API_DIR, 'tree.json'), JSON.stringify(tree, null, 2));
fs.writeFileSync(path.join(API_DIR, 'files.json'), JSON.stringify(fileMap));
fs.writeFileSync(path.join(API_DIR, 'graph.json'), JSON.stringify({ nodes: graphNodes, links: graphLinks }));
console.log(`Successfully built vault API. Indexed ${Object.keys(fileMap).length} notes and ${graphLinks.length} connections.`);
