# Musannif — Detailed Implementation Plan
**Date:** 2026-07-03
**Status:** Ready for implementation
**Language:** Python 3.12+
**Package manager:** uv

---

## Reading Guide

Each **Stage** is independently deliverable — it compiles, tests pass, and it can be demonstrated in isolation before the next stage begins. Each stage is divided into **Phases** that must be completed in order within that stage. Concurrency requirements and unit test specifications are called out explicitly at every layer.

---

## Stage 0 — Project Scaffold

> **Goal:** A running, empty project with all tooling wired. No logic yet.

### Phase 0.1 — Directory structure

Create the following layout with `uv`:

```
musannif/
├── pyproject.toml
├── uv.lock
├── .python-version           # contains: 3.12
├── README.md
├── src/
│   └── musannif/
│       ├── __init__.py       # exposes version = "0.1.0"
│       ├── cli.py
│       ├── ast_parser.py
│       ├── graph.py
│       ├── context.py
│       ├── validator.py
│       ├── planner.py
│       ├── orchestrator.py
│       ├── assembler.py
│       └── tui/
│           ├── __init__.py
│           ├── app.py
│           ├── screens/
│           │   ├── __init__.py
│           │   ├── decomposition.py
│           │   ├── dashboard.py
│           │   └── summary.py
│           ├── widgets/
│           │   ├── __init__.py
│           │   ├── ast_tree.py
│           │   ├── wave_panel.py
│           │   └── log_panel.py
│           └── theme.py
└── tests/
    ├── conftest.py
    ├── test_ast_parser.py
    ├── test_graph.py
    ├── test_context.py
    ├── test_validator.py
    ├── test_planner.py
    ├── test_orchestrator.py
    └── test_assembler.py
```

**Commands:**
```bash
uv init musannif
cd musannif
uv python pin 3.12
mkdir -p src/musannif/tui/screens src/musannif/tui/widgets tests
```

### Phase 0.2 — pyproject.toml

```toml
[project]
name = "musannif"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "anthropic>=0.52.0",
    "networkx>=3.3.0",
    "typer>=0.12.0",
    "textual>=3.0.0",
]

[project.scripts]
musannif = "musannif.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/musannif"]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-mock>=3.12.0",
    "pytest-cov>=5.0.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Install:**
```bash
uv sync --all-groups
```

### Phase 0.3 — CLI entrypoint skeleton

`src/musannif/cli.py`:
```python
import typer

app = typer.Typer(
    name="musannif",
    help="Musannif — structured long-form document generator.",
    add_completion=False,
)

@app.command()
def run(
    prompt: str = typer.Argument(..., help="The topic or prompt to decompose and generate."),
    output: str = typer.Option("output.md", "--output", "-o", help="Path to write the assembled document."),
    model: str = typer.Option("claude-opus-4-5", "--model", "-m", help="Claude model to use for generation nodes."),
    planner_model: str = typer.Option("claude-haiku-4-5", "--planner-model", help="Claude model to use for planning/structural work."),
):
    """Decompose a prompt into a dependency graph, review it, then generate."""
    typer.echo(f"Prompt received: {prompt}")  # placeholder

if __name__ == "__main__":
    app()
```

### Phase 0.4 — Smoke test

```bash
uv run musannif run "Test prompt"
# Expected: "Prompt received: Test prompt"
uv run pytest tests/ --co -q
# Expected: no errors, 0 tests collected (none written yet)
```

**Stage 0 exit criteria:** `uv run musannif --help` renders cleanly. `uv run pytest` exits 0.

---

## Stage 1 — AST Parser

> **Goal:** A deterministic, pure-function parser that converts a markdown string into a heading tree. Zero model involvement. Zero external dependencies (uses stdlib only).

### Phase 1.1 — Data model

`src/musannif/ast_parser.py` — define the node type first:

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ASTNode:
    """
    One node in the heading tree.

    Attributes:
        path:     Tuple of heading titles from root to this node.
                  e.g. ("The Subcontinent", "Post-1857 Vacuum", "From Swords to Syllabi")
                  The path is the stable address used by depends_on edges.
        depth:    Heading level. H1 = 1, H2 = 2, H3 = 3.
        title:    The raw heading text, stripped of leading '#' and whitespace.
        children: Ordered list of child ASTNodes.
        parent:   Reference to parent ASTNode. None for root.
        content:  The markdown prose content of this section (everything between
                  this heading and the next heading of equal or lesser depth).
                  Populated during generation; empty string at parse time.
        summary:  The ≤100-word summary paragraph extracted from the
                  <!-- summary: ... --> block. Empty string until generated.
        depends_on: List of path tuples this node depends on.
                  Set by the planner; empty list for independent nodes.
        status:   One of: "pending", "generating", "complete", "failed"
    """
    path: tuple[str, ...]
    depth: int
    title: str
    children: list[ASTNode] = field(default_factory=list)
    parent: Optional[ASTNode] = field(default=None, repr=False)
    content: str = ""
    summary: str = ""
    depends_on: list[tuple[str, ...]] = field(default_factory=list)
    status: str = "pending"

    @property
    def address(self) -> str:
        """Human-readable path string: 'Root > Child > Grandchild'."""
        return " > ".join(self.path)

    def is_leaf(self) -> bool:
        return len(self.children) == 0
```

### Phase 1.2 — Parser implementation

```python
import re
from typing import Optional

_HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

def parse_markdown_ast(markdown: str) -> ASTNode:
    """
    Parse a markdown string into a heading AST.

    Rules:
    - The first H1 becomes the root node.
    - If no H1 exists, a virtual root "Document" at depth 0 is created.
    - Headings at depth > current node's depth become children.
    - Headings at depth <= current node's depth walk up the tree until
      a node of lesser depth is found, then attach as a child.
    - Content between headings is assigned to the node whose heading precedes it.

    Args:
        markdown: Raw markdown string.

    Returns:
        Root ASTNode of the tree.

    Raises:
        ValueError: If markdown is empty or contains no headings.
    """
    lines = markdown.split('\n')
    headings: list[tuple[int, int, str]] = []  # (line_index, depth, title)

    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m:
            depth = len(m.group(1))
            title = m.group(2).strip()
            headings.append((i, depth, title))

    if not headings:
        raise ValueError("No headings found in markdown. Cannot build AST.")

    # Build content slices: content[k] = lines between heading k and heading k+1
    content_slices: list[str] = []
    for k, (line_idx, _, _) in enumerate(headings):
        start = line_idx + 1
        end = headings[k + 1][0] if k + 1 < len(headings) else len(lines)
        content_slices.append('\n'.join(lines[start:end]).strip())

    # Build tree
    root_depth = headings[0][1]
    root_title = headings[0][2]
    root = ASTNode(
        path=(root_title,),
        depth=root_depth,
        title=root_title,
        content=content_slices[0],
    )

    # Stack tracks the current ancestry chain
    stack: list[ASTNode] = [root]

    for k in range(1, len(headings)):
        _, depth, title = headings[k]
        content = content_slices[k]

        # Pop stack until we find a node shallower than current
        while len(stack) > 1 and stack[-1].depth >= depth:
            stack.pop()

        parent = stack[-1]
        new_path = parent.path + (title,)
        node = ASTNode(
            path=new_path,
            depth=depth,
            title=title,
            parent=parent,
            content=content,
        )
        parent.children.append(node)
        stack.append(node)

    return root


def flatten_ast(root: ASTNode) -> list[ASTNode]:
    """
    Return all nodes in depth-first pre-order.
    Useful for iteration, display, and address-based lookup.
    """
    result: list[ASTNode] = []
    def _walk(node: ASTNode) -> None:
        result.append(node)
        for child in node.children:
            _walk(child)
    _walk(root)
    return result


def find_node(root: ASTNode, path: tuple[str, ...]) -> Optional[ASTNode]:
    """
    Look up a node by its path tuple. O(n) walk.
    Returns None if path does not exist.
    """
    for node in flatten_ast(root):
        if node.path == path:
            return node
    return None


def ast_to_markdown_outline(root: ASTNode) -> str:
    """
    Serialize the AST back to a markdown heading outline (no content, no summaries).
    Used for the approval gate display and planner output.
    """
    lines: list[str] = []
    for node in flatten_ast(root):
        prefix = '#' * node.depth
        lines.append(f"{prefix} {node.title}")
    return '\n'.join(lines)
```

### Phase 1.3 — Unit tests (`tests/test_ast_parser.py`)

Every test is a pure function call — no mocks, no async:

