import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import 'katex/dist/katex.min.css';

const API_BASE = '/api';

interface FileNode {
  name: string;
  path: string;
  isDir: boolean;
  children?: FileNode[];
}

function App() {
  const [tree, setTree] = useState<FileNode[]>([]);
  const [fileMap, setFileMap] = useState<Record<string, string>>({});
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch(`${API_BASE}/tree.json`)
      .then((res) => res.json())
      .then((data) => setTree(data))
      .catch((err) => console.error("Failed to load vault tree", err));

    fetch(`${API_BASE}/files.json`)
      .then((res) => res.json())
      .then((data) => setFileMap(data))
      .catch((err) => console.error("Failed to load files map", err));
  }, []);

  const toggleFolder = (path: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const next = new Set(expandedFolders);
    if (next.has(path)) {
      next.delete(path);
    } else {
      next.add(path);
    }
    setExpandedFolders(next);
  };

  const handleSelectNode = (node: FileNode) => {
    if (!node.isDir) {
      setSelectedFile(node);
      setLoading(true);
      // Simulate network decrypt delay for the cyberpunk aesthetic
      setTimeout(() => {
        setFileContent(fileMap[node.path] || '---\nEmpty node\n---\nTarget missing or corrupted.');
        setLoading(false);
      }, 150);
    }
  };

  const findNodeByName = (nodes: FileNode[], targetName: string): FileNode | null => {
    // Deep clean Obsidian specific target metadata (#headings, ^blocks) before fuzzy matched
    let cleanTarget = targetName.split('#')[0].split('^')[0].replace(/\.md$/i, '').toLowerCase().trim();
    // Handle cases where obsidian links include paths (e.g. Folder/Note)
    const parts = cleanTarget.split(/[/\\]/);
    const baseTarget = parts[parts.length - 1].replace(/\s+/g, ''); // strip all spaces for safety

    for (const node of nodes) {
      if (!node.isDir) {
        const nodeBase = node.name.replace(/\.md$/i, '').toLowerCase().replace(/\s+/g, '');
        if (nodeBase === baseTarget) {
          return node;
        }
      }
      if (node.isDir && node.children) {
        const found = findNodeByName(node.children, targetName);
        if (found) return found;
      }
    }
    return null;
  };

  const handleLinkClick = (targetName: string) => {
    const node = findNodeByName(tree, targetName);
    if (node) {
      handleSelectNode(node);
    } else {
      alert(`Vault Error: Could not locate a note matching "${targetName.split('#')[0]}" in the file tree.`);
      console.warn("Could not find note in tree:", targetName);
    }
  };

  const renderTree = (nodes: FileNode[], level = 0) => {
    return nodes.map((node) => {
      const isExpanded = expandedFolders.has(node.path);
      const isSelected = selectedFile?.path === node.path;
      return (
        <div key={node.path} className={`pl-${level === 0 ? 0 : 3} space-y-0.5`}>
          <div 
            className={`flex items-center gap-1.5 py-1.5 cursor-pointer font-label text-[13px] transition-all rounded-sm select-none
              ${isSelected ? 'text-primary bg-primary/10 px-2 border border-primary/20' : 'text-slate-400 hover:text-slate-200 hover:bg-[#1f1f26] px-2'}`}
            onClick={(e) => {
              if (node.isDir) {
                toggleFolder(node.path, e);
                const tocNode = node.children?.find(n => n.name.startsWith('T.O.C'));
                if (tocNode) {
                  handleSelectNode(tocNode);
                }
              } else {
                handleSelectNode(node);
              }
            }}
          >
            {node.isDir ? (
              <>
                <span className="material-symbols-outlined text-[16px] opacity-70">
                  {isExpanded ? 'keyboard_arrow_down' : 'keyboard_arrow_right'}
                </span>
                <span className="material-symbols-outlined text-[16px] text-primary/70" style={{ fontVariationSettings: isExpanded ? "'FILL' 1" : "'FILL' 0" }}>
                  {isExpanded ? 'folder_open' : 'folder'}
                </span>
              </>
            ) : (
              <span className="material-symbols-outlined text-[16px] opacity-50 ml-[22px]">description</span>
            )}
            <span className={`truncate ${node.name.startsWith('T.O.C') ? 'text-primary/90 font-bold tracking-wide' : ''}`}>
              {node.name.replace('.md', '')}
            </span>
          </div>
          {node.isDir && isExpanded && node.children && (
            <div className="pl-1 border-l border-[#2A2A35] ml-4 mt-1">
              {renderTree(node.children, level + 1)}
            </div>
          )}
        </div>
      );
    });
  };

  const extractTags = (content: string) => {
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return [];
    const lines = match[1].split('\n');
    const tagsLine = lines.find(l => l.startsWith('tags:'));
    if (!tagsLine) return [];
    return tagsLine.replace('tags:', '').split(',')
      .map(t => t.trim().replace(/"|'/g, '').replace(/^- |^\[|\]$/g, '').trim())
      .filter(t => t);
  };

  const tags = fileContent ? extractTags(fileContent) : [];
  let cleanContent = fileContent ? fileContent.replace(/^---\n[\s\S]*?\n---/, '') : '';

  // Obsidian Pre-processor (Wikilinks, Marks, Callouts)
  cleanContent = cleanContent.replace(/(!?)\[\[([\s\S]*?)\]\]/g, (match, prefix, p1) => {
    // Ignore Obsidian Image Embeds `![[...]]` for now
    if (prefix === '!') return match; 
    
    // In markdown tables, users escape the alias pipe like `\|`
    // If we simply split by `|`, the target gets a trailing `\`
    // So we replace `\|` with a temporary placeholder, or just clean the trailing slash.
    const parts = p1.split('|');
    const target = parts[0].replace(/\\$/, '').trim(); 
    const text = parts.length > 1 ? parts[1].trim() : target;
    
    // URL Encode the target and use a hash fragment to bypass ReactMarkdown's strict URL protocol filtering
    return `[${text}](#obsidian:${encodeURIComponent(target)})`;
  });
  
  cleanContent = cleanContent.replace(/==(.*?)==/g, '<mark class="bg-primary/20 text-primary px-1 rounded-sm">$1</mark>');
  
  cleanContent = cleanContent.replace(/^> \[!(.*?)\](.*?)$/gm, (match, type, title) => {
    const isWarn = ['warning', 'caution', 'error'].includes(type.toLowerCase());
    const isInfo = ['info', 'note', 'abstract'].includes(type.toLowerCase());
    const colorClass = isWarn ? 'border-amber-500 text-amber-500 bg-amber-500/10' : 
                       isInfo ? 'border-primary text-primary bg-primary/10' : 
                       'border-tertiary text-tertiary bg-tertiary/10';
    return `<div class="p-3 my-4 border-l-4 rounded-r-sm ${colorClass}">
              <div class="font-bold font-technical text-xs uppercase tracking-widest mb-1">${title || type}</div>`;
  });
  cleanContent = cleanContent.replace(/^> /gm, ''); // let HTML div handle blockquote

  return (
    <div className="bg-[#000000] text-on-surface font-body selection:bg-primary/30 h-screen flex flex-col overflow-hidden">
      <header className="bg-[#000000]/80 backdrop-blur-xl flex justify-between items-center w-full px-6 h-14 border-b border-[#2A2A35]">
        <div className="flex items-center gap-4">
          <span className="text-sm font-black tracking-widest uppercase text-primary font-headline">Vault Explorer</span>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-[320px] flex-shrink-0 bg-[#0A0A0C] flex flex-col border-r border-[#2A2A35] overflow-y-auto">
          <div className="p-4 mb-2 sticky top-0 bg-[#0A0A0C]/90 backdrop-blur-sm z-10 border-b border-[#2A2A35]">
            <div className="text-[9px] uppercase tracking-[0.2em] text-slate-500 font-technical mb-2">Workspace</div>
            <div className="text-primary text-xs font-technical tracking-wider break-all bg-primary/5 p-2 rounded-sm border border-primary/20">
              D:\\WISDOM\\Kybernetes
            </div>
          </div>
          <nav className="flex-1 px-2 pb-10">
            {tree.length > 0 ? renderTree(tree) : <div className="text-center text-slate-500 text-xs mt-10 animate-pulse">Scanning Vault...</div>}
          </nav>
        </aside>

        {/* Viewer */}
        <section className="flex-1 bg-[#0A0A0C] overflow-y-auto w-full scroll-smooth">
          {selectedFile ? (
            <>
              <div className="sticky top-0 bg-[#0A0A0C]/95 backdrop-blur-md px-10 py-4 flex items-center justify-between z-20 border-b border-[#2A2A35] shadow-[0_10px_30px_rgba(0,0,0,0.8)]">
                <div className="flex items-center gap-2 text-[11px] text-slate-300 font-technical uppercase tracking-widest">
                  <span className="material-symbols-outlined text-[16px] text-primary">description</span> {selectedFile.name}
                </div>
                <div className="flex gap-2">
                  {tags.map((tag, idx) => {
                    const isCS = tag.includes('cs') || tag.includes('ai');
                    const bgClass = isCS ? 'bg-primary/10 text-primary border-primary/30' : 'bg-[#15151A] text-on-surface-variant border-[#2A2A35]';
                    return (
                      <span key={idx} className={`${bgClass} text-[9px] px-3 py-1 font-technical tracking-[0.2em] border rounded-sm uppercase`}>
                        {tag}
                      </span>
                    )
                  })}
                </div>
              </div>
              
              <div className="px-10 py-12 max-w-4xl mx-auto">
                <article className="prose prose-invert prose-p:text-slate-300 max-w-none">
                  {loading ? (
                    <div className="text-primary animate-pulse font-mono flex items-center gap-2"><span className="material-symbols-outlined">sync</span> Decrypting stream...</div>
                  ) : (
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm, remarkMath]}
                      rehypePlugins={[rehypeRaw, rehypeKatex]}
                      components={{
                        h1: ({node, ...props}) => <h1 className="text-4xl font-headline font-black text-on-surface mt-10 mb-8 pb-4 border-b-2 border-primary/20 tracking-tight" {...props} />,
                        h2: ({node, ...props}) => <h2 className="text-2xl font-headline font-bold text-primary/90 mt-12 mb-6 tracking-tight flex items-center gap-3 before:content-[''] before:block before:w-2 before:h-8 before:bg-primary/50 before:rounded-sm" {...props} />,
                        h3: ({node, ...props}) => <h3 className="text-xl font-headline font-semibold text-tertiary mt-8 mb-4 border-b border-tertiary/20 pb-2" {...props} />,
                        
                        table: ({node, ...props}) => <div className="overflow-x-auto my-8 border border-[#2A2A35] rounded-sm bg-[#15151A]/50"><table className="w-full text-sm text-left align-middle" {...props} /></div>,
                        th: ({node, ...props}) => <th className="px-4 py-3 text-[10px] uppercase tracking-[0.2em] text-slate-400 font-technical border-b border-[#2A2A35] bg-[#15151A]" {...props} />,
                        td: ({node, ...props}) => <td className="px-4 py-3 border-b border-[#2A2A35]/30 hover:bg-[#1f1f26] transition-colors" {...props} />,
                        
                        a: ({node, href, children, ...props}) => {
                          if (href?.startsWith('#obsidian:')) {
                            const target = decodeURIComponent(href.replace('#obsidian:', ''));
                            return (
                              <button 
                                onClick={(e) => { e.preventDefault(); handleLinkClick(target); }}
                                className="text-primary font-technical tracking-wide text-sm px-1.5 py-0.5 bg-primary/10 hover:bg-primary/20 border border-primary/20 hover:border-primary/50 transition-colors rounded-sm mx-1 cursor-pointer align-baseline"
                              >
                                {children}
                              </button>
                            );
                          }
                          
                          if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
                            const target = decodeURIComponent(href).replace(/\.md$/, '');
                            return (
                              <button 
                                onClick={(e) => { e.preventDefault(); handleLinkClick(target); }}
                                className="text-primary hover:underline decoration-primary/40 underline-offset-4 cursor-pointer align-baseline"
                              >
                                {children}
                              </button>
                            );
                          }

                          if (!href) return <span className="text-slate-500 line-through">{children}</span>;

                          return <a className="text-primary hover:underline decoration-primary/40 underline-offset-4 cursor-pointer" href={href} target="_blank" rel="noreferrer" {...props}>{children}</a>;
                        },
                        
                        code: ({node, className, children, ...props}) => {
                          const match = /language-(\w+)/.exec(className || '');
                          const isInline = !match && !String(children).includes('\\n');
                          return !isInline ? (
                            <div className="my-6 bg-[#15151A] rounded-sm border border-[#2A2A35] shadow-xl overflow-hidden">
                              <div className="flex items-center justify-between px-4 py-2 border-b border-[#2A2A35] bg-[#0A0A0C]">
                                <span className="text-[9px] font-technical text-slate-500 uppercase tracking-[0.2em]">{match ? match[1] : 'code'}</span>
                              </div>
                              <pre className="p-4 font-technical text-sm leading-relaxed text-[#a6ffb6] overflow-x-auto"><code className={className} {...props}>{children}</code></pre>
                            </div>
                          ) : (
                            <code className="font-technical text-primary bg-primary/10 px-1.5 py-0.5 rounded-sm text-[0.85em]" {...props}>{children}</code>
                          )
                        }
                      }}
                    >
                      {cleanContent}
                    </ReactMarkdown>
                  )}
                </article>
              </div>
            </>
          ) : (
            <div className="h-full flex items-center justify-center flex-col text-[#2A2A35] gap-4">
              <span className="material-symbols-outlined text-[100px] font-light">account_tree</span>
              <p className="font-technical text-xs uppercase tracking-widest text-slate-600">Initialize Memory Bridge</p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default App;
