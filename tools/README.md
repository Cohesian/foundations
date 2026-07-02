# tools

Small maintenance scripts for the corpus. Not corpus nodes.

## `validate_corpus.py`

Checks that the three-dir corpus (`tree/` + `papers/` + `media/`) is internally
consistent, so structure and content never drift apart.

For every node in `tree/` it verifies:

- **edges resolve** — each `edges.g` (grouping children), `edges.l` (linear
  `prev` / `next`), and `edges.r` (related) target points to a real sibling node;
- **content exists** — each leaf's declared `formats` has its file present in the
  right domain: `md` / `ipynb` in `papers/`, `mp4` in `media/`, at the same
  relative path (`<domain>/<path>/<id>.<ext>`);
- **kinds match location** — `T` / `L` use `props.yaml` in a directory; `F` / `Fd`
  are `<id>.yaml` leaves.

### Usage

```bash
pip install pyyaml        # one-time dependency
python tools/validate_corpus.py
```

Exits `0` when everything resolves, non-zero with a list of problems otherwise.
Run it after editing the tree, adding a content file, or declaring a new format.

See [`docs/CORPUS.md`](../docs/CORPUS.md) for the full layout the validator enforces.