```python
import pytest
from musannif.ast_parser import parse_markdown_ast, flatten_ast, find_node, ast_to_markdown_outline, ASTNode

# --- Fixtures ---

SIMPLE_MD = """\
# Root
## Child A
### Grandchild A1
### Grandchild A2
## Child B
"""

FLAT_MD = """\
# Root
## Section 1
## Section 2
## Section 3
"""

NO_H1_MD = """\
## Section 1
## Section 2
"""

CONTENT_MD = """\
# Root
Some root content.

## Child
Child content here.
More child content.
"""

# --- Tests: parse_markdown_ast ---

def test_parse_simple_tree_root_title():
    root = parse_markdown_ast(SIMPLE_MD)
    assert root.title == "Root"

def test_parse_simple_tree_root_depth():
    root = parse_markdown_ast(SIMPLE_MD)
    assert root.depth == 1

def test_parse_simple_tree_child_count():
    root = parse_markdown_ast(SIMPLE_MD)
    assert len(root.children) == 2

def test_parse_simple_tree_grandchild_count():
    root = parse_markdown_ast(SIMPLE_MD)
    assert len(root.children[0].children) == 2

def test_parse_simple_tree_second_child_no_children():
    root = parse_markdown_ast(SIMPLE_MD)
    assert len(root.children[1].children) == 0

def test_parse_path_root():
    root = parse_markdown_ast(SIMPLE_MD)
    assert root.path == ("Root",)

def test_parse_path_child():
    root = parse_markdown_ast(SIMPLE_MD)
    assert root.children[0].path == ("Root", "Child A")

def test_parse_path_grandchild():
    root = parse_markdown_ast(SIMPLE_MD)
    grandchild = root.children[0].children[0]
    assert grandchild.path == ("Root", "Child A", "Grandchild A1")

def test_parse_parent_reference():
    root = parse_markdown_ast(SIMPLE_MD)
    child = root.children[0]
    assert child.parent is root

def test_parse_grandchild_parent_reference():
    root = parse_markdown_ast(SIMPLE_MD)
    grandchild = root.children[0].children[0]
    assert grandchild.parent is root.children[0]

def test_parse_flat_structure():
    root = parse_markdown_ast(FLAT_MD)
    assert len(root.children) == 3
    for child in root.children:
        assert len(child.children) == 0

def test_parse_content_assigned_to_root():
    root = parse_markdown_ast(CONTENT_MD)
    assert "Some root content." in root.content

def test_parse_content_assigned_to_child():
    root = parse_markdown_ast(CONTENT_MD)
    child = root.children[0]
    assert "Child content here." in child.content

def test_parse_empty_raises():
    with pytest.raises(ValueError, match="No headings"):
        parse_markdown_ast("")

def test_parse_no_headings_raises():
    with pytest.raises(ValueError, match="No headings"):
        parse_markdown_ast("Just some text without any headings.")

def test_parse_address_property():
    root = parse_markdown_ast(SIMPLE_MD)
    grandchild = root.children[0].children[0]
    assert grandchild.address == "Root > Child A > Grandchild A1"

def test_parse_is_leaf_true():
    root = parse_markdown_ast(SIMPLE_MD)
    grandchild = root.children[0].children[0]
    assert grandchild.is_leaf() is True

def test_parse_is_leaf_false():
    root = parse_markdown_ast(SIMPLE_MD)
    assert root.is_leaf() is False

def test_parse_status_default_pending():
    root = parse_markdown_ast(SIMPLE_MD)
    assert root.status == "pending"

# --- Tests: flatten_ast ---

def test_flatten_count():
    root = parse_markdown_ast(SIMPLE_MD)
    nodes = flatten_ast(root)
    # Root + Child A + Grandchild A1 + Grandchild A2 + Child B = 5
    assert len(nodes) == 5

def test_flatten_order():
    root = parse_markdown_ast(SIMPLE_MD)
    nodes = flatten_ast(root)
    titles = [n.title for n in nodes]
    assert titles == ["Root", "Child A", "Grandchild A1", "Grandchild A2", "Child B"]

# --- Tests: find_node ---

def test_find_node_root():
    root = parse_markdown_ast(SIMPLE_MD)
    found = find_node(root, ("Root",))
    assert found is root

def test_find_node_grandchild():
    root = parse_markdown_ast(SIMPLE_MD)
    found = find_node(root, ("Root", "Child A", "Grandchild A2"))
    assert found is not None
    assert found.title == "Grandchild A2"

def test_find_node_missing_returns_none():
    root = parse_markdown_ast(SIMPLE_MD)
    found = find_node(root, ("Root", "Nonexistent"))
    assert found is None

# --- Tests: ast_to_markdown_outline ---

def test_outline_round_trip():
    root = parse_markdown_ast(FLAT_MD)
    outline = ast_to_markdown_outline(root)
    assert "# Root" in outline
    assert "## Section 1" in outline
    assert "## Section 2" in outline
    assert "## Section 3" in outline

def test_outline_depth_prefix():
    root = parse_markdown_ast(SIMPLE_MD)
    outline = ast_to_markdown_outline(root)
    lines = outline.split('\n')
    # Grandchild lines must start with ###
    grandchild_lines = [l for l in lines if "Grandchild" in l]
    assert all(l.startswith("###") for l in grandchild_lines)
```

**Run:** `uv run pytest tests/test_ast_parser.py -v`
**Expected:** 30 tests, all green.

---

## Stage 2 — Graph Engine

> **Goal:** A deterministic DAG built from ASTNode `depends_on` edges. Validates the graph, computes topological generation waves, detects cycles. Uses `networkx` as the graph backend.

### Phase 2.1 — Graph builder

`src/musannif/graph.py`:

```python
from __future__ import annotations
import networkx as nx
from musannif.ast_parser import ASTNode, flatten_ast

class PipelineGraph:
    """
    A directed acyclic graph of ASTNodes connected by depends_on edges.

    Node identity: the node's path tuple (used as the networkx node key).
    Edge A → B means: "B depends on A" (A must complete before B starts).

    The graph is built once from the approved AST and is immutable after build.
    The only mutable state is node.status, which the orchestrator updates.
    """

    def __init__(self, root: ASTNode) -> None:
        self._root = root
        self._graph: nx.DiGraph = nx.DiGraph()
        self._nodes: dict[tuple[str, ...], ASTNode] = {}
        self._build(root)

    def _build(self, root: ASTNode) -> None:
        """
        Traverse the AST, add all nodes to the graph, then add depends_on edges.

        Raises:
            ValueError: If a depends_on path references a node not in the AST.
            ValueError: If the resulting graph contains a cycle.
        """
        # Register all nodes
        for node in flatten_ast(root):
            self._graph.add_node(node.path)
            self._nodes[node.path] = node

        # Add edges from depends_on declarations
        for node in flatten_ast(root):
            for dep_path in node.depends_on:
                if dep_path not in self._nodes:
                    raise ValueError(
                        f"Node '{node.address}' declares depends_on "
                        f"'{' > '.join(dep_path)}' which does not exist in the AST."
                    )
                # Edge: dep_path → node.path (dep must finish before node starts)
                self._graph.add_edge(dep_path, node.path)

        if not nx.is_directed_acyclic_graph(self._graph):
            cycle = nx.find_cycle(self._graph)
            raise ValueError(
                f"Dependency cycle detected: {cycle}. The graph must be a DAG."
            )

    def compute_waves(self) -> list[list[ASTNode]]:
        """
        Compute ordered generation waves via topological sort.

        A wave is a maximal set of nodes whose all dependencies are satisfied
        by earlier waves. Nodes within a wave can be generated in parallel.

        Returns:
            List of waves. Each wave is a list of ASTNodes.
            Wave 0 contains all nodes with no dependencies.
            Wave k contains all nodes whose dependencies are all in waves 0..k-1.

        Algorithm: Kahn's algorithm (BFS-based topological sort),
        grouped into depth levels for wave assignment.
        """
        # in_degree counts how many unsatisfied dependencies each node has
        in_degree: dict[tuple[str, ...], int] = {
            path: self._graph.in_degree(path)
            for path in self._graph.nodes
        }

        waves: list[list[ASTNode]] = []
        ready: list[tuple[str, ...]] = [
            path for path, deg in in_degree.items() if deg == 0
        ]

        while ready:
            wave_nodes = [self._nodes[path] for path in ready]
            waves.append(wave_nodes)
            next_ready: list[tuple[str, ...]] = []
            for path in ready:
                for successor in self._graph.successors(path):
                    in_degree[successor] -= 1
                    if in_degree[successor] == 0:
                        next_ready.append(successor)
            ready = next_ready

        return waves

    def get_node(self, path: tuple[str, ...]) -> ASTNode:
        """Retrieve an ASTNode by path. Raises KeyError if not found."""
        return self._nodes[path]

    def direct_dependencies(self, node: ASTNode) -> list[ASTNode]:
        """
        Return all nodes that `node` directly depends on.
        These are the nodes whose summaries will be injected as Tier 1+2 context.
        """
        return [
            self._nodes[dep_path]
            for dep_path in self._graph.predecessors(node.path)
        ]

    def all_nodes(self) -> list[ASTNode]:
        """All nodes in the graph, in topological order."""
        return [self._nodes[p] for p in nx.topological_sort(self._graph)]

    def validate_no_orphans(self) -> list[ASTNode]:
        """
        Return any leaf nodes that have no outgoing edges and no content.
        Used after generation to detect nodes that were never written.
        """
        return [
            node for node in self._nodes.values()
            if node.is_leaf() and node.content == "" and node.status != "complete"
        ]
```

