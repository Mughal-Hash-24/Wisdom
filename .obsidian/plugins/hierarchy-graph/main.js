/* 
   HIERARCHY GRAPH PLUGIN (SAFE MODE)
*/

const obsidian = require('obsidian');

const VIEW_TYPE_HIERARCHY = "hierarchy-graph-view";

class HierarchyGraphView extends obsidian.ItemView {
    constructor(leaf) {
        super(leaf);
        this.nodes = [];
        this.links = [];
        this.transform = { x: 0, y: 0, k: 1 };
        this.isDragging = false;
        this.dragStart = { x: 0, y: 0 };
        this.animationFrameId = null;
    }

    getViewType() {
        return VIEW_TYPE_HIERARCHY;
    }

    getDisplayText() {
        return "Hierarchy Graph";
    }

    getIcon() {
        return "graph";
    }

    async onOpen() {
        console.log("Hierarchy Graph: Opening View");
        const container = this.containerEl.children[1];
        container.empty();
        container.addClass("hierarchy-graph-container");

        this.canvas = document.createElement("canvas");
        this.canvas.addClass("hierarchy-graph-canvas");
        container.appendChild(this.canvas);
        
        this.ctx = this.canvas.getContext("2d");

        // Controls
        const controls = document.createElement("div");
        controls.addClass("hierarchy-graph-controls");
        
        const refreshBtn = document.createElement("button");
        refreshBtn.innerText = "Refresh Graph";
        refreshBtn.onclick = () => this.refreshData();
        controls.appendChild(refreshBtn);

        const resetBtn = document.createElement("button");
        resetBtn.innerText = "Reset View";
        resetBtn.onclick = () => {
             this.transform = { x: this.canvas.width / 2, y: this.canvas.height / 2, k: 1 };
        };
        controls.appendChild(resetBtn);

        container.appendChild(controls);

        this.setupInteractions();
        this.refreshData();
        
        this.resizeObserver = new ResizeObserver(() => {
            this.resizeCanvas();
        });
        this.resizeObserver.observe(container);
    }

    resizeCanvas() {
        const container = this.containerEl.children[1];
        if(!container) return;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
        if (this.nodes.length === 0) {
             this.transform.x = this.canvas.width / 2;
             this.transform.y = this.canvas.height / 2;
        }
    }

    setupInteractions() {
        this.canvas.addEventListener("wheel", (e) => {
            e.preventDefault();
            const zoomSensitivity = 0.001;
            const delta = -e.deltaY * zoomSensitivity;
            this.transform.k = Math.max(0.1, Math.min(10, this.transform.k + delta));
        });

        this.canvas.addEventListener("mousedown", (e) => {
            this.isDragging = true;
            this.dragStart = { x: e.clientX, y: e.clientY };
        });

        window.addEventListener("mousemove", (e) => {
            if (!this.isDragging) return;
            const dx = e.clientX - this.dragStart.x;
            const dy = e.clientY - this.dragStart.y;
            this.transform.x += dx;
            this.transform.y += dy;
            this.dragStart = { x: e.clientX, y: e.clientY };
        });

        window.addEventListener("mouseup", () => {
            this.isDragging = false;
        });
    }

