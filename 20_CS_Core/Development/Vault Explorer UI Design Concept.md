---
tags:
  - field/cs
  - subject/development
  - concept/vault-ui
---

[[T.O.C (Development).md|Up to Development]]

<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Vault Explorer - Kinetic Intelligence</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&amp;family=Inter:wght@300;400;500;600;700&amp;family=Fira+Code:wght@400;500&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#00D4FF",
                        "primary-container": "#004c5e",
                        "on-primary-container": "#00d2fd",
                        "surface": "#0A0A0C",
                        "surface-container-low": "#15151A",
                        "surface-container": "#19191c",
                        "on-surface": "#f9f5f8",
                        "on-surface-variant": "#adaaad",
                        "outline-variant": "#2A2A35",
                        "tertiary": "#a6ffb6"
                    },
                    fontFamily: {
                        "headline": ["Space Grotesk"],
                        "body": ["Inter"],
                        "label": ["Inter"],
                        "mono": ["Fira Code", "monospace"],
                        "technical": ["JetBrains Mono", "monospace"]
                    },
                    borderRadius: {"DEFAULT": "0.125rem", "lg": "0.25rem", "xl": "0.5rem", "full": "0.75rem"},
                },
            },
        }
    </script>
<style>
        .glass-panel {
            backdrop-filter: blur(20px);
            background: rgba(19, 19, 21, 0.8);
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .active-glow {
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
            border: 1px solid rgba(0, 212, 255, 0.4);
        }
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-track {
            background: #000000;
        }
        ::-webkit-scrollbar-thumb {
            background: #2A2A35;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00D4FF;
        }
    </style>
</head>
<body class="bg-[#000000] text-on-surface font-body selection:bg-primary/30">
<!-- Top Navigation Bar -->
<header class="bg-[#000000]/80 backdrop-blur-xl flex justify-between items-center w-full px-6 h-16 sticky top-0 z-50 border-b border-[#2A2A35] shadow-[0_4px_20px_rgba(0,0,0,0.5)]">
<div class="flex items-center gap-4">
<span class="text-lg font-black tracking-widest uppercase text-primary font-headline">Vault Explorer</span>
<nav class="hidden md:flex gap-6 ml-8">
<a class="text-slate-400 font-medium hover:text-primary transition-opacity font-label text-xs uppercase tracking-widest" href="#">Recent</a>
<a class="text-slate-400 font-medium hover:text-primary transition-opacity font-label text-xs uppercase tracking-widest" href="#">Starred</a>
<a class="text-slate-400 font-medium hover:text-primary transition-opacity font-label text-xs uppercase tracking-widest" href="#">Archived</a>
</nav>
</div>
<div class="flex items-center gap-6">
<div class="relative hidden lg:block">
<input class="bg-[#15151A] border-none text-xs px-4 py-1.5 w-64 rounded-sm focus:ring-1 focus:ring-primary/50 text-on-surface-variant font-mono" placeholder="Search Kernel..." type="text"/>
<span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-primary text-sm">search</span>
</div>
<div class="flex items-center gap-4">
<button class="text-slate-400 hover:text-primary transition-colors"><span class="material-symbols-outlined">notifications</span></button>
<button class="text-slate-400 hover:text-primary transition-colors"><span class="material-symbols-outlined text-[20px]">terminal</span></button>
<div class="w-8 h-8 rounded border border-outline-variant flex items-center justify-center overflow-hidden">
<img alt="Kernel Admin" class="w-full h-full object-cover" data-alt="minimalist 3d avatar of a technical system administrator with a cybernetic aesthetic and soft blue lighting" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBbLcH8cgWpZVUfTnRDCQwa69NJ9NYlMCRkdMOsQeZ3UhFRHroy4iAP8dIOPEDUhfMtoVvLyyb_HPQa7fHee7fljhPLxHAKd-E0uj2xyLBtUy5HJan0NCnmSXV83Otj1wO5NN_9vP8uY5GZFxiMibcZ0p12AGh4iDlluzADnfc4z0Lu62xa_rMO5D5gbhU5uENgBlIrsYHd-oLRBiKXKQoR7az2nWAT_luD3jAOYaZ7DoL9pIfgSc9TyeW_TxnhvMOGMEbhVapvLtk"/>
</div>
</div>
</div>
</header>
<div class="flex h-[calc(100vh-64px)] overflow-hidden">
<!-- Sidebar: File Tree (Pane 1) -->
<aside class="w-[250px] flex-shrink-0 bg-[#15151A] flex flex-col border-r border-[#2A2A35] overflow-y-auto">
<div class="p-4 mb-4">
<button class="w-full bg-primary/5 hover:bg-primary/10 border border-primary/20 text-primary py-2 px-4 rounded-sm font-headline font-bold text-xs tracking-widest uppercase flex items-center justify-center gap-2 transition-all">
<span class="material-symbols-outlined text-[16px]">add</span> New Note
            </button>
</div>
<nav class="flex-1 px-4 space-y-1">
<div class="flex items-center gap-2 py-1 text-slate-400 hover:text-slate-200 transition-colors cursor-pointer font-label text-sm">
<span class="material-symbols-outlined text-[18px]">keyboard_arrow_down</span>
<span class="material-symbols-outlined text-[18px]">folder_open</span>
                Vault
            </div>
<div class="pl-4 space-y-1">
<div class="flex items-center gap-2 py-1 text-slate-400 hover:text-slate-200 cursor-pointer font-label text-sm">
<span class="material-symbols-outlined text-[18px]">keyboard_arrow_down</span>
<span class="material-symbols-outlined text-[18px]">folder</span>
                    10_University
                </div>
<div class="pl-4 space-y-1">
<div class="flex items-center gap-2 py-1 text-slate-400 hover:text-slate-200 cursor-pointer font-label text-sm">
<span class="material-symbols-outlined text-[18px]">keyboard_arrow_down</span>
<span class="material-symbols-outlined text-[18px]">folder</span>
                        Semester_01
                    </div>
<div class="pl-4">
<div class="flex items-center gap-2 px-3 py-1.5 text-primary font-bold bg-primary/5 cursor-pointer font-label text-sm active-glow rounded-sm">
<span class="material-symbols-outlined text-[18px]" style="font-variation-settings: 'FILL' 1;">folder</span>
                            Artificial Intelligence
                        </div>
</div>
</div>
</div>
<div class="pt-8 space-y-1">
<div class="flex items-center gap-2 py-1.5 text-slate-500 hover:text-slate-300 transition-colors cursor-pointer font-label text-sm">
<span class="material-symbols-outlined text-[18px]">search</span>
                    Search
                </div>
<div class="flex items-center gap-2 py-1.5 text-slate-500 hover:text-slate-300 transition-colors cursor-pointer font-label text-sm">
<span class="material-symbols-outlined text-[18px]">hub</span>
                    Graph
                </div>
<div class="flex items-center gap-2 py-1.5 text-slate-500 hover:text-slate-300 transition-colors cursor-pointer font-label text-sm">
<span class="material-symbols-outlined text-[18px]">settings</span>
                    Settings
                </div>
</div>
</nav>
<div class="p-4 border-t border-[#2A2A35]/50">
<div class="flex items-center gap-2 py-1 text-slate-600 hover:text-slate-400 transition-colors cursor-pointer font-label text-[10px] uppercase tracking-widest">
<span class="material-symbols-outlined text-[14px]">description</span>
                Docs
            </div>
<div class="flex items-center gap-2 py-1 text-slate-600 hover:text-slate-400 transition-colors cursor-pointer font-label text-[10px] uppercase tracking-widest">
<span class="material-symbols-outlined text-[14px]">help_outline</span>
                Support
            </div>
<div class="mt-2">
<span class="font-technical text-[9px] text-slate-700 uppercase tracking-tighter">v1.0.4-kernel</span>
</div>
</div>
</aside>
<!-- Hub: Table of Contents (Pane 2) -->
<main class="flex-1 bg-surface-container-low overflow-y-auto border-r border-[#2A2A35]">
<div class="p-8">
<div class="mb-10">
<h1 class="font-headline text-3xl font-bold tracking-tight text-on-surface mb-2">Artificial Intelligence Notes</h1>
<p class="text-on-surface-variant font-label text-sm max-w-lg opacity-60">Knowledge cluster for semester 01 computational logic and heuristics.</p>
</div>
<div class="w-full">
<div class="grid grid-cols-12 gap-4 px-4 py-3 text-[10px] uppercase tracking-[0.2em] text-slate-500 font-technical border-b border-[#2A2A35]">
<div class="col-span-1">ID</div>
<div class="col-span-3">Category</div>
<div class="col-span-8">Content</div>
</div>
<div class="divide-y divide-[#2A2A35]/30">
<!-- Data Grid Row -->
<div class="grid grid-cols-12 gap-4 px-4 py-4 hover:bg-[#1f1f26] transition-colors group cursor-pointer">
<div class="col-span-1 font-technical text-xs text-slate-500 py-1">1.1.1</div>
<div class="col-span-3">
<span class="bg-primary/5 text-primary text-[9px] px-2 py-1 font-technical border border-primary/20 rounded-sm">SEARCH_ALGO</span>
</div>
<div class="col-span-8">
<h3 class="text-primary font-medium text-sm group-hover:underline underline-offset-4 decoration-primary/40">A* Algorithm &amp; Informed Search</h3>
<p class="text-on-surface-variant text-[11px] mt-1 line-clamp-1 opacity-70">Pathfinding using f(n) = g(n) + h(n) cost functions.</p>
</div>
</div>
<div class="grid grid-cols-12 gap-4 px-4 py-4 hover:bg-[#1f1f26] transition-colors group cursor-pointer">
<div class="col-span-1 font-technical text-xs text-slate-500 py-1">1.1.2</div>
<div class="col-span-3">
<span class="bg-primary/5 text-primary text-[9px] px-2 py-1 font-technical border border-primary/20 rounded-sm">LOGIC</span>
</div>
<div class="col-span-8">
<h3 class="text-primary font-medium text-sm group-hover:underline underline-offset-4 decoration-primary/40">Propositional Calculus</h3>
<p class="text-on-surface-variant text-[11px] mt-1 line-clamp-1 opacity-70">Foundational logic gates and truth tables in AI systems.</p>
</div>
</div>
<div class="grid grid-cols-12 gap-4 px-4 py-4 hover:bg-[#1f1f26] transition-colors group cursor-pointer">
<div class="col-span-1 font-technical text-xs text-slate-500 py-1">1.1.3</div>
<div class="col-span-3">
<span class="bg-tertiary/5 text-tertiary text-[9px] px-2 py-1 font-technical border border-tertiary/20 rounded-sm">HEURISTICS</span>
</div>
<div class="col-span-8">
<h3 class="text-primary font-medium text-sm group-hover:underline underline-offset-4 decoration-primary/40">Admissible Heuristics</h3>
<p class="text-on-surface-variant text-[11px] mt-1 line-clamp-1 opacity-70">Criteria for optimality in informed search patterns.</p>
</div>
</div>
</div>
</div>
</div>
</main>
<!-- Viewer: Markdown Renderer (Pane 3) -->
<section class="flex-[2] bg-[#0A0A0C] overflow-y-auto">
<div class="sticky top-0 bg-[#0A0A0C]/90 backdrop-blur-md px-10 py-4 flex items-center justify-between z-10 border-b border-[#2A2A35]">
<button class="flex items-center gap-2 text-[10px] text-primary font-technical uppercase tracking-widest hover:opacity-70 transition-opacity">
<span class="material-symbols-outlined text-[16px]">arrow_back</span> Up to T.O.C
            </button>
<div class="flex gap-2">
<span class="bg-primary/10 text-primary text-[9px] px-3 py-1 font-technical tracking-widest border border-primary/20 rounded-sm uppercase">field/cs</span>
<span class="bg-[#15151A] text-on-surface-variant text-[9px] px-3 py-1 font-technical tracking-widest border border-[#2A2A35] rounded-sm uppercase">concept/search</span>
</div>
</div>
<div class="px-10 py-12 max-w-3xl mx-auto">
<article class="prose prose-invert max-w-none">
<h1 class="font-headline text-4xl font-bold tracking-tight text-on-surface mb-8 border-l-4 border-primary pl-6">1.1.1 - A* Algorithm</h1>
<h2 class="font-headline text-xl font-semibold text-primary/80 mt-10 mb-4 tracking-tight uppercase tracking-[0.1em]">Overview</h2>
<p class="text-on-surface-variant leading-relaxed mb-6">
                    The A* Algorithm is an informed search strategy that uses a combination of path cost and estimated distance to the goal. Unlike Dijkstra’s, it prioritizes nodes that appear closer to the solution based on <span class="text-primary border-b border-primary/30 cursor-help hover:bg-primary/10 transition-colors font-technical">[[Search Heuristics]]</span>.
                </p>
<div class="my-8 bg-[#15151A] p-6 rounded-sm border border-[#2A2A35] shadow-xl">
<div class="flex items-center justify-between mb-4 border-b border-[#2A2A35] pb-2">
<span class="text-[9px] font-technical text-slate-500 uppercase tracking-[0.2em]">Implementation : Python</span>
<button class="text-slate-500 hover:text-primary transition-colors"><span class="material-symbols-outlined text-sm">content_copy</span></button>
</div>
<pre class="font-technical text-sm leading-relaxed text-tertiary overflow-x-auto selection:bg-tertiary/20"><code>def a_star_search(graph, start, goal):
    # f(n) = g(n) + h(n)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break
            
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost &lt; cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current</code></pre>
</div>
<h2 class="font-headline text-xl font-semibold text-primary/80 mt-12 mb-4 tracking-tight uppercase tracking-[0.1em]">Mathematical Logic</h2>
<p class="text-on-surface-variant leading-relaxed mb-6">
                    The core equation governing the node selection is defined as <code class="font-technical text-primary bg-primary/10 px-1.5 py-0.5 rounded-sm">f(n) = g(n) + h(n)</code>. For the algorithm to be optimal, the heuristic function must be admissible—meaning it never overestimates the actual cost to reach the goal.
                </p>
<!-- Editorial Technical Graphic Area -->
<div class="mt-12 mb-20 relative aspect-video bg-[#000000] border border-[#2A2A35] overflow-hidden flex items-center justify-center group">
<div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(#00D4FF 1px, transparent 1px); background-size: 20px 20px;"></div>
<img class="w-full h-full object-cover opacity-40 group-hover:opacity-60 transition-opacity duration-700" data-alt="abstract architectural rendering of a glowing network grid with blue nodes connected by digital lines in a dark void" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDvs2UL0IDV9taOyC04RobgpKPTgHHiwZSLZOYtbHVZAsqlrM-mpUEfaEQS1Kkd2s6_zTCX6RVrlqnvO6gxwz4ce-9UQLPU1JLJGS-BUpH6KYIpCXIfy2UHAMzcieIimAsUDoTMEZNVIvA1zrw4JfTWrWTm_f77pFkGv6VaM5eZvKKZn-VKiJ2uDxQR5NBzESCelNFr7i-by7ZlRzcbegR2MnrlWxpt3Q0KmPy1BUwJFJ-JNd5ovzY5FybnIrto1PpLMBF6kvm3AEU"/>
<div class="absolute bottom-6 left-6 flex flex-col">
<span class="font-technical text-[9px] text-primary uppercase tracking-[0.3em] mb-1">Visualizing Heuristic Flow</span>
<span class="font-headline text-lg font-bold text-on-surface tracking-tight">Manhattan Distance vs. Euclidean</span>
</div>
</div>
</article>
</div>
</section>
</div>
</body></html>