### Phase 2.2 — Unit tests (`tests/test_graph.py`)

```python
import pytest
from musannif.ast_parser import parse_markdown_ast, ASTNode
from musannif.graph import PipelineGraph

SIMPLE_MD = """\
# Root
## Section A
## Section B
## Section C
"""

def make_ast_with_deps() -> ASTNode:
    """Build an AST where B depends on A, and C depends on B."""
    root = parse_markdown_ast(SIMPLE_MD)
    nodes = {n.title: n for n in [root] + root.children}
    nodes["Section B"].depends_on = [nodes["Section A"].path]
    nodes["Section C"].depends_on = [nodes["Section B"].path]
    return root

def make_ast_with_cycle() -> ASTNode:
    """Build an AST with a cycle: A depends on B, B depends on A."""
    root = parse_markdown_ast(SIMPLE_MD)
    nodes = {n.title: n for n in [root] + root.children}
    nodes["Section A"].depends_on = [nodes["Section B"].path]
    nodes["Section B"].depends_on = [nodes["Section A"].path]
    return root

def make_ast_with_bad_dep() -> ASTNode:
    """Node references a path that doesn't exist."""
    root = parse_markdown_ast(SIMPLE_MD)
    root.children[0].depends_on = [("Root", "Nonexistent Section")]
    return root

# --- Build tests ---

def test_graph_builds_without_deps():
    root = parse_markdown_ast(SIMPLE_MD)
    g = PipelineGraph(root)
    assert len(g.all_nodes()) == 4  # Root + A + B + C

def test_graph_builds_with_valid_deps():
    root = make_ast_with_deps()
    g = PipelineGraph(root)  # Should not raise
    assert g is not None

def test_graph_raises_on_cycle():
    root = make_ast_with_cycle()
    with pytest.raises(ValueError, match="cycle"):
        PipelineGraph(root)

def test_graph_raises_on_bad_dep_path():
    root = make_ast_with_bad_dep()
    with pytest.raises(ValueError, match="does not exist"):
        PipelineGraph(root)

# --- Wave computation tests ---

def test_wave_no_deps_single_wave():
    root = parse_markdown_ast(SIMPLE_MD)
    g = PipelineGraph(root)
    waves = g.compute_waves()
    # All nodes in one wave since no deps
    assert len(waves) == 1
    assert len(waves[0]) == 4

def test_wave_linear_chain_three_waves():
    root = make_ast_with_deps()
    g = PipelineGraph(root)
    waves = g.compute_waves()
    # Wave 0: Root + A (no deps)
    # Wave 1: B (depends on A)
    # Wave 2: C (depends on B)
    assert len(waves) == 3

def test_wave_all_nodes_covered():
    root = make_ast_with_deps()
    g = PipelineGraph(root)
    waves = g.compute_waves()
    all_in_waves = [n for wave in waves for n in wave]
    assert len(all_in_waves) == 4

def test_wave_order_respected():
    root = make_ast_with_deps()
    g = PipelineGraph(root)
    waves = g.compute_waves()
    # Section A must appear before Section B
    flat = [n.title for wave in waves for n in wave]
    assert flat.index("Section A") < flat.index("Section B")
    assert flat.index("Section B") < flat.index("Section C")

# --- Direct dependencies tests ---

def test_direct_dependencies_empty_for_root():
    root = parse_markdown_ast(SIMPLE_MD)
    g = PipelineGraph(root)
    assert g.direct_dependencies(root) == []

def test_direct_dependencies_returns_correct_node():
    root = make_ast_with_deps()
    g = PipelineGraph(root)
    section_b = g.get_node(("Root", "Section B"))
    deps = g.direct_dependencies(section_b)
    assert len(deps) == 1
    assert deps[0].title == "Section A"

# --- Validate no orphans ---

def test_no_orphans_when_all_complete():
    root = parse_markdown_ast(SIMPLE_MD)
    for node in [root] + root.children:
        node.status = "complete"
        node.content = "some content"
    g = PipelineGraph(root)
    assert g.validate_no_orphans() == []
```

**Run:** `uv run pytest tests/test_graph.py -v`
**Expected:** 16 tests, all green.

---

## Stage 3 — Validator + Context Assembler

> **Goal:** Two pure modules. The validator extracts and checks `<!-- summary: ... -->` blocks. The context assembler constructs the three-tier context payload injected into each agent before generation.

### Phase 3.1 — Validator (`src/musannif/validator.py`)

```python
from __future__ import annotations
import re
from dataclasses import dataclass

_SUMMARY_RE = re.compile(
    r'<!--\s*summary:\s*(.*?)\s*-->',
    re.DOTALL | re.IGNORECASE
)
_MAX_WORDS = 100

@dataclass
class ValidationResult:
    valid: bool
    summary: str        # Extracted text if valid, empty string if not
    word_count: int
    error: str          # Human-readable error message if not valid

def extract_and_validate_summary(content: str) -> ValidationResult:
    """
    Extract the <!-- summary: ... --> block from generated content and validate it.

    Rules:
        1. Exactly one <!-- summary: ... --> block must be present.
        2. The extracted text must be non-empty (not just whitespace).
        3. The word count of the extracted text must be ≤ 100.

    Args:
        content: The full markdown content generated by an agent for one node.

    Returns:
        ValidationResult with valid=True and the summary text if all rules pass.
        ValidationResult with valid=False and an error message otherwise.
    """
    matches = _SUMMARY_RE.findall(content)

    if len(matches) == 0:
        return ValidationResult(
            valid=False,
            summary="",
            word_count=0,
            error="No <!-- summary: ... --> block found. Agent must end its section with one.",
        )

    if len(matches) > 1:
        return ValidationResult(
            valid=False,
            summary="",
            word_count=0,
            error=f"Multiple summary blocks found ({len(matches)}). Exactly one is required.",
        )

    raw = matches[0].strip()

    if not raw:
        return ValidationResult(
            valid=False,
            summary="",
            word_count=0,
            error="Summary block is empty. A ≤100-word prose paragraph is required.",
        )

    words = raw.split()
    word_count = len(words)

    if word_count > _MAX_WORDS:
        return ValidationResult(
            valid=False,
            summary=raw,
            word_count=word_count,
            error=f"Summary is {word_count} words. Maximum allowed is {_MAX_WORDS}.",
        )

    return ValidationResult(valid=True, summary=raw, word_count=word_count, error="")


def strip_summary_block(content: str) -> str:
    """
    Remove the <!-- summary: ... --> block from content.
    Used when assembling the final document (summaries are internal scaffolding,
    not part of the reader-facing output).
    """
    return _SUMMARY_RE.sub('', content).strip()
```

### Phase 3.2 — Context assembler (`src/musannif/context.py`)

```python
from __future__ import annotations
from musannif.ast_parser import ASTNode, ast_to_markdown_outline

class ContextTier:
    """Namespace for tier constants."""
    AST_AND_SUMMARY = "tier_1_2"
    FULL_TEXT = "tier_3"

def assemble_context(
    node: ASTNode,
    dependencies: list[ASTNode],
) -> str:
    """
    Assemble the Tier 1+2 context string injected into an agent before generation.

    For each dependency node, injects:
    - Tier 1: The heading outline of that node's subtree (deterministic, free).
    - Tier 2: The ≤100-word summary paragraph.

    Args:
        node:         The node about to be generated.
        dependencies: The direct dependency nodes (from PipelineGraph.direct_dependencies).
                      Each must have status="complete" and a non-empty summary.

    Returns:
        A formatted string ready to prepend to the agent's generation prompt.
        Empty string if dependencies list is empty.
    """
    if not dependencies:
        return ""

    sections: list[str] = []

    for dep in dependencies:
        outline = ast_to_markdown_outline(dep)
        summary = dep.summary if dep.summary else "[Summary not yet available]"

        section = (
            f'### Upstream node: "{dep.address}"\n'
            f"**Sections written:**\n```\n{outline}\n```\n\n"
            f"**Summary:** {summary}"
        )
        sections.append(section)

    header = (
        "## Prerequisites covered by upstream nodes\n"
        "(Review these. If Tier 1+2 is insufficient to understand what was covered, "
        "you may request the full text of a specific node using the `read_node_content` tool "
        "before writing your section.)\n\n"
    )

    return header + "\n\n---\n\n".join(sections) + "\n\n---\n"


def build_generation_prompt(
    node: ASTNode,
    dependencies: list[ASTNode],
    principle_card: str = "",
) -> str:
    """
    Build the complete prompt sent to a generation agent for one node.

    Structure:
    1. Principle card (voice/style instructions) — if provided.
    2. Tier 1+2 context from dependencies.
    3. The generation instruction for this specific node.

    Args:
        node:           The node to generate.
        dependencies:   Direct dependency nodes.
        principle_card: Optional style/voice card text.

    Returns:
        Complete prompt string.
    """
    parts: list[str] = []

    if principle_card:
        parts.append(f"## Voice and Style\n{principle_card}\n")

    context = assemble_context(node, dependencies)
    if context:
        parts.append(context)

    instruction = (
        f"## Your task\n"
        f"Write the section: **{node.address}**\n\n"
        f"Do not retell narratives already covered by upstream nodes. "
        f"Reference them briefly if needed, then advance the argument.\n\n"
        f"End your section with exactly one summary block in this format:\n"
        f"```\n"
        f"<!-- summary: [your ≤100-word prose summary of what this section covered] -->\n"
        f"```\n"
        f"The summary must be plain prose, not bullet points or lists.\n"
        f"The summary must be ≤100 words. It will be validated automatically.\n"
    )
    parts.append(instruction)

    return "\n".join(parts)
