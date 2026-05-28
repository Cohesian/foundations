---
title: Agent Architecture
description: Agent structure for inference over semantic data.
kind: F
edges:
  g: []
  l:
    prev: F-01-theorem.md
    next: F-03-conclusions.md
  r: []
---

# Agent Architecture

This file translates the inference theorem into an agent/function architecture.

The goal is to separate the expensive inductive work from the cheaper mechanical work.

Context is the expensive resource.

Therefore, each function should receive only the context it actually needs.

---

## Core artifacts

The system produces and consumes three main artifacts:

```txt
S = Data Structure Semantics
F = Extraction Fingerprint
X = Scraper / Extractor Functor
```

Where:

- `S` describes what the data is.
- `F` describes where the data is found in a concrete representation.
- `X` transforms an input file into normalized JSON.

The source files are only needed for induction.

Once `S` and `F` exist, later functions should avoid rereading the original files unless repair, validation, or regeneration is required.

---

## Function S: induce semantics

```txt
Fn S: files[] → semantics
```

This function reads the `n` sibling files and induces the representation-independent data structure semantics.

It answers:

```txt
What is the data structure underneath these files?
```

It should infer:

- fields
- primitive types
- composite types
- nesting
- optionality
- shared fields
- variant fields
- semantic descriptions

This is a high-context function because it must inspect the input examples.

Symbolically:

$$
S(I_1, I_2, ..., I_n) = \mathcal{S}
$$

Where:

- $I_k$ is an input file
- $\mathcal{S}$ is the induced semantic backbone

---

## Function F: induce fingerprint

```txt
Fn F: files[] + semantics → fingerprint
```

This function reads the sibling files and maps the induced semantics to representation-specific targets.

It answers:

```txt
Where does each semantic field live inside this representation?
```

For HTML, this may include:

- DOM selectors
- CSS selectors
- XPath routes
- heading anchors
- semantic sections
- repeated item selectors
- attributes
- fallback routes
- normalization rules
- confidence scores

This is also a high-context function because it must inspect the input examples.

Symbolically:

$$
F(I_1, I_2, ..., I_n, \mathcal{S}) = \mathcal{F}
$$

Where:

- $\mathcal{S}$ is the semantic backbone
- $\mathcal{F}$ is the extraction fingerprint

---

## Function X: generate scraper functor

```txt
Fn X: semantics + fingerprint → scraper
```

This function generates an executable scraper/extractor from the already-induced artifacts.

It answers:

```txt
How do we turn a new sibling input file into JSON?
```

For HTML, this may generate a Python script using a DOM-capable parser such as BeautifulSoup.

This can be a low-context function if `S` and `F` are complete enough.

It should not need to reread the original files.

Symbolically:

$$
X(\mathcal{S}, \mathcal{F}) = s_R
$$

Where:

- $s_R$ is the scraper/extractor for representation family $R$

The scraper then acts as a function:

$$
s_R(X_R) = J
$$

Where:

- $X_R$ is a new input file from representation family $R$
- $J$ is the normalized JSON output

For HTML:

$$
s_{html}(\langle name \rangle.html) = \langle name \rangle.json
$$

---

## Full pipeline

The full pipeline is:

```txt
files[] → S → F → X → scraper → json
```

More explicitly:

```txt
files[]
  → induce semantics
  → induce fingerprint
  → generate scraper
  → run scraper on new file
  → output JSON
```

Or symbolically:

$$
I_{1..n} \xrightarrow{S} \mathcal{S}
$$

$$
(I_{1..n}, \mathcal{S}) \xrightarrow{F} \mathcal{F}
$$

$$
(\mathcal{S}, \mathcal{F}) \xrightarrow{X} s_R
$$

$$
X_R \xrightarrow{s_R} J
$$

---

## Composition

The functions can be composed.

A full one-run agent may perform:

```txt
X ∘ F ∘ S
```

Meaning:

```txt
first induce semantics,
then induce fingerprint,
then generate the scraper.
```

Expanded:

$$
(X \circ F \circ S)(I_{1..n}) = s_R
$$

This means a set of examples can be transformed into a reusable scraper.

However, the functions should also be callable independently.

This allows different workflows.

---

## Independent workflows

### Semantic-only workflow

Use this when we only want to know the semantic backbone.

```txt
files[] → S
```

Output:

```txt
semantics.json
```

### Fingerprint workflow

Use this when semantics already exists, but the extraction targets need to be induced.

```txt
files[] + semantics.json → F
```

Output:

```txt
fingerprint.json
```

### Stateless scraper-generation workflow

Use this when both semantics and fingerprint are already cooked.

```txt
semantics.json + fingerprint.json → X
```

Output:

```txt
scraper.py
```

This is the cheapest script-generation mode because it does not require the original files.

### Full one-run workflow

Use this when we want the agent to do everything in one pass.

```txt
files[] → semantics.json + fingerprint.json + scraper.py
```

This is convenient, but it is more context-expensive.

---

## Context cost

The functions have different context requirements.

| Function | Needs original files? | Context cost | Output |
| --- | --- | --- | --- |
| `S` | yes | high | `semantics.json` |
| `F` | yes | high | `fingerprint.json` |
| `X` | no, if `S` and `F` are complete | low | `scraper.py` |
| `s_R` | no | low | `<name>.json` |

The ideal architecture is:

```txt
Use context-heavy induction once.
Then reuse the induced artifacts many times.
```

---

## Category-theoretic intuition

The architecture can be understood as a chain of structure-preserving transformations.

Each function maps one kind of object into another:

```txt
Inputs → Semantics → Fingerprint → Scraper → JSON
```

The scraper itself acts like a functor between representations:

```txt
HTML-family object → JSON-family object
```

It preserves the semantic identity while changing the representation.

For example:

```txt
profile.html → profile.json
```

The content identity remains the same, but the representational form changes.

So the scraper is not merely copying text.

It is preserving semantic structure across representation boundaries.

---

## Design rule

The induction functions may be intelligent, probabilistic, and context-heavy.

The scraper function should be deterministic, stateless, and cheap to run.

In short:

```txt
S discovers the semantic space.
F targets the source representation.
X generates the machine.
s_R runs the machine.
```