    refreshData() {
        console.log("Hierarchy Graph: Refreshing Data");
        const files = this.app.vault.getAllLoadedFiles();
        this.nodes = [];
        this.links = [];
        const fileMap = {};

        files.forEach(file => {
            const depth = file.path.split("/").length - 1;
            
            let color = "#555";
            if (depth === 0) color = "#ffffff"; 
            else if (file.path.includes("40_Projects")) color = "#ff00d4";
            else if (file.path.includes("20_CS_Core")) color = "#ffd700";
            else if (file.path.includes("10_University")) color = "#00aaff";
            else if (file.path.includes("00_Inbox")) color = "#ff3333";
            else if (file.path.includes("30_Knowledge")) color = "#00ff00";
            
            const radius = Math.max(2000, 25000 / (depth + 1));
            
            const node = {
                id: file.path,
                name: file.name,
                depth: depth,
                x: (Math.random() - 0.5) * 100,
                y: (Math.random() - 0.5) * 100,
                vx: 0, vy: 0,
                radius: radius,
                color: color
            };
            
            this.nodes.push(node);
            fileMap[file.path] = node;
        });

        files.forEach(file => {
            if (file.parent) {
                const parentNode = fileMap[file.parent.path];
                const childNode = fileMap[file.path];
                if (parentNode && childNode) {
                    const length = 0;
                    this.links.push({ source: parentNode, target: childNode, length: length });
                }
            }
        });

        if (this.animationFrameId) cancelAnimationFrame(this.animationFrameId);
        this.runSimulation();
    }

    runSimulation() {
        const repulsion = 1;
        const centerPull = 0.8;
        
        this.nodes.forEach(node => {
            this.nodes.forEach(other => {
                if (node === other) return;
                const dx = node.x - other.x;
                const dy = node.y - other.y;
                const distSq = dx * dx + dy * dy || 1;
                const force = repulsion / distSq;
                node.vx += (dx * force);
                node.vy += (dy * force);
            });
            node.vx -= node.x * centerPull;
            node.vy -= node.y * centerPull;
        });

        this.links.forEach(link => {
            const dx = link.target.x - link.source.x;
            const dy = link.target.y - link.source.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const displacement = dist - link.length;
            const k = 0.9;
            
            const fx = (dx / dist) * k * displacement;
            const fy = (dy / dist) * k * displacement;
            
            link.source.vx += fx; link.source.vy += fy;
            link.target.vx -= fx; link.target.vy -= fy;
        });

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.save();
        this.ctx.translate(this.transform.x, this.transform.y);
        this.ctx.scale(this.transform.k, this.transform.k);

        this.ctx.strokeStyle = "#444";
        this.ctx.lineWidth = 1;
        this.links.forEach(link => {
            this.ctx.beginPath();
            this.ctx.moveTo(link.source.x, link.source.y);
            this.ctx.lineTo(link.target.x, link.target.y);
            this.ctx.stroke();
        });

        this.nodes.forEach(node => {
            node.x += node.vx * 0.5;
            node.y += node.vy * 0.5;
            node.vx *= 0.9;
            node.vy *= 0.9;

            this.ctx.fillStyle = node.color;
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            this.ctx.fill();
            
            if (node.radius > 5) {
                this.ctx.fillStyle = "#ccc";
                this.ctx.font = `${node.radius}px sans-serif`;
                this.ctx.fillText(node.name, node.x + node.radius + 2, node.y + node.radius / 2);
            }
        });
        
        this.ctx.restore();
        this.animationFrameId = requestAnimationFrame(() => this.runSimulation());
    }

    async onClose() {
        if (this.animationFrameId) cancelAnimationFrame(this.animationFrameId);
    }
}

module.exports = class HierarchyGraphPlugin extends obsidian.Plugin {
    async onload() {
        console.log("Hierarchy Graph: Plugin Loaded");
        this.registerView(
            VIEW_TYPE_HIERARCHY,
            (leaf) => new HierarchyGraphView(leaf)
        );

        this.addRibbonIcon('graph', 'Open Hierarchy Graph', () => {
            this.activateView();
        });

        this.addCommand({
            id: 'open-hierarchy-graph-cmd',
            name: 'Open Hierarchy Graph',
            callback: () => {
                this.activateView();
            }
        });
    }

    async activateView() {
        this.app.workspace.detachLeavesOfType(VIEW_TYPE_HIERARCHY);

        await this.app.workspace.getRightLeaf(false).setViewState({
            type: VIEW_TYPE_HIERARCHY,
            active: true,
        });

        this.app.workspace.revealLeaf(
            this.app.workspace.getLeavesOfType(VIEW_TYPE_HIERARCHY)[0]
        );
    }
};