```

### Phase 3.3 — Unit tests (`tests/test_validator.py` and `tests/test_context.py`)

**test_validator.py:**
```python
import pytest
from musannif.validator import extract_and_validate_summary, strip_summary_block

VALID_CONTENT = """\
Some generated prose content.

More content here.

<!-- summary: The 1857 Rebellion destroyed the Mughal patronage system. Without royal land grants, scholars pivoted to institutional self-preservation. Deoband pioneered the public-funded madrasa model. -->
"""

OVER_LIMIT_CONTENT = (
    "<!-- summary: " + " ".join(["word"] * 101) + " -->"
)

def test_valid_summary_extracted():
    result = extract_and_validate_summary(VALID_CONTENT)
    assert result.valid is True
    assert "1857 Rebellion" in result.summary

def test_valid_summary_word_count_under_limit():
    result = extract_and_validate_summary(VALID_CONTENT)
    assert result.word_count <= 100

def test_missing_summary_block():
    result = extract_and_validate_summary("Content without any summary block.")
    assert result.valid is False
    assert "No <!-- summary" in result.error

def test_empty_summary_block():
    result = extract_and_validate_summary("<!-- summary:   -->")
    assert result.valid is False
    assert "empty" in result.error.lower()

def test_multiple_summary_blocks():
    content = "<!-- summary: First. --> some text <!-- summary: Second. -->"
    result = extract_and_validate_summary(content)
    assert result.valid is False
    assert "Multiple" in result.error

def test_over_word_limit():
    result = extract_and_validate_summary(OVER_LIMIT_CONTENT)
    assert result.valid is False
    assert "101" in result.error

def test_exactly_100_words_valid():
    summary = " ".join(["word"] * 100)
    content = f"<!-- summary: {summary} -->"
    result = extract_and_validate_summary(content)
    assert result.valid is True
    assert result.word_count == 100

def test_strip_removes_summary_block():
    stripped = strip_summary_block(VALID_CONTENT)
    assert "<!-- summary:" not in stripped

def test_strip_preserves_content():
    stripped = strip_summary_block(VALID_CONTENT)
    assert "Some generated prose content." in stripped

def test_strip_no_block_unchanged():
    content = "No summary here."
    assert strip_summary_block(content) == content
```

**test_context.py:**
```python
import pytest
from musannif.ast_parser import parse_markdown_ast
from musannif.context import assemble_context, build_generation_prompt

MD = """\
# Root
## Section A
## Section B
"""

def make_complete_node(title: str, summary: str) -> object:
    root = parse_markdown_ast(f"# Root\n## {title}\n")
    child = root.children[0]
    child.status = "complete"
    child.summary = summary
    return child

def test_assemble_empty_deps_returns_empty():
    root = parse_markdown_ast(MD)
    node = root.children[1]
    result = assemble_context(node, [])
    assert result == ""

def test_assemble_includes_dep_address():
    root = parse_markdown_ast(MD)
    dep = root.children[0]
    dep.summary = "A short summary."
    dep.status = "complete"
    node = root.children[1]
    result = assemble_context(node, [dep])
    assert "Section A" in result

def test_assemble_includes_dep_summary():
    root = parse_markdown_ast(MD)
    dep = root.children[0]
    dep.summary = "A short summary."
    dep.status = "complete"
    node = root.children[1]
    result = assemble_context(node, [dep])
    assert "A short summary." in result

def test_assemble_includes_outline():
    root = parse_markdown_ast(MD)
    dep = root.children[0]
    dep.summary = "Some summary."
    node = root.children[1]
    result = assemble_context(node, [dep])
    assert "## Section A" in result

def test_build_prompt_contains_task():
    root = parse_markdown_ast(MD)
    node = root.children[1]
    prompt = build_generation_prompt(node, [])
    assert "Section B" in prompt

def test_build_prompt_contains_summary_instruction():
    root = parse_markdown_ast(MD)
    node = root.children[0]
    prompt = build_generation_prompt(node, [])
    assert "<!-- summary:" in prompt

def test_build_prompt_includes_principle_card():
    root = parse_markdown_ast(MD)
    node = root.children[0]
    prompt = build_generation_prompt(node, [], principle_card="Be precise.")
    assert "Be precise." in prompt

def test_build_prompt_no_context_when_no_deps():
    root = parse_markdown_ast(MD)
    node = root.children[0]
    prompt = build_generation_prompt(node, [])
    assert "Prerequisites" not in prompt
```

**Run:** `uv run pytest tests/test_validator.py tests/test_context.py -v`
**Expected:** 20 tests, all green.

---

## Stage 4 — Planner + Orchestrator

> **Goal:** The planner calls Claude to decompose a prompt into an approved AST. The orchestrator runs the generation waves, calling Claude agents per node, validating summaries, and updating the AST. This stage introduces real Claude API calls, mocked in tests.

### Phase 4.1 — Planner (`src/musannif/planner.py`)

The planner's job: take a raw prompt, produce a markdown outline + YAML depends_on block that parses into an AST.

```python
from __future__ import annotations
import re
import yaml
import anthropic
from musannif.ast_parser import parse_markdown_ast, ASTNode, find_node

_PLANNER_SYSTEM_PROMPT = """\
You are a structural planner for a long-form document generation pipeline.

Your job: given a topic prompt, decompose it into a hierarchical markdown outline.

Output format — you must output EXACTLY two blocks and nothing else:

BLOCK 1: A markdown heading outline. Use # for the document root, ## for major sections, ### for subsections. Use as many levels as the topic genuinely needs.

BLOCK 2: A YAML block (fenced with ```yaml and ```) specifying the depends_on edges between sections. Each entry maps a section path (list of titles from root to section) to a list of paths it depends on.

Rules for depends_on:
- A section should depend on another if it assumes the reader has already read that section.
- Narrative prerequisites are the most common dependency: if section B retells the same backstory that section A covers, B should depend on A.
- Do not add unnecessary dependencies. A section with no prerequisites should not appear in the YAML at all.
- Paths are lists of strings matching the heading titles exactly as written in the outline.

Example output:

# The Subcontinent
## Post-1857 Vacuum
## Birth of Deoband
## Barelvi Reaction
## Prophetology

```yaml
depends_on:
  - path: ["The Subcontinent", "Birth of Deoband"]
    depends_on: [["The Subcontinent", "Post-1857 Vacuum"]]
  - path: ["The Subcontinent", "Barelvi Reaction"]
    depends_on: [["The Subcontinent", "Post-1857 Vacuum"], ["The Subcontinent", "Birth of Deoband"]]
  - path: ["The Subcontinent", "Prophetology"]
    depends_on: [["The Subcontinent", "Barelvi Reaction"]]
```
"""

_YAML_BLOCK_RE = re.compile(r'```yaml\s*(.*?)\s*```', re.DOTALL)

def _extract_outline_and_deps(raw: str) -> tuple[str, str]:
    """
    Split the planner's raw output into the markdown outline and the YAML block.

    Returns:
        (outline_markdown, yaml_string)

    Raises:
        ValueError: If the YAML block is missing or the outline is empty.
    """
    yaml_match = _YAML_BLOCK_RE.search(raw)
    yaml_str = yaml_match.group(1) if yaml_match else ""

    # The outline is everything before the YAML block
    if yaml_match:
        outline = raw[:yaml_match.start()].strip()
    else:
        outline = raw.strip()

    if not outline:
        raise ValueError("Planner output contained no markdown outline.")

    return outline, yaml_str


