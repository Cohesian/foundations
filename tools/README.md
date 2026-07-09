# tools

Small maintenance scripts for the k-graph. Not k-graph nodes.

## `validate_kgraph.py`

Checks that the k-graph (`k-graph/` structure + `data/` content trees) is
internally consistent, so structure and content never drift apart.

For every node in `k-graph/` it verifies:

- **edges resolve** — each `edges.g` (grouping children), `edges.l` (linear
  `prev` / `next`), and `edges.r` (related) target points to a real sibling node;
- **content resolves** — each leaf's `data` tree lists `sources` in
  [`k-graph.toml`](../k-graph.toml); local `path` sources must have files on disk
  where required; `hash` sources must have map entries; local mp4 builds optional;
- **kinds match location** — `T` / `L` use `props.yaml` in a directory; `F` / `Fd`
  are `<id>.yaml` leaves.

### Usage

```bash
pip install pyyaml        # one-time dependency
python tools/validate_kgraph.py
```

Exits `0` when everything resolves, non-zero with a list of problems otherwise.
Run it after editing the tree, adding a content file, or declaring new data.

## `resolve_kgraph.py`

Projects a k-graph key through a source (for debugging / site wiring):

```bash
python tools/resolve_kgraph.py media.videos T-computer-science/L-composite/F-01-carbon-binder
python tools/resolve_kgraph.py media.videos T-computer-science/L-composite/F-01-carbon-binder --source local
```

Uses `serve` from `k-graph.toml` when `--source` is omitted.

See [`docs/KGRAPH.md`](../docs/KGRAPH.md) for the full layout the validator enforces.
