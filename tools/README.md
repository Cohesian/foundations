# tools

Small maintenance scripts for the k-graph. Not k-graph nodes.

## `validate_kgraph.py`

Checks that the k-graph (`k-graph/` structure + `papers/` / bucket content) is
internally consistent, so structure and content never drift apart.

For every node in `k-graph/` it verifies:

- **edges resolve** — each `edges.g` (grouping children), `edges.l` (linear
  `prev` / `next`), and `edges.r` (related) target points to a real sibling node;
- **content resolves** — each leaf's declared `formats` is configured in
  [`k-graph.toml`](../k-graph.toml); **local** formats (e.g. `md`, `ipynb`) must have
  their file on disk at `<base>/<path>/<id>.<ext>`, while **remote** formats
  (e.g. `mp4` in a bucket) are trusted;
- **kinds match location** — `T` / `L` use `props.yaml` in a directory; `F` / `Fd`
  are `<id>.yaml` leaves.

### Usage

```bash
pip install pyyaml        # one-time dependency
python tools/validate_kgraph.py
```

Exits `0` when everything resolves, non-zero with a list of problems otherwise.
Run it after editing the tree, adding a content file, or declaring a new format.

See [`docs/KGRAPH.md`](../docs/KGRAPH.md) for the full layout the validator enforces.