def _apply_deps_to_ast(root: ASTNode, yaml_str: str) -> None:
    """
    Parse the YAML depends_on block and write the edge declarations onto AST nodes.

    Modifies ASTNode.depends_on in-place.

    Raises:
        ValueError: If a path in the YAML does not match any node in the AST.
        ValueError: If a dependency path in the YAML does not match any node.
        yaml.YAMLError: If the YAML is malformed.
    """
    if not yaml_str.strip():
        return  # No dependencies declared

    data = yaml.safe_load(yaml_str)
    if not data or "depends_on" not in data:
        return

    for entry in data["depends_on"]:
        path = tuple(entry["path"])
        node = find_node(root, path)
        if node is None:
            raise ValueError(
                f"YAML depends_on references path {list(path)} which does not exist in the outline."
            )
        dep_paths: list[tuple[str, ...]] = []
        for dep in entry.get("depends_on", []):
            dep_path = tuple(dep)
            dep_node = find_node(root, dep_path)
            if dep_node is None:
                raise ValueError(
                    f"YAML depends_on: node {list(path)} references dependency "
                    f"{list(dep_path)} which does not exist in the outline."
                )
            dep_paths.append(dep_path)
        node.depends_on = dep_paths


async def run_planner(
    prompt: str,
    model: str = "claude-haiku-4-5",
    client: anthropic.AsyncAnthropic | None = None,
) -> ASTNode:
    """
    Call the planner model and return a fully constructed ASTNode tree.

    Args:
        prompt:  The raw user prompt.
        model:   The Claude model to use for planning (cheap/fast tier).
        client:  An existing AsyncAnthropic client. If None, a new one is created
                 using the ANTHROPIC_API_KEY environment variable.

    Returns:
        Root ASTNode with depends_on edges populated.

    Raises:
        ValueError: If the planner output cannot be parsed.
        anthropic.APIError: On API failure.
    """
    if client is None:
        client = anthropic.AsyncAnthropic()

    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        system=_PLANNER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    outline, yaml_str = _extract_outline_and_deps(raw)
    root = parse_markdown_ast(outline)
    _apply_deps_to_ast(root, yaml_str)
    return root
```

### Phase 4.2 — Orchestrator (`src/musannif/orchestrator.py`)

```python
from __future__ import annotations
import asyncio
import anthropic
from musannif.ast_parser import ASTNode
from musannif.graph import PipelineGraph
from musannif.context import build_generation_prompt
from musannif.validator import extract_and_validate_summary, strip_summary_block

_GENERATION_SYSTEM_PROMPT = """\
You are a domain expert generating one section of a long-form document.
You write with depth, precision, and narrative coherence.
Follow all instructions in the user message exactly.
Never repeat narratives that upstream nodes have already covered.
End your response with the <!-- summary: ... --> block as instructed.
"""

_MAX_RETRIES = 3

class GenerationError(Exception):
    """Raised when a node fails to generate a valid summary after max retries."""

async def _generate_node(
    node: ASTNode,
    dependencies: list[ASTNode],
    model: str,
    client: anthropic.AsyncAnthropic,
    principle_card: str = "",
    on_status_change: callable | None = None,
) -> None:
    """
    Generate content for a single ASTNode. Updates node.content, node.summary,
    and node.status in-place. Retries up to _MAX_RETRIES times on validation failure.

    Args:
        node:             The node to generate.
        dependencies:     Direct dependency nodes (already complete).
        model:            Claude model to use.
        client:           AsyncAnthropic client (shared across the orchestrator).
        principle_card:   Optional voice/style instructions.
        on_status_change: Optional callback(node) called whenever node.status changes.
                          Used by the TUI to update the live display.

    Raises:
        GenerationError: If the node fails validation after _MAX_RETRIES attempts.
    """
    def _set_status(status: str) -> None:
        node.status = status
        if on_status_change:
            on_status_change(node)

    _set_status("generating")
    prompt = build_generation_prompt(node, dependencies, principle_card)

    for attempt in range(1, _MAX_RETRIES + 1):
        response = await client.messages.create(
            model=model,
            max_tokens=8192,
            system=_GENERATION_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_content = response.content[0].text
        result = extract_and_validate_summary(raw_content)

        if result.valid:
            node.content = strip_summary_block(raw_content)
            node.summary = result.summary
            _set_status("complete")
            return
        else:
            # Feed the validation error back as a correction prompt
            correction = (
                f"Your previous response failed validation: {result.error}\n"
                f"Rewrite the section and ensure it ends with a valid "
                f"<!-- summary: ... --> block of ≤100 words."
            )
            prompt = prompt + f"\n\n[VALIDATION FAILED — Attempt {attempt}/{_MAX_RETRIES}]\n{correction}"

    _set_status("failed")
    raise GenerationError(
        f"Node '{node.address}' failed validation after {_MAX_RETRIES} attempts."
    )


async def run_orchestrator(
    graph: PipelineGraph,
    model: str = "claude-opus-4-5",
    client: anthropic.AsyncAnthropic | None = None,
    on_status_change: callable | None = None,
    on_wave_start: callable | None = None,
) -> None:
    """
    Execute the full generation pipeline in topological wave order.

    Within each wave, all nodes are dispatched concurrently using asyncio.gather.
    Across waves, execution is strictly sequential (wave k+1 starts only after
    all nodes in wave k are complete).

    Args:
        graph:            The approved PipelineGraph.
        model:            Claude model for generation nodes.
        client:           Shared AsyncAnthropic client. Created if None.
        on_status_change: Callback(node) fired on every node status transition.
                          Called from the asyncio event loop — must not block.
        on_wave_start:    Callback(wave_index, wave_nodes) fired before each wave.
                          Used by the TUI to update wave progress display.

    Raises:
        GenerationError:  If any node in any wave fails after max retries.
                          Propagated immediately — no other waves start after failure.
    """
    if client is None:
        client = anthropic.AsyncAnthropic()

    waves = graph.compute_waves()

    for wave_index, wave_nodes in enumerate(waves):
        if on_wave_start:
            on_wave_start(wave_index, wave_nodes)

        tasks = [
            _generate_node(
                node=node,
                dependencies=graph.direct_dependencies(node),
                model=model,
                client=client,
                on_status_change=on_status_change,
            )
            for node in wave_nodes
        ]

        # All nodes in this wave run concurrently.
        # asyncio.gather propagates the first exception immediately.
        await asyncio.gather(*tasks)
```

### Phase 4.3 — Unit tests (`tests/test_planner.py`, `tests/test_orchestrator.py`)

**Note on mocking:** All Claude API calls are mocked. Tests verify the orchestration logic, not the model output.

**test_planner.py:**
```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from musannif.planner import _extract_outline_and_deps, _apply_deps_to_ast, run_planner
from musannif.ast_parser import parse_markdown_ast

VALID_PLANNER_OUTPUT = """\
# The Topic
## Section A
## Section B
## Section C

```yaml
depends_on:
  - path: ["The Topic", "Section B"]
    depends_on: [["The Topic", "Section A"]]
  - path: ["The Topic", "Section C"]
    depends_on: [["The Topic", "Section B"]]
```
"""

def test_extract_outline_returns_markdown():
    outline, _ = _extract_outline_and_deps(VALID_PLANNER_OUTPUT)
    assert "# The Topic" in outline

def test_extract_yaml_returns_yaml():
    _, yaml_str = _extract_outline_and_deps(VALID_PLANNER_OUTPUT)
    assert "depends_on" in yaml_str

def test_extract_no_yaml_block_returns_empty():
    outline, yaml_str = _extract_outline_and_deps("# Root\n## Section")
    assert "# Root" in outline
    assert yaml_str == ""

def test_extract_empty_outline_raises():
    from musannif.planner import _extract_outline_and_deps
    import pytest
    with pytest.raises(ValueError, match="no markdown outline"):
        _extract_outline_and_deps("```yaml\ndepends_on: []\n```")

def test_apply_deps_sets_depends_on():
    root = parse_markdown_ast("# The Topic\n## Section A\n## Section B\n")
    yaml_str = """
depends_on:
  - path: ["The Topic", "Section B"]
    depends_on: [["The Topic", "Section A"]]
"""
    _apply_deps_to_ast(root, yaml_str)
    section_b = root.children[1]
    assert section_b.depends_on == [("The Topic", "Section A")]

def test_apply_deps_bad_path_raises():
    root = parse_markdown_ast("# Root\n## A\n")
    yaml_str = """
depends_on:
  - path: ["Root", "Nonexistent"]
    depends_on: []
"""
    with pytest.raises(ValueError, match="does not exist"):
        _apply_deps_to_ast(root, yaml_str)

def test_apply_deps_empty_yaml_is_noop():
    root = parse_markdown_ast("# Root\n## A\n")
    _apply_deps_to_ast(root, "")
    assert root.children[0].depends_on == []

@pytest.mark.asyncio
async def test_run_planner_calls_api(mocker):
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=VALID_PLANNER_OUTPUT)]
    mock_client.messages.create = AsyncMock(return_value=mock_response)

    root = await run_planner("Test prompt", client=mock_client)
    assert root.title == "The Topic"
    assert len(root.children) == 3

