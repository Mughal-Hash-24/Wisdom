import React, { useState, useEffect, useMemo, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import ForceGraph2D from 'react-force-graph-2d';
import Fuse from 'fuse.js';
import 'katex/dist/katex.min.css';

const API_BASE = '/api';

interface FileNode {
  name: string;
  path: string;
  isDir: boolean;
  children?: FileNode[];
}

const GRAPH_COLORS: Record<number, string> = {
  1: '#00d4ff', // CS (Neon Blue)
  2: '#ff9d00', // Math (Vivid Orange)
  3: '#10b981', // Humanities (Emerald Green)
  4: '#f43f5e', // AI (Cyber Pink)
  5: '#0ea5e9', // OS (Azure)
  6: '#ffffff', // Maps (White)
  0: '#4b5563'  // Default (Slate)
};

function CommandPalette({ isOpen, onClose, fileMap, onSelect }: any) {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const docs = useMemo(() => {
    return Object.keys(fileMap).map(k => ({
      path: k,
      content: fileMap[k],
      name: k.split('/').pop()?.replace('.md', '') || k
    }));
  }, [fileMap]);

  const fuse = useMemo(() => new Fuse(docs, { keys: ['name', 'content'], threshold: 0.3 }), [docs]);
  const results = query ? fuse.search(query).slice(0, 8).map(r => r.item) : docs.slice(0, 8);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    } else if (!isOpen) {
      setQuery('');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex justify-center items-start pt-[15vh]" onClick={onClose}>
      <div 
        className="bg-[#0A0A0C] border border-[#2A2A35] w-full max-w-2xl rounded-sm shadow-[0_0_50px_rgba(0,212,255,0.1)] flex flex-col max-h-[60vh] overflow-hidden" 
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center border-b border-[#2A2A35] px-6">
          <span className="material-symbols-outlined text-primary mr-3">search</span>
          <input 
            ref={inputRef}
            value={query} 
            onChange={e => setQuery(e.target.value)} 
            className="w-full bg-transparent py-5 text-on-surface outline-none text-lg font-headline placeholder:text-[#2A2A35]" 
            placeholder="Search Vault Nodes..." 
          />
          <div className="text-[10px] text-[#2A2A35] font-technical uppercase border border-[#2A2A35] px-2 py-1 rounded-sm">ESC to close</div>
        </div>
        
        <div className="flex-1 overflow-y-auto">
          {results.length > 0 ? results.map((res: any, idx: number) => (
             <div 
               key={idx} 
               onClick={() => { onSelect(res.path); onClose(); }} 
               className="p-4 hover:bg-[#15151A] cursor-pointer border-b border-[#2A2A35]/30 group transition-colors"
             >
               <div className="text-primary font-technical tracking-widest uppercase text-xs mb-1 group-hover:text-[#00d4ff] flex items-center justify-between">
                 <span>{res.name}</span>
                 <span className="material-symbols-outlined text-[14px] opacity-0 group-hover:opacity-100 transition-opacity text-[#00d4ff]">keyboard_return</span>
               </div>
               <div className="text-slate-500 text-[10px] truncate uppercase font-technical opacity-60 tracking-wider flex items-center gap-2">
                 <span className="material-symbols-outlined text-[12px]">folder</span> {res.path}
               </div>
             </div>
          )) : (
            <div className="p-10 text-center text-slate-500 font-technical text-xs tracking-widest uppercase">
              No matching nodes found.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


function App() {
  const [tree, setTree] = useState<FileNode[]>([]);
  const [fileMap, setFileMap] = useState<Record<string, string>>({});
  const [graphData, setGraphData] = useState<any>({ nodes: [], links: [] });
  
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  
  const [viewMode, setViewMode] = useState<'doc' | 'graph'>('doc');
  const [searchOpen, setSearchOpen] = useState(false);
  const [graphDims, setGraphDims] = useState({ w: 800, h: 600 });
  const graphContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${API_BASE}/tree.json`).then(res => res.json()).then(setTree).catch(console.error);
    fetch(`${API_BASE}/files.json`).then(res => res.json()).then(setFileMap).catch(console.error);
    fetch(`${API_BASE}/graph.json`).then(res => res.json()).then(setGraphData).catch(console.error);
  }, []);

  // Window resizing for Graph
  useEffect(() => {
    const updateDims = () => {
      if (graphContainerRef.current) {
        setGraphDims({
          w: graphContainerRef.current.clientWidth,
          h: graphContainerRef.current.clientHeight
        });
      }
    };
    window.addEventListener('resize', updateDims);
    // Slight delay to ensure flex layout mounted
    setTimeout(updateDims, 50);
    return () => window.removeEventListener('resize', updateDims);
  }, [viewMode]);

  // Global Keybinds
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setSearchOpen(prev => !prev);
      }
      if (e.key === 'Escape') {
        setSearchOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const toggleFolder = (path: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const next = new Set(expandedFolders);
    if (next.has(path)) next.delete(path); else next.add(path);
    setExpandedFolders(next);
  };

  const handleSelectNode = (node: FileNode) => {
    if (!node.isDir) {
      setViewMode('doc');
      setSelectedFile(node);
      setLoading(true);
      setTimeout(() => {
        setFileContent(fileMap[node.path] || '---\nEmpty node\n---\nTarget missing or corrupted.');
        setLoading(false);
      }, 150);
    }
  };
  
  const handleSelectPath = (fetchPath: string) => {
    // Reconstruct FileNode for simplicity
    handleSelectNode({
      name: fetchPath.split(/[/\\]/).pop() || fetchPath,
      path: fetchPath,
      isDir: false
    });
  };

  const findNodeByName = (nodes: FileNode[], targetName: string): FileNode | null => {
    let cleanTarget = targetName.split('#')[0].split('^')[0].replace(/\.md$/i, '').toLowerCase().trim();
    const parts = cleanTarget.split(/[/\\]/);
    const baseTarget = parts[parts.length - 1].replace(/\s+/g, ''); 

    for (const node of nodes) {
      if (!node.isDir) {
        const nodeBase = node.name.replace(/\.md$/i, '').toLowerCase().replace(/\s+/g, '');
        if (nodeBase === baseTarget) return node;
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
                if (tocNode) handleSelectNode(tocNode);
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
    return tagsLine.replace('tags:', '').split(',').map(t => t.trim().replace(/"|'/g, '').replace(/^- |^\[|\]$/g, '').trim()).filter(t => t);
  };

  const tags = fileContent ? extractTags(fileContent) : [];
  let cleanContent = fileContent ? fileContent.replace(/^---\n[\s\S]*?\n---/, '') : '';

  cleanContent = cleanContent.replace(/(!?)\[\[([\s\S]*?)\]\]/g, (match, prefix, p1) => {
    if (prefix === '!') return match; 
    const parts = p1.split('|');
    const target = parts[0].replace(/\\$/, '').trim(); 
    const text = parts.length > 1 ? parts[1].trim() : target;
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
  cleanContent = cleanContent.replace(/^> /gm, '');

  return (
    <div className="bg-[#000000] text-on-surface font-body selection:bg-primary/30 h-screen flex flex-col overflow-hidden">
      
      <CommandPalette 
        isOpen={searchOpen} 
        onClose={() => setSearchOpen(false)} 
        fileMap={fileMap} 
        onSelect={handleSelectPath} 
      />

      <header className="bg-[#000000]/80 backdrop-blur-xl flex justify-between items-center w-full px-6 h-14 border-b border-[#2A2A35]">
        <div className="flex items-center gap-4">
          <span className="text-sm font-black tracking-widest uppercase text-primary font-headline">Vault Explorer</span>
          
          <div className="flex items-center bg-[#15151A] rounded-sm ml-6 border border-[#2A2A35] overflow-hidden">
            <button 
              onClick={() => setViewMode('doc')}
              className={`px-4 py-1.5 text-[10px] uppercase font-technical tracking-widest transition-colors flex items-center gap-2
                ${viewMode === 'doc' ? 'bg-primary/20 text-primary' : 'text-slate-500 hover:text-slate-300'}`}
            >
              <span className="material-symbols-outlined text-[14px]">article</span> Document
            </button>
            <button 
              onClick={() => setViewMode('graph')}
              className={`px-4 py-1.5 text-[10px] uppercase font-technical tracking-widest transition-colors flex items-center gap-2 border-l border-[#2A2A35]
                ${viewMode === 'graph' ? 'bg-primary/20 text-primary' : 'text-slate-500 hover:text-slate-300'}`}
            >
              <span className="material-symbols-outlined text-[14px]">scatter_plot</span> Graph
            </button>
          </div>
        </div>

        <div className="flex items-center gap-4">
           <button 
             onClick={() => setSearchOpen(true)}
             className="flex items-center gap-3 bg-[#15151A] border border-[#2A2A35] hover:border-primary/50 text-slate-400 hover:text-primary transition-colors px-4 py-1.5 rounded-sm"
           >
              <span className="material-symbols-outlined text-[14px]">search</span>
              <span className="text-[10px] font-technical uppercase tracking-widest">Search</span>
              <div className="flex bg-[#0A0A0C] border border-[#2A2A35] px-1.5 rounded-sm text-[9px] font-mono">
                ⌘K
              </div>
           </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden relative">
        <aside className="w-[320px] flex-shrink-0 bg-[#0A0A0C] flex flex-col border-r border-[#2A2A35] overflow-y-auto z-10">
          <div className="p-4 mb-2 sticky top-0 bg-[#0A0A0C]/90 backdrop-blur-sm z-10 border-b border-[#2A2A35]">
            <div className="text-[9px] uppercase tracking-[0.2em] text-slate-500 font-technical mb-2">Workspace</div>
            <div className="text-primary text-xs font-technical tracking-wider break-all bg-primary/5 p-2 rounded-sm border border-primary/20">
              Kybernetes Architecture
            </div>
          </div>
          <nav className="flex-1 px-2 pb-10">
            {tree.length > 0 ? renderTree(tree) : <div className="text-center text-slate-500 text-xs mt-10 animate-pulse">Scanning Vault...</div>}
          </nav>
        </aside>

        {viewMode === 'doc' ? (
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
                  <article className="prose prose-invert prose-p:text-[15px] prose-p:leading-relaxed prose-p:text-slate-300 max-w-none">
                    {loading ? (
                      <div className="text-primary animate-pulse font-mono flex items-center gap-2">
                        <span className="material-symbols-outlined">sync</span> Decrypting stream...
                      </div>
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
                            const isInline = !match && !String(children).includes('\n');
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
                <p className="font-technical text-xs uppercase tracking-widest text-slate-600">Select a memory node</p>
              </div>
            )}
          </section>
        ) : (
          <section className="flex-1 bg-[#060608] relative" ref={graphContainerRef}>
            {graphData.nodes.length > 0 && (
              <ForceGraph2D
                width={graphDims.w}
                height={graphDims.h}
                graphData={graphData}
                nodeLabel="label"
                nodeRelSize={4}
                nodeColor={(node: any) => GRAPH_COLORS[node.group] || GRAPH_COLORS[0]}
                nodeVal={(node: any) => node.val}
                linkColor={() => '#2A2A35'}
                backgroundColor="#060608"
                linkDirectionalParticles={2}
                linkDirectionalParticleSpeed={d => 0.004}
                onNodeClick={(node: any) => {
                  handleSelectPath(node.path);
                }}
              />
            )}
            <div className="absolute top-4 left-4 bg-[#0A0A0C]/80 backdrop-blur-md border border-[#2A2A35] p-4 rounded-sm">
               <h3 className="text-primary font-headline text-sm font-bold tracking-widest uppercase mb-2">Kybernetes Graph</h3>
               <div className="text-[10px] font-technical uppercase text-slate-500 tracking-wider space-y-1">
                 <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#00d4ff]"></span> CompSci</div>
                 <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#f43f5e]"></span> A.I</div>
                 <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#10b981]"></span> Humanities</div>
                 <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-[#ffffff]"></span> System Map</div>
               </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

export default App;