@pytest.mark.asyncio
async def test_run_planner_applies_deps(mocker):
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=VALID_PLANNER_OUTPUT)]
    mock_client.messages.create = AsyncMock(return_value=mock_response)

    root = await run_planner("Test prompt", client=mock_client)
    section_b = root.children[1]
    assert len(section_b.depends_on) == 1
```

**test_orchestrator.py:**
```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from musannif.ast_parser import parse_markdown_ast
from musannif.graph import PipelineGraph
from musannif.orchestrator import run_orchestrator, GenerationError

VALID_GENERATION = """\
Some generated prose.

<!-- summary: This section covered the key arguments about the topic using clear narrative prose that does not retell upstream content. -->
"""

INVALID_GENERATION = "Generated prose with no summary block at all."

def make_mock_client(text: str) -> AsyncMock:
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=text)]
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    return mock_client

@pytest.mark.asyncio
async def test_orchestrator_marks_nodes_complete():
    root = parse_markdown_ast("# Root\n## A\n## B\n")
    graph = PipelineGraph(root)
    client = make_mock_client(VALID_GENERATION)

    await run_orchestrator(graph, client=client)

    for node in graph.all_nodes():
        assert node.status == "complete"

@pytest.mark.asyncio
async def test_orchestrator_sets_content():
    root = parse_markdown_ast("# Root\n## A\n")
    graph = PipelineGraph(root)
    client = make_mock_client(VALID_GENERATION)

    await run_orchestrator(graph, client=client)

    section_a = root.children[0]
    assert "Some generated prose." in section_a.content

@pytest.mark.asyncio
async def test_orchestrator_sets_summary():
    root = parse_markdown_ast("# Root\n## A\n")
    graph = PipelineGraph(root)
    client = make_mock_client(VALID_GENERATION)

    await run_orchestrator(graph, client=client)

    section_a = root.children[0]
    assert section_a.summary != ""

@pytest.mark.asyncio
async def test_orchestrator_calls_status_callback():
    root = parse_markdown_ast("# Root\n## A\n")
    graph = PipelineGraph(root)
    client = make_mock_client(VALID_GENERATION)
    statuses = []

    await run_orchestrator(graph, client=client, on_status_change=lambda n: statuses.append(n.status))

    assert "generating" in statuses
    assert "complete" in statuses

@pytest.mark.asyncio
async def test_orchestrator_raises_after_max_retries():
    root = parse_markdown_ast("# Root\n## A\n")
    graph = PipelineGraph(root)
    client = make_mock_client(INVALID_GENERATION)

    with pytest.raises(GenerationError):
        await run_orchestrator(graph, client=client)

@pytest.mark.asyncio
async def test_orchestrator_marks_failed_on_error():
    root = parse_markdown_ast("# Root\n## A\n")
    graph = PipelineGraph(root)
    client = make_mock_client(INVALID_GENERATION)

    try:
        await run_orchestrator(graph, client=client)
    except GenerationError:
        pass

    section_a = root.children[0]
    assert section_a.status == "failed"

@pytest.mark.asyncio
async def test_orchestrator_respects_wave_order():
    """
    Section B depends on Section A.
    Verify A is complete before B starts generating.
    """
    root = parse_markdown_ast("# Root\n## A\n## B\n")
    root.children[1].depends_on = [root.children[0].path]
    graph = PipelineGraph(root)
    completion_order = []

    original_create = make_mock_client(VALID_GENERATION).messages.create

    import asyncio
    call_count = 0

    async def ordered_create(**kwargs):
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0)  # yield to event loop
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=VALID_GENERATION)]
        return mock_response

    client = AsyncMock()
    client.messages.create = ordered_create

    await run_orchestrator(
        graph,
        client=client,
        on_status_change=lambda n: completion_order.append((n.title, n.status))
    )

    # A must reach "complete" before B starts "generating"
    a_complete_idx = next(i for i, (t, s) in enumerate(completion_order) if t == "A" and s == "complete")
    b_generating_idx = next(i for i, (t, s) in enumerate(completion_order) if t == "B" and s == "generating")
    assert a_complete_idx < b_generating_idx
```

**Run:** `uv run pytest tests/test_planner.py tests/test_orchestrator.py -v`
**Expected:** 18 tests, all green.

---

## Stage 5 — Assembler

> **Goal:** Stitch all completed nodes into a final markdown document in AST order. Strip summary blocks. Produce clean reader-facing output.

### Phase 5.1 — Assembler (`src/musannif/assembler.py`)

```python
from __future__ import annotations
from musannif.ast_parser import ASTNode, flatten_ast
from musannif.validator import strip_summary_block

class AssemblyError(Exception):
    """Raised when one or more nodes are not complete and cannot be assembled."""

def assemble_document(root: ASTNode, strict: bool = True) -> str:
    """
    Stitch all ASTNodes into a final markdown document.

    Traversal order: depth-first pre-order (same as flatten_ast), which matches
    the logical reading order of a hierarchical document.

    For each node:
    - Write the heading (# * depth + title).
    - Write the content (with summary block stripped).

    Args:
        root:   The root ASTNode of the completed AST.
        strict: If True, raise AssemblyError if any node has status != "complete".
                If False, insert a [GENERATION FAILED] placeholder for incomplete nodes.

    Returns:
        Assembled markdown string.

    Raises:
        AssemblyError: If strict=True and any node is not complete.
    """
    nodes = flatten_ast(root)
    incomplete = [n for n in nodes if n.status != "complete"]

    if strict and incomplete:
        titles = [n.address for n in incomplete]
        raise AssemblyError(
            f"Cannot assemble document: {len(incomplete)} node(s) not complete:\n"
            + "\n".join(f"  - {t}" for t in titles)
        )

    sections: list[str] = []

    for node in nodes:
        heading = '#' * node.depth + ' ' + node.title

        if node.status == "complete":
            content = strip_summary_block(node.content)
            section = f"{heading}\n\n{content}" if content else heading
        else:
            section = f"{heading}\n\n[GENERATION FAILED — content not available]"

        sections.append(section)

    return '\n\n'.join(sections)


def write_document(root: ASTNode, output_path: str, strict: bool = True) -> None:
    """
    Assemble and write the document to a file.

    Args:
        root:        The root ASTNode.
        output_path: File path to write to. Will overwrite if exists.
        strict:      Passed through to assemble_document.
    """
    content = assemble_document(root, strict=strict)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

### Phase 5.2 — Unit tests (`tests/test_assembler.py`)

```python
import pytest
import os
import tempfile
from musannif.ast_parser import parse_markdown_ast
from musannif.assembler import assemble_document, write_document, AssemblyError

MD = "# Root\n## A\n## B\n"

def make_complete_ast(md: str = MD) -> object:
    root = parse_markdown_ast(md)
    for node in [root] + list(root.children):
        node.status = "complete"
        node.content = f"Content for {node.title}. <!-- summary: Summary of {node.title}. -->"
    return root

def test_assemble_contains_all_headings():
    root = make_complete_ast()
    doc = assemble_document(root)
    assert "# Root" in doc
    assert "## A" in doc
    assert "## B" in doc

def test_assemble_strips_summary_blocks():
    root = make_complete_ast()
    doc = assemble_document(root)
    assert "<!-- summary:" not in doc

def test_assemble_contains_content():
    root = make_complete_ast()
    doc = assemble_document(root)
    assert "Content for A." in doc

def test_assemble_strict_raises_on_incomplete():
    root = parse_markdown_ast(MD)
    root.children[0].status = "complete"
    root.children[0].content = "content"
    # root and B are not complete
    with pytest.raises(AssemblyError):
        assemble_document(root, strict=True)

def test_assemble_non_strict_includes_placeholder():
    root = parse_markdown_ast(MD)
    root.status = "complete"
    root.content = "root content"
    root.children[0].status = "failed"
    root.children[0].content = ""
    root.children[1].status = "complete"
    root.children[1].content = "B content"

    doc = assemble_document(root, strict=False)
    assert "GENERATION FAILED" in doc

def test_assemble_order_matches_ast():
    root = make_complete_ast()
    doc = assemble_document(root)
    a_pos = doc.index("## A")
    b_pos = doc.index("## B")
    assert a_pos < b_pos

def test_write_document_creates_file():
    root = make_complete_ast()
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        path = f.name
    try:
        write_document(root, path)
        assert os.path.exists(path)
        with open(path) as f:
            content = f.read()
        assert "# Root" in content
    finally:
        os.unlink(path)
```

**Run:** `uv run pytest tests/test_assembler.py -v`
**Expected:** 8 tests, all green.

---

## Stage 6 — Textual TUI

> **Goal:** A three-screen Textual application wired to the orchestrator. Screen 1 is the interactive approval gate. Screen 2 is the live generation dashboard. Screen 3 is the completion summary.

### Phase 6.1 — Theme (`src/musannif/tui/theme.py`)

```python
# Night Sky color palette — matches Musannif vault graph aesthetics
THEME = {
    "background":     "#0d1117",
    "border":         "#30363d",
    "title":          "#58a6ff",
    "complete":       "#3fb950",
    "generating":     "#79c0ff",
    "pending":        "#484f58",
    "failed":         "#f85149",
    "log_timestamp":  "#8b949e",
    "log_message":    "#c9d1d9",
    "accent":         "#58a6ff",
    "surface":        "#161b22",
    "text":           "#c9d1d9",
}

# Textual CSS string — loaded by app.py
TEXTUAL_CSS = """\
Screen {
    background: #0d1117;
}

Header {
    background: #161b22;
    color: #58a6ff;
    text-style: bold;
}

Footer {
    background: #161b22;
    color: #8b949e;
}

.node-pending   { color: #484f58; }
.node-generating { color: #79c0ff; }
.node-complete  { color: #3fb950; }
.node-failed    { color: #f85149; }

.panel-title {
    color: #58a6ff;
    text-style: bold;
    padding: 0 1;
}

WavePanel {
    border: solid #30363d;
    padding: 1;
}

LogPanel {
    border: solid #30363d;
    padding: 1;
    height: 12;
    overflow-y: auto;
}

ASTTree {
    border: solid #30363d;
    padding: 1;
}
"""
```

### Phase 6.2 — AST Tree widget (`src/musannif/tui/widgets/ast_tree.py`)

```python
from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from musannif.ast_parser import ASTNode, flatten_ast

STATUS_ICONS = {
    "pending":    "○",
    "generating": "◌",   # Will be animated via spinner in the dashboard
    "complete":   "✓",
    "failed":     "✗",
}

STATUS_CLASSES = {
    "pending":    "node-pending",
    "generating": "node-generating",
    "complete":   "node-complete",
    "failed":     "node-failed",
}

class ASTTreeWidget(Tree):
    """
    A Textual Tree widget that renders the heading AST with live status icons.
    Supports real-time updates via update_node_status().
    """

    def __init__(self, root: ASTNode, **kwargs) -> None:
        super().__init__(root.title, **kwargs)
        self._ast_root = root
        self._path_to_tree_node: dict[tuple[str, ...], TreeNode] = {}
        self._build_tree(root, self.root)
        self.root.expand()

    def _build_tree(self, ast_node: ASTNode, tree_node: TreeNode) -> None:
        icon = STATUS_ICONS.get(ast_node.status, "○")
        css_class = STATUS_CLASSES.get(ast_node.status, "node-pending")
        label = f"{icon} {ast_node.title}"
        tree_node.set_label(label)
        tree_node.add_class(css_class)
        self._path_to_tree_node[ast_node.path] = tree_node

        for child in ast_node.children:
            child_tree_node = tree_node.add(child.title)
            self._build_tree(child, child_tree_node)

    def update_node_status(self, node: ASTNode) -> None:
        """
        Update the visual state of one node. Called by the orchestrator's
        on_status_change callback. Thread-safe via Textual's call_from_thread.
        """
        tree_node = self._path_to_tree_node.get(node.path)
        if tree_node is None:
            return
        icon = STATUS_ICONS.get(node.status, "○")
        tree_node.set_label(f"{icon} {node.title}")
        # Remove all status classes and add the current one
        for cls in STATUS_CLASSES.values():
            tree_node.remove_class(cls)
        tree_node.add_class(STATUS_CLASSES.get(node.status, "node-pending"))
```

### Phase 6.3 — Wave panel widget (`src/musannif/tui/widgets/wave_panel.py`)

```python
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import reactive

class WavePanelWidget(Widget):
    """
    Displays wave progress. Shows each wave with status and node count.
    Updated by the orchestrator's on_wave_start callback.
    """

    def __init__(self, total_waves: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self._total_waves = total_waves
        self._wave_statuses: dict[int, str] = {}   # wave_index → "pending"|"active"|"complete"
        self._wave_counts: dict[int, int] = {}     # wave_index → node count

    def compose(self) -> ComposeResult:
        yield Static("", id="wave-content")

    def _render_waves(self) -> str:
        lines = []
        for i in range(self._total_waves):
            status = self._wave_statuses.get(i, "pending")
            count = self._wave_counts.get(i, 0)
            if status == "complete":
                icon, css = "●", "#3fb950"
            elif status == "active":
                icon, css = "◌", "#79c0ff"
            else:
                icon, css = "○", "#484f58"
            lines.append(f"[{css}]{icon}[/] Wave {i + 1} [{count} nodes]  {status.upper()}")
        return "\n".join(lines)

    def set_wave_active(self, wave_index: int, node_count: int) -> None:
        # Mark previous waves complete
        for i in range(wave_index):
            self._wave_statuses[i] = "complete"
        self._wave_statuses[wave_index] = "active"
        self._wave_counts[wave_index] = node_count
        self.query_one("#wave-content", Static).update(self._render_waves())

    def mark_all_complete(self) -> None:
        for i in range(self._total_waves):
            self._wave_statuses[i] = "complete"
        self.query_one("#wave-content", Static).update(self._render_waves())
```

### Phase 6.4 — Log panel widget (`src/musannif/tui/widgets/log_panel.py`)

```python
from datetime import datetime
from textual.widgets import RichLog

class LogPanelWidget(RichLog):
    """
    A scrolling log panel. Entries are written via append().
    Uses RichLog for efficient streaming updates.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(highlight=True, markup=True, wrap=True, **kwargs)

    def log_event(self, message: str, level: str = "info") -> None:
        """
        Append a timestamped log entry.

        Args:
            message: The log message.
            level:   "info" (cyan), "success" (green), "warn" (yellow), "error" (red).
        """
        color_map = {
            "info":    "#79c0ff",
            "success": "#3fb950",
            "warn":    "#e3b341",
            "error":   "#f85149",
        }
        color = color_map.get(level, "#c9d1d9")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.write(f"[#8b949e]{timestamp}[/]  [{color}]{message}[/]")
```

### Phase 6.5 — Screen 1: Decomposition Review (`src/musannif/tui/screens/decomposition.py`)

```python
from __future__ import annotations
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, TextArea
from textual.containers import Horizontal, Vertical
from musannif.ast_parser import ASTNode, ast_to_markdown_outline, parse_markdown_ast
from musannif.tui.widgets.ast_tree import ASTTreeWidget

class DecompositionScreen(Screen):
    """
    Screen 1: Approval Gate.

    Left panel: interactive AST tree (read-only display).
    Right panel: editable markdown outline TextArea.
    Bottom: [Approve] and [Quit] buttons.

    The user can edit the markdown outline directly. On [Approve],
    the outline is re-parsed into an AST and returned to the app.
    """

    BINDINGS = [
        ("ctrl+a", "approve", "Approve"),
        ("ctrl+q", "quit_app", "Quit"),
    ]

    def __init__(self, root: ASTNode, **kwargs) -> None:
        super().__init__(**kwargs)
        self._root = root
        self._outline = ast_to_markdown_outline(root)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="left-panel"):
                yield Static("AST Preview", classes="panel-title")
                yield ASTTreeWidget(self._root, id="ast-tree")
            with Vertical(id="right-panel"):
                yield Static("Edit Outline  (Ctrl+A to approve)", classes="panel-title")
                yield TextArea(self._outline, id="outline-editor", language="markdown")
        with Horizontal(id="button-row"):
            yield Button("Approve & Generate", id="btn-approve", variant="success")
            yield Button("Quit", id="btn-quit", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-approve":
            self.action_approve()
        elif event.button.id == "btn-quit":
            self.action_quit_app()

    def action_approve(self) -> None:
        editor = self.query_one("#outline-editor", TextArea)
        edited_outline = editor.text
        try:
            new_root = parse_markdown_ast(edited_outline)
            self.dismiss(new_root)
        except ValueError as e:
            self.notify(f"Parse error: {e}", severity="error")

    def action_quit_app(self) -> None:
        self.app.exit(None)
```

### Phase 6.6 — Screen 2: Generation Dashboard (`src/musannif/tui/screens/dashboard.py`)

```python
from __future__ import annotations
import asyncio
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical
from musannif.ast_parser import ASTNode
from musannif.graph import PipelineGraph
from musannif.orchestrator import run_orchestrator
from musannif.tui.widgets.ast_tree import ASTTreeWidget
from musannif.tui.widgets.wave_panel import WavePanelWidget
from musannif.tui.widgets.log_panel import LogPanelWidget
import anthropic

class DashboardScreen(Screen):
    """
    Screen 2: Live generation dashboard.

    Left panel: AST tree with live status updates.
    Right panel: Wave progress.
    Bottom panel: Scrolling log.

    Generation runs in a background asyncio task started on mount.
    UI updates are dispatched via call_from_thread (safe from async tasks).
    """

    def __init__(
        self,
        graph: PipelineGraph,
        model: str,
        client: anthropic.AsyncAnthropic,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._graph = graph
        self._model = model
        self._client = client

    def compose(self) -> ComposeResult:
        root = self._graph.get_node(
            next(iter(n.path for n in self._graph.all_nodes()))
        )
        waves = self._graph.compute_waves()
        yield Header()
        with Horizontal():
            with Vertical(id="left-panel"):
                yield Static("Generation Tree", classes="panel-title")
                yield ASTTreeWidget(root, id="ast-tree")
            with Vertical(id="right-panel"):
                yield Static("Wave Progress", classes="panel-title")
                yield WavePanelWidget(len(waves), id="wave-panel")
        yield Static("Live Log", classes="panel-title")
        yield LogPanelWidget(id="log-panel")
        yield Footer()

    def on_mount(self) -> None:
        """Start the orchestrator as a background asyncio task."""
        self.run_worker(self._run_generation(), exclusive=True)

    async def _run_generation(self) -> None:
        log = self.query_one("#log-panel", LogPanelWidget)
        tree_widget = self.query_one("#ast-tree", ASTTreeWidget)
        wave_widget = self.query_one("#wave-panel", WavePanelWidget)

        def on_status_change(node: ASTNode) -> None:
            # call_from_thread is not needed here because _run_generation
            # is already running in the Textual worker (same event loop).
            tree_widget.update_node_status(node)
            level = "success" if node.status == "complete" else (
                "error" if node.status == "failed" else "info"
            )
            log.log_event(f"{node.status.upper()}: {node.address}", level=level)

        def on_wave_start(wave_index: int, wave_nodes: list) -> None:
            wave_widget.set_wave_active(wave_index, len(wave_nodes))
            log.log_event(
                f"Wave {wave_index + 1} started — {len(wave_nodes)} node(s) in parallel",
                level="info"
            )

        try:
            await run_orchestrator(
                self._graph,
                model=self._model,
                client=self._client,
                on_status_change=on_status_change,
                on_wave_start=on_wave_start,
            )
            wave_widget.mark_all_complete()
            log.log_event("All nodes complete. Assembling document...", level="success")
            self.dismiss("complete")
        except Exception as e:
            log.log_event(f"Generation failed: {e}", level="error")
            self.dismiss("failed")
```

### Phase 6.7 — Screen 3: Completion Summary (`src/musannif/tui/screens/summary.py`)

```python
from __future__ import annotations
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical
from musannif.ast_parser import ASTNode, flatten_ast

class SummaryScreen(Screen):
    """
    Screen 3: Completion summary. Displayed after all nodes are generated.
    Shows stats and the output file path.
    """

    def __init__(self, root: ASTNode, output_path: str, elapsed: float, **kwargs) -> None:
        super().__init__(**kwargs)
        self._root = root
        self._output_path = output_path
        self._elapsed = elapsed

    def compose(self) -> ComposeResult:
        nodes = flatten_ast(self._root)
        complete = sum(1 for n in nodes if n.status == "complete")
        failed = sum(1 for n in nodes if n.status == "failed")
        elapsed_str = f"{self._elapsed:.1f}s"

        yield Header()
        with Vertical(id="summary-content"):
            yield Static("[#3fb950]Pipeline complete.[/]", classes="panel-title")
            yield Static(f"Total nodes:    {len(nodes)}")
            yield Static(f"Complete:       [#3fb950]{complete}[/]")
            yield Static(f"Failed:         [#f85149]{failed}[/]" if failed else "Failed:         0")
            yield Static(f"Time elapsed:   {elapsed_str}")
            yield Static(f"Output file:    [#58a6ff]{self._output_path}[/]")
        yield Button("Exit", id="btn-exit", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-exit":
            self.app.exit()
```

### Phase 6.8 — Main app (`src/musannif/tui/app.py`)

```python
from __future__ import annotations
import time
import anthropic
from textual.app import App
from musannif.ast_parser import ASTNode
from musannif.graph import PipelineGraph
from musannif.assembler import write_document
from musannif.tui.theme import TEXTUAL_CSS
from musannif.tui.screens.decomposition import DecompositionScreen
from musannif.tui.screens.dashboard import DashboardScreen
from musannif.tui.screens.summary import SummaryScreen

class MusannifApp(App):
    """
    Root Textual application. Manages screen transitions.

    Flow:
        DecompositionScreen  →  (user approves)  →
        DashboardScreen      →  (generation done) →
        SummaryScreen        →  (user exits)
    """

    CSS = TEXTUAL_CSS
    TITLE = "MUSANNIF"
    SUB_TITLE = "Structured Document Generator"

    def __init__(
        self,
        root: ASTNode,
        model: str,
        planner_model: str,
        output_path: str,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._initial_root = root
        self._model = model
        self._output_path = output_path
        self._client = anthropic.AsyncAnthropic()
        self._start_time: float = 0.0

    def on_mount(self) -> None:
        self.push_screen(
            DecompositionScreen(self._initial_root),
            callback=self._on_decomposition_approved,
        )

    def _on_decomposition_approved(self, approved_root: ASTNode | None) -> None:
        if approved_root is None:
            self.exit()
            return
        try:
            graph = PipelineGraph(approved_root)
        except ValueError as e:
            self.notify(f"Graph error: {e}", severity="error")
            return
        self._start_time = time.monotonic()
        self.push_screen(
            DashboardScreen(graph, self._model, self._client),
            callback=lambda result: self._on_generation_done(result, approved_root, graph),
        )

    def _on_generation_done(
        self, result: str, root: ASTNode, graph: PipelineGraph
    ) -> None:
        elapsed = time.monotonic() - self._start_time
        if result == "complete":
            try:
                write_document(root, self._output_path, strict=False)
            except Exception as e:
                self.notify(f"Write failed: {e}", severity="error")
        self.push_screen(SummaryScreen(root, self._output_path, elapsed))
```

### Phase 6.9 — Wire CLI to TUI (`src/musannif/cli.py` — final)

```python
import asyncio
import typer
import anthropic
from musannif.planner import run_planner
from musannif.tui.app import MusannifApp

app = typer.Typer(
    name="musannif",
    help="Musannif — structured long-form document generator.",
    add_completion=False,
)

@app.command()
def run(
    prompt: str = typer.Argument(..., help="Topic or prompt to decompose and generate."),
    output: str = typer.Option("output.md", "--output", "-o", help="Output file path."),
    model: str = typer.Option("claude-opus-4-5", "--model", "-m", help="Generation model."),
    planner_model: str = typer.Option("claude-haiku-4-5", "--planner-model", help="Planning model."),
):
    """Decompose a prompt, review the plan, then generate a structured document."""

    typer.echo("Running planner...")
    root = asyncio.run(run_planner(prompt, model=planner_model))
    typer.echo(f"Plan ready — {sum(1 for _ in __import__('musannif.ast_parser', fromlist=['flatten_ast']).flatten_ast(root))} nodes.")

    musannif_app = MusannifApp(
        root=root,
        model=model,
        planner_model=planner_model,
        output_path=output,
    )
    musannif_app.run()

if __name__ == "__main__":
    app()
```

---

## Concurrency Model — Reference

| Location | Mechanism | Notes |
|---|---|---|
| Wave parallel execution | `asyncio.gather(*tasks)` | All nodes in a wave are dispatched concurrently. No thread pool — pure async. |
| Planner call | `await client.messages.create(...)` | Single async call, not parallelized. |
| Tier 3 full-text read | `open(...)` sync call inside async context | Acceptable — file reads are fast. If scaling, wrap in `asyncio.to_thread`. |
| TUI ↔ orchestrator | Textual Worker (`run_worker`) | Orchestrator runs inside Textual's async worker. No `call_from_thread` needed — same event loop. |
| Retry on validation failure | Sequential in same coroutine | Retries are not parallel — the node must succeed before the wave can complete. |

---

## Test Coverage Target

| Module | Min coverage |
|---|---|
| ast_parser.py | 100% |
| graph.py | 100% |
| validator.py | 100% |
| context.py | 95% |
| planner.py | 90% (API calls mocked) |
| orchestrator.py | 90% (API calls mocked) |
| assembler.py | 100% |
| tui/* | Not unit tested — Textual has its own pilot testing framework for integration tests |

Run full suite:
```bash
uv run pytest --cov=src/musannif --cov-report=term-missing -v
```

---

## Stage Completion Checklist

| Stage | Deliverable | Exit criteria |
|---|---|---|
| 0 | Scaffold | `musannif --help` works. `pytest` exits 0. |
| 1 | AST Parser | 30 tests green. `parse_markdown_ast` handles all heading depth combinations. |
| 2 | Graph Engine | 16 tests green. Cycle detection works. Wave computation verified. |
| 3 | Validator + Context | 20 tests green. Summary extraction handles all edge cases. |
| 4 | Planner + Orchestrator | 18 tests green. Wave ordering test confirms dependency contract. |
| 5 | Assembler | 8 tests green. Output file written correctly. |
| 6 | TUI | App launches. All three screens render. Generation runs end-to-end with real API key. |
